from django.views import View
from IPLproject.models import *
from django.shortcuts import render
from django.db.models import F, Q


class TeamPageView(View):
    def get(self, request, *args, **kwargs):
        if kwargs.get('team_name'):
            matches = Match.objects.filter(Q(team1=kwargs.get('team_name')) | Q(team2=kwargs.get('team_name')))
            team_seasons = matches.values('season').distinct().order_by('-season')
            years = Match.objects.values('season').distinct().order_by('season')
            team_logo = dict()
            team_logo['team_logo'] = "/static/images/" + kwargs.get('team_name').replace(' ', '_') + ".png"
            return render(request,
                          template_name='team_page.html',
                          context={
                              'seasons': years,
                              'logged_in': request.user.is_authenticated,
                              'username': request.user.get_username(),
                              'team_name': kwargs.get('team_name'),
                              'matches': matches,
                              'team_seasons': team_seasons,
                              'team_logo': team_logo,
                          }
                          )
