from django import forms
from .models import Subject, PDFNote

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Subject Description'}),
        }

class PDFNoteForm(forms.ModelForm):
    class Meta:
        model = PDFNote
        fields = ['title', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PDF Title'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
