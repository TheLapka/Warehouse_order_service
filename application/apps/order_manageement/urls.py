from apps.order_manageement import views
from django.urls import path

urlpatterns = [
    path("warehouse/stock/crate_order", view=views.AddProductInOrderView.as_view()),
]