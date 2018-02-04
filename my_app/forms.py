from django import forms


class Login(forms.Form):
    login = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class AddLinkForm(forms.Form):
    link_path = forms.CharField(label='Link:', max_length=128)
    link_password = forms.CharField(label='Link password:', max_length=128)

















