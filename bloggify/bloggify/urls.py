"""
URL configuration for bloggify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static
from articles import views as articles_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', articles_views.guest_home_view),
    path('bloggify/', articles_views.guest_home_view, name='guest-home'),
    path('guest-post-details/', articles_views.guest_post_details_view, name='guest-post-details'),
    path('register/', accounts_views.register_view, name='register'),
    path('login/', accounts_views.login_view, name='login'),
    path('home/', articles_views.home_view, name='home'),
    path('post-details/', articles_views.post_details_view, name='post-details'),
    path('like-post/', articles_views.like_post_view, name='like-post'),
    path('create-post/', articles_views.create_post_view, name='create-post'),
    path('view-posts/', articles_views.posts_view, name='view-posts'),
    path('edit-post/', articles_views.edit_post_view, name='edit-post'),
    path('delete-post/', articles_views.delete_post_view, name='delete-post'),
    path('add-comment/', articles_views.add_comment_view, name='add-comment'),
    path('profile/', accounts_views.profile_view, name='profile'),
    path('editprofile/', accounts_views.edit_profile_view, name='editprofile'),
    path('change-password/', accounts_views.change_password_view, name='change-password'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('reset-password/', accounts_views.reset_password_view, name='reset-password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
