from django import forms
from .models import Link
from django.contrib.auth import authenticate


class Login(forms.Form):
    login = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean(self):
        # validate the data normally
        super().clean()
        # if more or less than one was given (XOR)
        login = self.cleaned_data['login']
        password = self.cleaned_data['password']
        user = authenticate(username=login, password=password)
        if user is None:
            raise forms.ValidationError('login or password wrong')
        return self.cleaned_data


class AddLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['path', 'file']

    def __init__(self, *args, **kwargs):
        super(AddLinkForm, self).__init__(*args, **kwargs)
        self.fields['path'].required = False
        self.fields['file'].required = False
        # self.fields['path'].help_text = 'Link to secure'

    def clean(self):
        # validate the data normally
        super().clean()
        # if more or less than one was given (XOR)
        link_path = self.cleaned_data['path']
        link_file = self.cleaned_data['file']
        if not ((link_path and not link_file)
           or (not link_path and link_file)):
            raise forms.ValidationError('Fill one and only one of the fields')
        return self.cleaned_data


class GetLinkForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

    # class Meta:
    #     model = Link
    #     fields = ['link_password']
    #
    # def __init__(self, *args, **kwargs):
    #     super(GetLinkForm, self).__init__(*args, **kwargs)
    #     self.fields['link_password'].label = 'Password'


class SelectContentForm(forms.Form):
    slug = forms.SlugField(max_length=128)
