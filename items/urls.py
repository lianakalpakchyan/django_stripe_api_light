from django.urls import path

from . import views

urlpatterns = [
    path("", views.ItemListView.as_view(), name="item_list"),
    path("item/<int:item_id>", views.ItemDetailView.as_view(), name="item"),
    path('order', views.OrderAPIDetailView.as_view(), name='order'),
    path('orderitem/<int:pk>', views.OrderItemAPIDetailView.as_view(), name='orderitem'),
    path('discount_list', views.DiscountList.as_view(), name='discount_list'),
    path('tax_list', views.TaxList.as_view(), name='tax_list'),
    path("buy", views.buy, name='buy'),
    path("success", views.SuccessView.as_view(), name="success"),
]
