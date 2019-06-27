from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.IntegerField()
    city = models.CharField(max_length=64, null=True)
    date = models.DateField()
    team1 = models.CharField(max_length=64, null=True)
    team2 = models.CharField(max_length=64, null=True)
    toss_winner = models.CharField(max_length=64, null=True)
    toss_decision = models.CharField(max_length=64, null=True)
    result = models.CharField(max_length=64, null=True)
    dl_applied = models.IntegerField()
    winner = models.CharField(max_length=64, null=True)
    win_by_runs = models.IntegerField()
    win_by_wickets = models.IntegerField()
    player_of_match = models.CharField(max_length=64, null=True)
    venue = models.CharField(max_length=64, null=True)
    umpire1 = models.CharField(max_length=64, null=True)
    umpire2 = models.CharField(max_length=64, null=True)
    umpire3 = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.team1 + " V/S " + self.team2


class Deliveries(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    inning = models.IntegerField()
    batting_team = models.CharField(max_length=64, null=True)
    bowling_team = models.CharField(max_length=64, null=True)
    over = models.IntegerField()
    ball = models.IntegerField()
    batsman = models.CharField(max_length=64, null=True)
    non_striker = models.CharField(max_length=64, null=True)
    bowler = models.CharField(max_length=64, null=True)
    is_super_over = models.IntegerField()
    wide_runs = models.IntegerField()
    bye_runs = models.IntegerField()
    legbye_runs = models.IntegerField()
    noball_runs = models.IntegerField()
    penalty_runs = models.IntegerField()
    batsman_runs = models.IntegerField()
    extra_runs = models.IntegerField()
    total_runs = models.IntegerField()
    player_dismissed = models.CharField(max_length=64, null=True)
    dismissal_kind = models.CharField(max_length=64, null=True)
    fielder = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.bowling_team + " V/S " + self.batting_team


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.user.email



