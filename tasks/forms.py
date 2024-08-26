from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    # le digo en que formulario esta basado este formulario
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']

        # podemos colocar clases y estilizar formularios de esta forma
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control', "placeholder": "write a title"}),
            "description": forms.Textarea(attrs={'class': 'form-control', "placeholder": "write a description", "rows": 3}),
            "important": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
