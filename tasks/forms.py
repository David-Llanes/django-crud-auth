from django import forms
from .models import Task

''' CreateTaskForm
1: Este formulario estará basado en un modelo. En el modelo Task.
Eso lo tenemos que indicar dentro del apartado Meta

2: Como se va a basar en un modelo, le debemos especificar que campos queremos que cree.
Para esto agregamos en Meta una lista con los fields.

3: Para agregar estilos desde un formulario, lo hacemos desde el apartado widgets.
Las clases se agregan en forma de diccionario.
'''

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'important': 'Importante'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la tarea', 'autofocus': 'on'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '¿De qué va esta tarea?'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

