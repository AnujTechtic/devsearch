from django.shortcuts import render
from .models import Profile

# Create your views here.
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