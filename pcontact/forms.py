from django import forms
from .models import Tags,Contacts,CompanyAssociation,InsttitueAssociation
from django.contrib.auth.models import User

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields="__all__"

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['company'].queryset = CompanyAssociation.objects.all()
        self.fields['institute'].queryset = InsttitueAssociation.objects.all()
        self.fields['tags'].queryset = Tags.objects.all()
        self.fields['connection'].help_text = ""
        self.fields['connection'].queryset = User.objects.filter(is_superuser=True)
        cho = (('Angel', 'Angel'), ('Expert', 'Expert'), ('GP', 'GP'), ('LP', 'LP'))
        self.fields['role'] = forms.MultipleChoiceField(choices=cho, widget=forms.CheckboxSelectMultiple())

class CompanyAssociationForm(forms.ModelForm):
    year = forms.CharField(label='Start - End Year',widget=forms.TextInput(attrs={'placeholder':'Jan 2015 - Sep 2017'}), required=False)
