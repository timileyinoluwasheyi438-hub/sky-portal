from django import forms
from .models import Team, Department, Engineer,Dependency

class TeamForm(forms.ModelForm):
    new_department_name = forms.CharField(
        max_length=200,
        required=False,
        label="OR Create New Department",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Marketing'})
    )
    new_department_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        label="New Department Description (Optional)"
    )

    class Meta:
        model = Team
        fields = ['name', 'department', 'manager', 'purpose', 'responsibilities',
                  'slack_channel', 'contact_email', 'repo_url', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].required = False

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('department') and not cleaned_data.get('new_department_name'):
            raise forms.ValidationError("Select a department or create a new one.")
        return cleaned_data


class EngineerForm(forms.ModelForm):
    class Meta:
        model = Engineer
        fields = ['name', 'role', 'email']


class DependencyForm(forms.ModelForm):
    class Meta:
        model = Dependency
        fields = ['depends_on']
        widgets = {
            'depends_on': forms.Select(attrs={'class': 'form-control'})
        }