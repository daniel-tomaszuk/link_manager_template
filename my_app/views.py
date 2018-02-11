from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, login, logout)
from django.views.generic.edit import (FormView, CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views import generic
from django.db.models import F
from .forms import *
from .models import *
import datetime
from django.utils import timezone
from django.utils.text import slugify
import hashlib


class Login(FormView):
    template_name = 'my_app/login.html'
    # form_class in FormView !
    form_class = Login

    def get_success_url(self):
        # find your next url here
        # here method should be GET or POST.
        next_url = self.request.GET.get('next')
        if next_url:
            success_url = next_url
            return success_url  # you can include some query strings as well
        else:
            success_url = reverse_lazy('my_app:login')
            return success_url  # what url you wish to return'

    def form_valid(self, form):
        user_login = form.cleaned_data["login"]
        password = form.cleaned_data["password"]
        user = authenticate(username=user_login, password=password)
        if user is not None:
            login(self.request, user)
        return super(Login, self).form_valid(form)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('my_app:login'))

    def post(self):
        pass


class MainPage(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('my_app:login')
    redirect_field_name = 'next'
    # context_object_name = 'link_list' is set by default
    template_name = "my_app/main_page.html"

    def get_queryset(self):
        return Link.objects.filter(valid=True)\
                           .filter(my_user=self.request.user)


class AddLink(LoginRequiredMixin, CreateView):
    model = Link
    template_name = "my_app/add_link_form.html"
    fields = ["path", "link_password"]

    login_url = reverse_lazy('my_app:login')
    redirect_field_name = 'next'
    success_url = reverse_lazy("my_app:main-page")

    def form_valid(self, form):
        form.instance.my_user = self.request.user
        # get unique slug field
        # generate the slug
        max_length = Link._meta.get_field('slug').max_length
        # generate unique slug
        i = 0
        while True:
            my_slug = slugify(str(self.request.user) + '_'
                              + str(i))[:max_length]
            my_slug = hashlib.sha224(my_slug.encode()).hexdigest()
            # look for unique slug
            if not Link.objects.filter(slug=my_slug).exists():
                break
            i += 1
        form.instance.slug = my_slug
        return super().form_valid(form)


class ShowLink(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('my_app:login')
    redirect_field_name = 'next'
    model = Link  # so context name is given as "link"
    template_name = 'my_app/show_link.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_valid_date = timezone.now() - datetime.timedelta(days=1)
        # get link object from context
        link = get_object_or_404(Link, pk=context['object'].id)
        if last_valid_date < link.creation_date:
            # link still valid, will be displayed
            link.link_displays = F('link_displays') + 1
            link.save()
        else:
            # set valid as False
            link.valid = F('valid') * False
            link.save()
            context['message'] = 'Link not valid. 24h time window has passed.'
        return context
