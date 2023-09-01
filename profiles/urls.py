from django.urls import path,include,re_path
from . import views

urlpatterns = [
    path('setlang/<str:lang>/',views.set_lang),
    path('profile/order/cancel/<int:oid>/',views.cancel_order),
    path('profile/edit_profile/',views.edit_profile),
    path('profile/<str:info>/',views.profile),
    path('profile/',views.profile,),
    
    path('',views.index),
    path('register/',views.RegistrationForm),
    path('accounts/login/',views.login_view),
    path('register/accounts/login/',views.login_view),
    path('accounts/logout/',views.logout_view),
    path('distance',views.find_distance),
    path('qr/<str:key>',views.qr_login),
    path('password-reset/', views.password_reset_request),
    path('reset/done/accounts/login',views.login_view),
    path('profile/download/qr/',views.download_qr),
    path('profile/send_mail/qr/',views.qr_mail),
    path('market_price/',views.market_price),
    
    
]


'''
urlpatterns = [
    path('order/cancel/<int:oid>/',views.cancel_order),
    path('edit_profile/',views.edit_profile),
    path('<str:info>/',views.profile),
    path('',views.profile,name='profile'),
    
]
'''