
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.email





















#This is teacher profile! after that need to add buyer profile! and add type of profile is_buyer is_teacher
class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name = 'profile')
    email_confirmed = models.BooleanField(default = False)

    image = models.ImageField(upload_to='profile/')
    name = models.CharField(max_length=255, default = 'name')
    city = models.CharField(max_length=255, default = 'city')
    club = models.CharField(max_length=255, default = 'club')
    url_youtube = models.URLField(max_length=255, default = 'url.com')
    description = models.TextField(default = 'some text')

    def __str__(self):
        return self.user.email


    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'



CustomUser.profile = property(lambda u: TeacherProfile.objects.get_or_create(user=u)[0])









class VideoLink(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255, verbose_name = 'Заголовок', null=True)
    short_description = models.TextField(verbose_name = 'Кратко описание', null=True)
    title_image = models.ImageField(upload_to = 'videolinks/', verbose_name = 'Картинка', null=True)
    link_url = models.URLField(max_length = 255, verbose_name = 'Ссылка на видео', null=True)
    pub_date = models.DateTimeField(verbose_name = 'Дата публикации', null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('videodetail', kwargs={'pk': self.pk})


