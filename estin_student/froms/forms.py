from django import forms
from .models import Module, Resource


class ModuleFilterForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search for courses, exams, TDs, or modules...',
            'class': 'search-input',
            'id': 'search-input',
        })
    )
    level = forms.ChoiceField(
        choices=[('', 'All Levels')] + Module.Level.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'filter-select', 'id': 'filter-level'})
    )
    semester = forms.ChoiceField(
        choices=[('', 'All Semesters')] + Module.Semester.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'filter-select', 'id': 'filter-semester'})
    )
    resource_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Resource.ResourceType.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'filter-select', 'id': 'filter-type'})
    )


class ResourceUploadForm(forms.ModelForm):
    # Step 1 helper fields — not on the model, used to filter modules via AJAX
    level = forms.ChoiceField(
        choices=[('', 'Select Level')] + Module.Level.choices,
        required=True,
        label='Level',
        widget=forms.Select(attrs={'id': 'id_level', 'class': 'form-select'})
    )
    semester = forms.ChoiceField(
        choices=[('', 'Select Semester')] + Module.Semester.choices,
        required=True,
        label='Semester',
        widget=forms.Select(attrs={'id': 'id_semester', 'class': 'form-select'})
    )

    class Meta:
        model  = Resource
        fields = ['module', 'title', 'resource_type', 'academic_year', 'file']
        widgets = {
            'module': forms.Select(attrs={
                'id': 'id_module',
                'class': 'form-select',
                'disabled': 'disabled',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Analyse Complexe — Cours Complet',
            }),
            'resource_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'academic_year': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. 2024',
                'min': 2015,
                'max': 2030,
            }),
            'file': forms.FileInput(attrs={
                'class': 'file-input',
                'accept': '.pdf,.doc,.docx,.ppt,.pptx,.zip',
                'id': 'file-upload',
            }),
        }
        labels = {
            'module':        'Module',
            'title':         'Resource Title',
            'resource_type': 'Resource Type',
            'academic_year': 'Academic Year',
            'file':          'Upload File',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Module queryset starts empty — populated via AJAX
        self.fields['module'].queryset = Module.objects.none()

        if 'level' in self.data and 'semester' in self.data:
            try:
                level    = self.data.get('level')
                semester = self.data.get('semester')
                self.fields['module'].queryset = Module.objects.filter(
                    level=level, semester=semester
                ).order_by('name')
                self.fields['module'].widget.attrs.pop('disabled', None)
            except (ValueError, TypeError):
                pass

    def clean_academic_year(self):
        year = self.cleaned_data.get('academic_year')
        if year and (year < 2015 or year > 2030):
            raise forms.ValidationError('Enter a valid academic year between 2015 and 2030.')
        return year

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            allowed = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip']
            ext = file.name.rsplit('.', 1)[-1].lower()
            if ext not in allowed:
                raise forms.ValidationError(
                    f'Unsupported file type ".{ext}". Allowed: {", ".join(allowed)}'
                )
            if file.size > 50 * 1024 * 1024:
                raise forms.ValidationError('File size must be under 50MB.')
        return file
