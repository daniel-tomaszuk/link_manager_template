from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, login, logout)
from django.views.generic.edit import (FormView, CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.static import serve
from django.http import Http404
from django.db.models import F

# REST API
from .serializers import InfoSerializer, ContentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
##

from .forms import *
from .models import *
import datetime
from django.utils import timezone
from django.utils.text import slugify
import hashlib
import random
import os


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

    def post(self, request):
        pass


class MainPage(LoginRequiredMixin, generic.FormView):
    login_url = reverse_lazy('my_app:login')
    redirect_field_name = 'next'
    template_name = "my_app/main_page.html"
    form_class = SelectContentForm

    def form_valid(self, form):
        slug = form.cleaned_data['slug']
        link = get_object_or_404(Link, slug=slug)
        if link.is_valid:
            self.success_url = reverse_lazy('my_app:get-link', args=[slug])
        else:
            self.success_url = Http404
        return super(MainPage, self).form_valid(form)


# class MainPage(LoginRequiredMixin, generic.ListView):
#     login_url = reverse_lazy('my_app:login')
#     redirect_field_name = 'next'
#     # context_object_name = 'link_list' is set by default
#     template_name = "my_app/main_page.html"
#
#     def get_queryset(self):
#         return Link.objects.filter(valid=True)\
#                            .filter(my_user=self.request.user)


class AddLink(LoginRequiredMixin, CreateView):
    model = Link
    form_class = AddLinkForm
    # form_class.use_required_attribute = False
    template_name = "my_app/add_link_form.html"
    # redirects to login
    login_url = reverse_lazy('my_app:login')
    redirect_field_name = 'next'

    def get_success_url(self):
        # redirect by slug of the new created object
        return reverse_lazy('my_app:show-link', args=[self.object.slug])

    def form_valid(self, form):
        # validate the form, add slug and password to the object
        form.instance.my_user = self.request.user
        # get unique slug field
        # generate the slug
        max_slug_length = Link._meta.get_field('slug').max_length
        # max_password_length = Link._meta.get_field('link_password').max_length
        # generate unique slug and password
        i = 0
        while True:
            my_slug = slugify(str(self.request.user) + '_'
                              + str(i))[:max_slug_length]
            my_slug = hashlib.sha224(my_slug.encode()).hexdigest()
            # as example - take 10 random from slug
            my_password = ''.join([random.choice(my_slug) for i in range(10)])
            # look for unique slug
            if not Link.objects.filter(slug=my_slug).exists():
                break
            i += 1
        form.instance.slug = my_slug
        form.instance.link_password = my_password
        return super(AddLink, self).form_valid(form)


class ShowLink(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('my_app:login')
    redirect_field_name = 'next'
    model = Link  # so context name is given as "link"
    template_name = 'my_app/show_link.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get link object from context
        link = get_object_or_404(Link, pk=context['object'].id)
        if not link.is_valid:
            context['message'] = 'Link not valid. 24h time window has passed.'
        return context


class GetLink(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('my_app:login')
    redirect_field_name = 'next'
    model = Link
    template_name = 'my_app/get_link.html'
    form_class = GetLinkForm

    def form_valid(self, form):
        password = form.cleaned_data["password"]
        link = get_object_or_404(Link, slug=self.kwargs['slug'])
        # get Link object and check passwords
        if not password == link.link_password:
            form.add_error(None, ValidationError('Wrong password',
                                                 code='invalid'))
            return self.form_invalid(form)
        return super(GetLink, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_app:give-content', args=[self.kwargs['slug']])


class GiveLink(LoginRequiredMixin, View):
    login_url = reverse_lazy('my_app:login')
    redirect_field_name = 'next'

    def get(self, request, slug):
        link = Link.objects.get(slug=slug)
        if link.is_valid:
            link.link_displays = F('link_displays') + 1
            link.save()
            if link.path:
                return redirect(link.path)
            elif link.file:
                return serve(request, os.path.basename(str(link.file)),
                             os.path.dirname(str(link.file)))
        else:
            return Http404('Content not found')

    def post(self, request):
        pass


class InfoList(generics.ListAPIView):
    queryset = Link.objects.all()
    serializer_class = InfoSerializer


class AddContent(generics.CreateAPIView):
    queryset = Link.objects.all()
    serializer_class = ContentSerializer
