from . import views
from django.contrib import admin
from django.urls import path, include
app_name = 'partyapp'
urlpatterns = [
    path('', views.addparty, name='addparty'),
    path('add_party/', views.add_party, name='add_party'),
    path('SaleItem',views.saleitem,name='saleitem'),
    path('sale_item', views.sale_item, name='sale_item'),
    path('PurchaseItem', views.purchaseitem, name='purchaseitem'),
    path('purchase_item', views.purchase_item, name='purchase_item'),

]