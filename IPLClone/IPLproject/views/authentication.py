from django.views import View
from IPLproject.models import *
from IPLproject.forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import F


def logout_user(request):
    logout(request)
    return redirect('login')


class LoginController(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('colleges_html')
        login_form = LoginForm()
        years = Match.objects.values('season').distinct()

        return render(request,
                      template_name='login.html',
                      context={
                          'form':login_form,
                          'title':"Login",
                          'logged_in': request.user.is_authenticated,
                          'seasons': years,
                          'currentSeason': 'Seasons',

                      }
                      )

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('season_details')
        messages.error(request, 'Invalid credentials')
        years = Match.objects.values('season').distinct()
        return render(request, template_name='login.html', context={'form': login_form, 'title': "Login", 'logged_in': request.user.is_authenticated, 'seasons': years})




class SignUpController(View):
    def get(self, request, *args, **kwargs):
        signup_form = SignUpForm()
        years = Match.objects.values('season').distinct()
        return render(request,
                      template_name='signup.html',
                      context={
                          'form':signup_form,
                          'title': "Sign Up",
                          'logged_in': request.user.is_authenticated,
                          'seasons': years, 'currentSeason': 'Seasons',

                      }
                      )
    def post(self, request):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            first_name = signup_form.cleaned_data['firstname']
            last_name = signup_form.cleaned_data['lastname']
            username = signup_form.cleaned_data['username']
            password = signup_form.cleaned_data['password']

            if User.objects.filter(username=username):
                messages.error(request, 'User already exists!')
                return redirect('signup')

            user = User.objects.create_user(
                first_name=first_name,
                last_name = last_name,
                username=username,
                password=password
            )
            user.save()


            if user is not None:
                login(request, user)
                return redirect('season_details')
        messages.error(request, 'Invalid credentials')
        return redirect('signup')


