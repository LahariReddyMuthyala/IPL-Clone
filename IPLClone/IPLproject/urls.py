from django.contrib import admin
from django.urls import path
from IPLproject.views import *

urlpatterns = [
    path('login/', LoginController.as_view(), name="login"),
    path('signup/', SignUpController.as_view(), name="signup"),
    path('logout/', logout_user, name="logout"),
    path('', HomePageView.as_view(), name="home_page"),
    path('seasons/', SeasonView.as_view(), name="season_details"),
    path('seasons/<int:season_id>/', SeasonView.as_view(), name="season_details"),
    path('seasons/<int:season_id>/<int:match_id>/', MatchView.as_view(), name="match_details"),
    path('pointstable/<int:season_id>/', PointsTableView.as_view(), name="points_table"),
    path('teampage/<str:team_name>/', TeamPageView.as_view(), name="team_page")




]
