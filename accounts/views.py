# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, TeacherProfileUpdateForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import User
from .models import VideoLink, TeacherProfile
from django.core.mail import EmailMessage
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from .forms import  UserRegisterForm
from django import forms
from .models import CustomUser


from django.core.mail import send_mail






from django.contrib.auth.forms import PasswordResetForm
# Homepage views

def home(request):

	return render(request, 'home.html')


#signup templete view
class SignUpView(TemplateView):
	template_name = 'registration/signup.html'

class RegistrationView(CreateView):
    template_name = 'registration/signup_form.html'
    form_class = UserRegisterForm
    success_url = 'account_activation_sent'
    model = CustomUser

    def form_valid(self, form):
        obj = form.save(commit=False)
        password = obj.set_password(CustomUser.objects.make_random_password())
        obj.is_active = True  # PasswordResetForm won't send to inactive users.
        obj.save()


        # This form only requires the "email" field, so will validate.
        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()  # Must trigger validation
        # Copied from django/contrib/auth/views.py : password_reset
        opts = {
            'use_https': self.request.is_secure(),
            'email_template_name': 'registration/verification.html',
            'subject_template_name': 'registration/verification_subject.txt',
            'request': self.request,
             #'html_email_template_name': provide an HTML content template if you desire.
        }
         #This form sends the email on save()
        reset_form.save(**opts)

        return redirect('home')














# profile view for teacher and maybe for buyer
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = TeacherProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            TeacherProfile.objects.create(**{
                'name' : 'name', 'city': 'city', 'club': 'club', 'url_link': 'url.com', 'desctiption': 'desc'
            })
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = TeacherProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'registration/profile.html', context)













# views for activate account
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')





def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')













#Videos links view
def videolink(request):
    context = {'videos': VideoLink.objects.all()}
    return render(request, 'registrations/videolink.html')

#Add video links for teacher profile
class VideoLinksView(ListView):
    model = VideoLink
    template_name = 'registration/videolink.html'
    #<app>/<model>_<viewstype>
    context_object_name = 'videos'
    ordering = ['-pub_date']


class VideoDetailView(DetailView):
    model = VideoLink
    template_name = 'registration/videolink_detail.html'

class VideoCreateView(LoginRequiredMixin, CreateView):
    model = VideoLink

    template_name = 'registration/videolink_form.html'
    fields = ['title','title_image', 'link_url', 'pub_date', 'short_description']


    def form_valid(self, form):

        form.instance.teacher = self.request.user


        return super().form_valid(form)


class VideoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VideoLink
    fields = ['title', 'title_image', 'link_url', 'pub_date', 'short_description']
    template_name = 'registration/videolink_form.html'

    def form_valid(self, form):
        form.instance.teacher = self.request.user

        return super().form_valid(form)

    def test_func(self):
        video = self.get_object()
        if self.request.user == video.teacher:
            return True
        return False





class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VideoLink
    success_url = '/'
    template_name = 'registration/videolink_confirm_delete.html'

    def test_func(self):
        video = self.get_object()
        if self.request.user == video.teacher:
            return True
        return False
