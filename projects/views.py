from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm


def projecs(request):
    projects = Project.objects.all()
    return render(request, 'projects/projec.html', {'projects':projects})

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tags.all()
    return render(request, 'projects/project.html', {'project':projectObj})

def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projec')
    context = {'form': form }
    return render(request, "projects/project_form.html", context)

def updateProject(request, pk):
    project = Project.objects.get(id= pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projec')
    context = {'form': form }
    return render(request, "projects/project_form.html", context)

def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projec')
    context = {'object':project}
    return render(request, 'projects/delete_confirmation.html', context)