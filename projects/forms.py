from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList
from .models import Project
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','demo_link', 'source_link', 'tags',
                   'feautred_image']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),

        } 

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__( *args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input', })



        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add Title'})    