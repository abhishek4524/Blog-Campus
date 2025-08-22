from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views  # Import auth_views for login/logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:post_id>/', views.full_blog, name='full_blog'),
    path('<int:post_id>/edit/', views.blog_edit, name='blog_edit'),
    path('<int:post_id>/delete/', views.blog_delete, name='blog_delete'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Add this for login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout
    path('accounts/profile/', views.profile, name='profile'),

    
    
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)