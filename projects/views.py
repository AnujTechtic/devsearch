from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchProjects, paginateProjects


@login_required(login_url='login')
def projecs(request):
    projecs, search_query = searchProjects(request)
    custom_range, projecs  = paginateProjects(request, projecs, 3)
    context = {'projects':projecs, 'search':search_query, 'range':custom_range}
    return render(request, 'projects/projec.html', context )
@login_required(login_url='login')
def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tags.all()
    return render(request, 'projects/project.html', {'project':projectObj})

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {'form': form }
    return render(request, "projects/project_form.html", context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id= pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form }
    return render(request, "projects/project_form.html", context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id= pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projec')
    context = {'object':project}
    return render(request, 'delete_confirmation.html', context)