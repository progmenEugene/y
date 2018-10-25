Well, I understand you. I can do it.
#forms
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email']






#views


#signup teacher views
def teacher_signin(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            email = form.cleaned_data.get('email')
            user.save()
            messages.success(request, 'Account created for %s' %(email))

            current_site = get_current_site(request)
            mail_subject = 'Activate YogaWithPro account %s ' %(email)
            message = render_to_string('registration/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),


            })
            emails = form.cleaned_data.get('email')
            user.email(EmailMessage(mail_subject, message, to=[email]))
            user.email.send()
            return redirect('accounts_activation_sent')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup_form.html', {'form': form})

