
"""
URL configuration for trustvault project.
"""

from django.contrib import admin
from django.urls import path

from vault import views


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Home and authentication
    path("", views.home, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Document management
    path(
        "documents/upload/",
        views.upload_document,
        name="upload_document",
    ),
    path(
        "documents/<int:document_id>/download/",
        views.download_document,
        name="download_document",
    ),

    # Document permissions
    path(
        "documents/<int:document_id>/permissions/grant/",
        views.grant_permission,
        name="grant_permission",
    ),
    path(
        "documents/<int:document_id>/permissions/<int:user_id>/revoke/",
        views.revoke_permission,
        name="revoke_permission",
    ),
]

