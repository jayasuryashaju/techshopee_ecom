from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('user_registration', views.register, name="user_registration"),
    path('user_signin', views.login_user, name="user_signin"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('user_signout', views.user_signout, name="user_signout"),
    path('login_otp', views.login_otp, name="login_otp"),
    path('verify_otp', views.verify_otp, name="verify_otp"),

]
