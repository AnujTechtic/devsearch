from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

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

def logoutUser(request):
   logout(request)
   messages.error(request, "User was Logged Out")
   return redirect ('login')

