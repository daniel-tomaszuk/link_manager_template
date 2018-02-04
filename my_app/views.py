from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, login, logout)
from django.views.generic.edit import (FormView, CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from .models import *
import datetime
from django.utils import timezone
from django.utils.text import slugify
import hashlib


class Login(FormView):

    template_name = 'login.html'
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
            success_url = reverse_lazy('login')
            return success_url  # what url you wish to return'

    def form_valid(self, form):
        user_login = form.cleaned_data["login"]
        password = form.cleaned_data["password"]
        user = authenticate(username=user_login, password=password)
        if user is not None:
            login(self.request, user)
        return super(Login, self).form_valid(form)


class Logout(FormView):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('login'))

    def post(self):
        pass


class MainPage(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def get(self, request):
        logged_user = request.user
        user_link_list = Link.objects.filter(valid=True)\
                                     .filter(my_user=logged_user)
        context = {
            'message': 'Main Page',
            'link_list': user_link_list,
        }
        return render(request, 'main_page.html', context)

    def post(self, request):
        pass


class AddLink(LoginRequiredMixin, CreateView):
    model = Link
    template_name = "add_link_form.html"
    fields = ["path", "link_password"]

    login_url = reverse_lazy('login')
    redirect_field_name = 'next'
    success_url = reverse_lazy("main-page")

    def form_valid(self, form):
        form.instance.my_user = self.request.user
        # get unique slug field
        # generate the slug
        max_length = Link._meta.get_field('link_hash').max_length
        # generate unique slug
        i = 0
        while True:
            my_slug = slugify(str(self.request.user) + '_'
                              + str(i))[:max_length]
            my_slug = hashlib.sha224(my_slug.encode()).hexdigest()
            # look for unique slug
            if not Link.objects.filter(link_hash=my_slug).exists():
                break
            i += 1

        form.instance.link_hash = my_slug
        return super().form_valid(form)


class ShowLink(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def get(self, request, slug):
        logged_user = request.user
        link = Link.objects.get(link_hash=slug)
        # # for link in user_links:
        message = 'Link Info Page '
        # check if link is still valid
        last_valid_date = timezone.now() - datetime.timedelta(seconds=60)

        if last_valid_date < link.creation_date:
            # link still valid, will be displayed
            Link.objects.update()
            link.link_displays += 1
            link.save()
            context = {
                'message': message,
                'link': link,
                # 'time': time_seconds,
            }
            return render(request, 'show_link.html', context)
        else:
            link.valid = False
            link.save()
            message = 'Link not valid. 24h time window has passed.'
            context = {
                'message': message,
                # 'time': time_seconds,
            }
            return render(request, 'main_page.html', context)

    def post(self, request):
        pass



