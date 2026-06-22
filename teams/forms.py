from django import forms
from .models import Team, Department

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'department', 'manager', 'purpose', 'responsibilities',
                  'slack_channel', 'contact_email', 'repo_url', 'status']
        widgets = {
            'purpose': forms.Textarea(attrs={'rows': 3}),
            'responsibilities': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            widget = self.fields[field].widget
            if isinstance(widget, forms.Select):
                widget.attrs.update({'class': 'form-select'})
            else:
                widget.attrs.update({'class': 'form-control'})

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})