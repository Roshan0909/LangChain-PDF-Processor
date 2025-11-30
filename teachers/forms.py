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
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document Title'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.ppt,.pptx'}),
        }
    
    def clean_pdf_file(self):
        file = self.cleaned_data.get('pdf_file')
        if file:
            ext = file.name.split('.')[-1].lower()
            allowed = ['pdf', 'doc', 'docx', 'ppt', 'pptx']
            if ext not in allowed:
                raise forms.ValidationError(f'Only PDF, DOC, DOCX, PPT, and PPTX files are allowed. You uploaded: {ext}')
            if file.size > 50 * 1024 * 1024:  # 50MB limit
                raise forms.ValidationError('File size must be under 50MB')
        return file
