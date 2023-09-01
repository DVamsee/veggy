"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static  
from django.contrib import admin
from django.urls import path,include,re_path

from django.contrib.auth import views as auth_views


from profiles.views import (
    RegistrationForm,
    login_view,
    index,
    logout_view,
    qr_login,
    find_distance,
    qr_login,
    password_reset_request,
    
    qr_mail,
    base,
)

from django.conf.urls.i18n import i18n_patterns
from sell.views import add_product

urlpatterns = [
   
    #path('contact/',contact),
    #re_path(r'qr_login/(?P<key>\w+)/$',qr_login),
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/login/register/',RegistrationForm),
    #path('accounts/register/login/',login_view),
    
    #mail
    path('admin/', admin.site.urls),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="pages/reset-pasword.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='pages/password-reset-complete.html'), name='password_reset_complete'),   
    
    
    #path('qrmail/',qrmail),
    
    #sell
    path('',include('profiles.urls')),
    path('sell/',include('sell.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    
    
    #sample
    path('base/',base),
]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
        
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]


urlpatterns += i18n_patterns(
    
    
    #re_path(r'qr_login/(?P<key>\w+)/$',qr_login),
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/login/register/',RegistrationForm),
    #path('accounts/register/login/',login_view),
    path('admin/', admin.site.urls),
    #mail
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="pages/reset-pasword.html"),),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='pages/password-reset-complete.html'),),   
   
    
    #path('qrmail/',qrmail),
    
    #sell
    path('',include('profiles.urls')),
    path('sell/',include('sell.urls')),
    
    
   
    
    
    
)
