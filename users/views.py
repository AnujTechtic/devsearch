from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile

# Create your views here.
def loginUser(request):
   if request.user.is_authenticated:
      return redirect('profiles')
   if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      try:
         user = User.objects.get(username = username)
      except:
        messages.error(request, "Username does not exist")
        
      user = authenticate(request, username=username, password=password)
      if user is not None:
         login(request, user )
         return redirect('profiles')
      else:
         messages.error(request, "Username or Password is Incorrect")
   return render(request, 'users/login-register.html')

def logoutUser(request):
   logout(request)
   messages.info(request, "User was Logged Out")
   return redirect ('login')

def registerUser(request):
   page = 'register'
   form = CustomUserCreationForm()
   if request.method == 'POST':
      form = CustomUserCreationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.username = user.username.lower()
         user.save()
         messages.success(request, 'User account was created')
         login(request, user)
         return redirect('profiles')
      else:
         messages.success(request, 'An error has occurred during registration')
   context = {'page':page, 'form':form}
   return render(request, 'users/login-register.html', context)

def profiles(request):
 profiles = Profile.objects.all()
 context = {'profiles': profiles}
 return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
 profiles = Profile.objects.get(id = pk)
 topSkills = profiles.skill_set.exclude(description__exact="")
 otherSkills = profiles.skill_set.filter(description="")
 context = {'profiles': profiles, 'topSkills':topSkills, 'otherSkills':otherSkills}
 return render(request, 'users/user-profile.html', context)
@login_required(login_url='login')
def userAcount(request):
   profile = request.user.profile
   skills = profile.skill_set.all()
   projects = profile.project_set.all()
   context = {'profile':profile,'skills':skills, 'projects':projects}
   return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
   form = ProfileForm
   context = {'form':form}
   return render(request, 'users/profile-form.html', context)

