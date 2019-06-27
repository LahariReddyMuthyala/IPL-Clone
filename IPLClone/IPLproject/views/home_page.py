from django.views import View
from IPLproject.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.db.models import F, Q

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        currentSeason=2019
        teamPoints = Match.objects.values('team1').filter(season=currentSeason).annotate(points=Count('team1') + Count('team2') + Count('winner')).order_by('-points')
        years = Match.objects.values('season').distinct().order_by('season')
        teams = Match.objects.annotate(team=F('team1')).distinct().values('team') | Match.objects.annotate(team=F('team2')).distinct().values('team')
        teams = teams.filter(season=currentSeason)
        for team in teams:
            team['team_logo'] = team['team'].replace(' ', '_')
            team['team_logo'] = "/static/images/" + team['team_logo'] + ".png"
        winner = teamPoints[0]
        winner['team_logo'] = "/static/images/" + winner['team1'].replace(' ', '_') + ".png"
        runner_up = teamPoints[1]
        runner_up['team_logo'] = "/static/images/" + runner_up['team1'].replace(' ', '_') + ".png"
        final_match_id = Match.objects.filter(season=2019).values('id').order_by('-id')[0]
        match = Match.objects.filter(season=2019).order_by('-id')[0]
        #final_match_deliveries = Deliveries.objects.filter(match_id=final_match_id['id'])
        final_match_deliveries = Deliveries.objects.filter(match_id=final_match_id['id']).values('match_id', 'inning',
                                                                                     'batting_team', 'bowling_team',
                                                                                     'over', 'ball', 'batsman',
                                                                                     'bowler', 'is_super_over',
                                                                                     'wide_runs', 'bye_runs',
                                                                                     'legbye_runs', 'noball_runs',
                                                                                     'penalty_runs', 'batsman_runs',
                                                                                     'extra_runs', 'total_runs',
                                                                                     'player_dismissed',
                                                                                     'dismissal_kind', 'fielder')
        inning1 = final_match_deliveries.filter(inning=1)
        inning2 = final_match_deliveries.filter(inning=2)
        index = 0
        runrate = 0
        for i, inning in enumerate(inning1):
            if i > 1 and i < len(inning1) and inning1[i - 1]['over'] != inning1[i]['over']:
                inning['run_rate'] = runrate / 6
                runrate = 0
                index = 0
            if inning['wide_runs'] != 0 or inning['noball_runs'] != 0:
                index += 1
            inning['ballIndex'] = index
            runrate += inning['total_runs']

        index = 0
        for i, inning in enumerate(inning2):
            if inning['wide_runs'] != 0 or inning['noball_runs'] != 0:
                index += 1
            inning['ballIndex'] = index
            if i < len(inning2) - 1 and inning2[i]['over'] != inning2[i + 1]['over']:
                index = 0

        return render(request,
                          template_name='home_page.html',
                          context={
                              'seasons': years,
                              'teamPoints': teamPoints,
                              'currentSeason': currentSeason,
                              'teams': teams,
                              'logged_in': request.user.is_authenticated,
                              'username': request.user.get_username(),
                              'winner': winner,
                              'runner_up': runner_up,
                              'match': match,
                              'inning1': inning1,
                              'inning2': inning2,

                          }
                          )


