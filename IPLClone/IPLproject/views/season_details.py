from django.views import View
from IPLproject.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import F

class SeasonView(View):
    def get(self, request, *args, **kwargs):
        years = Match.objects.values('season').distinct().order_by('season')
        if kwargs.get('season_id'):
            match = Match.objects.filter(season = kwargs['season_id']).order_by('-id')
            currentSeason = kwargs['season_id']
        else:
            match = Match.objects.filter(season = 2019).order_by('-id')
            currentSeason = 2019
        match = match.values('id', 'season', 'city', 'date', 'team1', 'team2', 'toss_winner', 'toss_decision', 'result', 'winner', 'win_by_runs', 'win_by_wickets', 'player_of_match', 'venue')
        i=0
        for m in match:
            if i>4:
                break
            if i == 0:
                m['type']='Finals'
            if i == 1:
                m['type']='Qualifier 2'
            if i == 2:
                m['type'] = 'Eliminator'
            if i == 3:
                m['type'] = 'Qualifier 1'
            i+=1

        paginator = Paginator(match, 8)
        page = request.GET.get('page')
        matches = paginator.get_page(page)
        teams = Match.objects.annotate(team=F('team1')).distinct().values('team') | Match.objects.annotate(team=F('team2')).distinct().values('team')
        teams = teams.filter(season=currentSeason)
        for team in teams:
            team['team_logo'] = team['team'].replace(' ', '_')
            team['team_logo'] = "/static/images/" + team['team_logo'] + ".png"
        return render(
            request,
            'season_details.html',
            {'seasons': years,
             'matches': matches,
             'currentSeason': currentSeason,
             'teams': teams,
             'logged_in': request.user.is_authenticated,
             'username': request.user.get_username(),

             }
        )



