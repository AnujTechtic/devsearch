from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .models import Profile, Skill
from .utils import searchProfiles, paginateProfiles

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
         return redirect('edit-account')
      else:
         messages.success(request, 'An error has occurred during registration')
   context = {'page':page, 'form':form}
   return render(request, 'users/login-register.html', context)

def profiles(request):
 profiles, search_query = searchProfiles(request)
 custom_range, profiles  = paginateProfiles(request, profiles, 3)
 context = {'profiles': profiles, 'search':search_query, 'range':custom_range, 'profiles':profiles}
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
   profile = request.user.profile
   form = ProfileForm(instance=profile)
   if request.method == 'POST':
      form = ProfileForm(request.POST, request.FILES, instance=profile)
      if form.is_valid():
         form.save()
         return redirect('account')
   context = {'form':form}
   return render(request, 'users/profile-form.html', context)

@login_required(login_url='login')
def createSkill(request):
   form = SkillForm()
   profile = request.user.profile
   if request.method == 'POST':
      form = SkillForm(request.POST)
      if form.is_valid():
         skill = form.save(commit=False)
         skill.owner = profile
         skill.save()
         messages.success(request, "Skill was created successfully!")
         return redirect('account')
   context = {'form':form}
   return render(request, 'users/skill-form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
   profile = request.user.profile
   skill = profile.skill_set.get(id=pk)
   form = SkillForm(instance = skill)
   if request.method == 'POST':
      form = SkillForm(request.POST, instance=skill)
      if form.is_valid():
         form.save()
         messages.success(request, "Skill was updated successfully!")
         return redirect('account')
   context = {'form':form}
   return render(request, 'users/skill-form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
   profile = request.user.profile
   skill = profile.skill_set.get(id=pk)
   if request.method == 'POST':
      skill.delete()
      messages.success(request, "Skill was deleted successfully!")
      return redirect ('account')
   context = {'object':skill}
   return render(request, 'delete_confirmation.html', context)


