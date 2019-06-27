from django.views import View
from IPLproject.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F


class MatchView(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request, *args, **kwargs):
        if kwargs.get('match_id'):
            years = Match.objects.values('season').distinct()
            match=Match.objects.get(id=kwargs.get('match_id'))
            delivery = Deliveries.objects.filter(match_id=kwargs.get('match_id')).values('match_id', 'inning',
                                                                                         'batting_team', 'bowling_team',
                                                                                         'over', 'ball', 'batsman',
                                                                                         'bowler', 'is_super_over',
                                                                                         'wide_runs', 'bye_runs',
                                                                                         'legbye_runs', 'noball_runs',
                                                                                         'penalty_runs', 'batsman_runs',
                                                                                         'extra_runs', 'total_runs',
                                                                                         'player_dismissed',
                                                                                         'dismissal_kind', 'fielder')
            batsmen = delivery.values('batting_team','batsman', 'total_runs')
            top3batsmen = batsmen.values('batsman', 'batting_team').annotate(total_runs=Sum('total_runs')).order_by('-total_runs')[:3]
            bowlers = delivery.values('bowler', 'bowling_team', 'player_dismissed').exclude(player_dismissed='')
            top3bowlers = bowlers.values('bowler', 'bowling_team').annotate(total_wickets=Count('player_dismissed')).order_by('-total_wickets')[:3]
            inning1 = delivery.filter(inning=1)
            inning1_overs = inning1.values('over').distinct()
            inning2 = delivery.filter(inning=2)
            inning2_overs = inning2.values('over').distinct()
            index =0
            runrate=0
            for i, inning in enumerate(inning1):
                if i>1 and i<len(inning1) and inning1[i-1]['over'] != inning1[i]['over']:
                    inning['run_rate'] = runrate/6
                    runrate=0
                    index=0
                if inning['wide_runs'] !=0 or inning['noball_runs'] !=0:
                    index+=1
                inning['ballIndex'] = index
                runrate += inning['total_runs']

            index = 0
            for i, inning in enumerate(inning2):
                if inning['wide_runs'] != 0 or inning['noball_runs'] != 0:
                    index += 1
                inning['ballIndex'] = index
                if i < len(inning2) - 1 and inning2[i]['over'] != inning2[i + 1]['over']:
                    index = 0


            m = Match.objects.filter(id=kwargs.get('match_id')).values('team1', 'team2', 'toss_winner', 'toss_decision', 'win_by_runs', 'win_by_wickets')
            if m[0]['win_by_wickets'] > 0:
                if m[0]['toss_decision'] == 'field':
                    winner = m[0]['toss_winner']
                else:
                    if m[0]['toss_winner'] == m[0]['team1']:
                        winner = m[0]['team2']
                    else:
                        winner = m[0]['team1']
            elif m[0]['win_by_runs'] > 0:
                if m[0]['toss_decision'] == 'bat':
                    winner = m[0]['toss_winner']
                else:
                    if m[0]['toss_winner'] == m[0]['team1']:
                        winner = m[0]['team2']
                    else:
                        winner = m[0]['team1']

            currentSeason = kwargs.get('season_id')
            teams = Match.objects.annotate(team=F('team1')).distinct().values('team') | Match.objects.annotate(
                team=F('team2')).distinct().values('team')
            teams = teams.filter(season=currentSeason)
            for team in teams:
                team['team_logo'] = team['team'].replace(' ', '_')
                team['team_logo'] = "/static/images/" + team['team_logo'] + ".png"
            return render(request,
                          template_name='match_details.html',
                          context={
                              'seasons': years,
                              'match': match,
                              'inning1': inning1,
                              'inning2': inning2,
                              'top3batsmen': top3batsmen,
                              'top3bowlers': top3bowlers,
                              'teams': teams,
                              'currentSeason': currentSeason,
                              'logged_in': request.user.is_authenticated,
                              'username': request.user.get_username(),
                              'winner':winner,
                          }
                          )






        

