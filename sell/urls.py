from django.urls import path,include,re_path
from . import views
from profiles import views as p_views

urlpatterns = [
    path('accounts/logout',p_views.logout_view),
    path('addproduct/',views.add_product),
    path('orders/addproduct',views.add_product),
    path('products/addproduct',views.add_product),
    path('order/<int:oid>/<str:stat>/',views.order_status,name='orders'),
    path('product/order/<int:pid>/',views.order),
    path('<str:type>/',views.orders),
    path('product/price_change/<int:pid>',views.price_change,name='order'),
    path('product/price_change',views.price_change),
    path('product/remove/<int:pid>',views.remove_product),
    path('',views.orders),
]


'''
urlpatterns = [
    path('accounts/logout',p_views.logout_view),
    path('addproduct/',views.add_product),
    path('orders/addproduct',views.add_product),
    path('products/addproduct',views.add_product),
    path('order/<int:oid>/<str:stat>/',views.order_status,name='orders'),
    path('product/order/<int:pid>/',views.order),
    path('<str:type>/',views.orders),
    path('product/price_change/<int:pid>',views.price_change,name='order'),
    path('product/price_change',views.price_change),
    path('product/remove/<int:pid>',views.remove_product),
    path('',views.orders),
]
'''