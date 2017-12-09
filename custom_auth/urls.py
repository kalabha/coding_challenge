
from django.conf.urls import url
from django.urls import include

from custom_auth import api
from . import views

app_name = "custom_auth"

urlpatterns = [

    url(r'^api/', include([
        url(r'^sign_up/$', api.CreateUser.as_view()),
        url(r'^otp_verification/$', api.OtpVerification.as_view()),
        url(r'^request_otp/$', api.request_for_otp),
        url(r'^logout/$', api.api_logout),

    ])),
    url(r'^sign_up/$', views.sign_up, name="sign_up"),
    url(r'^login/$', views.userlogin, name="login"),
    url(r'^verify_otp/$', views.verify_otp, name="verify_otp"),
    url(r'^logout/$', views.userlogout, name="logout"),
    url(r'$', views.index, name="index"),




]
