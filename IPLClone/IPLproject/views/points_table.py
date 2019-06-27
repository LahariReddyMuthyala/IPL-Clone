from django.views import View
from IPLproject.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.db.models import F, Q


class PointsTableView(View):
    def get(self, request, *args, **kwargs):
        if kwargs.get('season_id'):
            years = Match.objects.values('season').distinct().order_by('season')
            teams = Match.objects.annotate(team=F('team1')).distinct().values('team') | Match.objects.annotate(team=F('team2')).distinct().values('team')
            teams = teams.filter(season=kwargs.get('season_id'))
            team_points = dict()
            for team in teams:
                team_points[team['team']] = 0
            for team in teams:
                team['team_logo'] = team['team'].replace(' ', '_')
                team['team_logo'] = "/static/images/" + team['team_logo'] + ".png"
            winner_points = Match.objects.values('winner').exclude(winner=None).filter(season=kwargs.get('season_id')).annotate(points=Count('winner') * 2).order_by('-points')
            draw_matches = Match.objects.exclude(result='normal').values('team1', 'team2').filter(season=kwargs.get('season_id'))
            for team in winner_points:
                team_points[team['winner']] += int(team['points'])
            for match in draw_matches:
                team_points[match['team1']] += 1
                team_points[match['team2']] += 1
            teamPoints=[{'team':k, 'points':team_points[k]} for k in team_points]
            teamPoints.sort(key=lambda d: d['points'], reverse=True)
            return render(request,
                          template_name='points_table.html',
                          context={
                              'seasons': years,
                              'teamPoints': teamPoints,
                              'currentSeason': kwargs.get('season_id'),
                              'teams': teams,
                              'logged_in': request.user.is_authenticated,
                              'username': request.user.get_username(),
                          }
                          )
