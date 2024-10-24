from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from volunteerapi.views import (
    UserViewSet,
    OpportunityViewSet,
    ProfileViewSet,
    SkillViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"opportunities", OpportunityViewSet, "opportunity")
router.register(r"profile", ProfileViewSet, "profile")
router.register(r"skills", SkillViewSet, "skill")

urlpatterns = [
    path("", include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path(
        "register", UserViewSet.as_view({"post": "register_account"}), name="register"
    ),
]
