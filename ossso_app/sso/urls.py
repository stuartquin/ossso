from django.urls import path
from sso import views

urlpatterns = [
    path("acs/<str:guid>/", views.sso_acs, name="sso-acs"),
    path("signin/<str:guid>/", views.signin, name="sso-signin"),
]
