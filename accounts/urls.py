
from django.urls import path, include
from .views import VideoLinksView, VideoDetailView, VideoCreateView, VideoUpdateView, VideoDeleteView
from . import views

urlpatterns = [
	path('accounts/profile/', views.profile, name = 'profile'),
	path('accounts/profile/videos/', VideoLinksView.as_view(), name = 'videolink' ),
	path('accounts/profile/videos/<int:pk>/', VideoDetailView.as_view(), name = 'videodetail'),
	path('accounts/profile/videos/new/', VideoCreateView.as_view(), name ='videocreate'),
	path('accounts/profile/videos/<int:pk>/update/', VideoUpdateView.as_view(), name ='videoupdate'),
	path('accounts/profile/videos/<int:pk>/delete/', VideoDeleteView.as_view(), name = 'videodelete'),



	path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/signup/', views.SignUpView.as_view(), name = 'signup'),
	#path('accounts/signup/buyer/', views.BuyerSignUpView.as_view(), name='buyer_signup'),# need create buyer
	path('accounts/signup/teacher/', views.RegistrationView.as_view(), name = 'teacher_signup'),
	path('account_activate_sent/', views.account_activation_sent, name = 'account_activation_sent'),
	path('activate/?P<uidb64>[0-9A-Za-z_\-]+/?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}/', views.activate, name='activate'),


]