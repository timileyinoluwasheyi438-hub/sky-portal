from django import forms
from .models import Team, Department
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
        self.fields['department'].required = False   # ← This is the key fix

    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department')
        new_name = cleaned_data.get('new_department_name')

        if not department and not new_name:
            raise forms.ValidationError("You must either select a department or create a new one.")
        
        return cleaned_data


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})