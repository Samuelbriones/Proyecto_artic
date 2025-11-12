from django import forms
from .models import Architect, ApplicationReview
from datetime import datetime


class ArchitectForm(forms.ModelForm):
    class Meta:
        model = Architect
        fields = [
            'full_name',
            'registration_number',
            'qualification',
            'institution',
            'graduation_year',
            'document',
        ]
        widgets = {
            'graduation_year': forms.NumberInput(attrs={'min': 1900, 'max': datetime.now().year, 'class':'w-full border rounded px-3 py-2'}),
            'full_name': forms.TextInput(attrs={'class':'w-full border rounded px-3 py-2'}),
            'registration_number': forms.TextInput(attrs={'class':'w-full border rounded px-3 py-2'}),
            'qualification': forms.TextInput(attrs={'class':'w-full border rounded px-3 py-2'}),
            'institution': forms.TextInput(attrs={'class':'w-full border rounded px-3 py-2'}),
            'document': forms.ClearableFileInput(attrs={'class':'w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add default classes to any widget that lacks them (keeps consistency)
        for fname, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                # file inputs often don't need same classes
                if isinstance(field.widget, forms.ClearableFileInput):
                    field.widget.attrs.update({'class':'w-full'})
                else:
                    field.widget.attrs.update({'class':'w-full border rounded px-3 py-2'})

    def clean_document(self):
        doc = self.cleaned_data.get('document')
        if doc:
            if not doc.name.lower().endswith('.pdf'):
                raise forms.ValidationError('El archivo debe ser un PDF.')
            # tamaño opcional: limitar a 5MB
            if doc.size > 5 * 1024 * 1024:
                raise forms.ValidationError('El archivo es demasiado grande (max 5MB).')
        return doc

    def clean_graduation_year(self):
        year = self.cleaned_data.get('graduation_year')
        current = datetime.now().year
        if year < 1900 or year > current:
            raise forms.ValidationError(f'El año debe estar entre 1900 y {current}')
        return year

class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = ApplicationReview
        fields = ['status', 'comments']
        widgets = {
            'status': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'comments': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2', 'rows': 4}),
        }
