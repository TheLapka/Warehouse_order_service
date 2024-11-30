from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.GetAllProductsView.as_view()),
    path("<int:pk>", view=views.RetrieveUpdateDeleteProductView.as_view()),
    path("create/", view=views.CreateProductView.as_view()),
    path("stock/add_or_update", view=views.AddProductInWarehouseView.as_view()),
    path("stock/", view=views.GetAllProductsInWarehouseView.as_view()),
    path("stock/<int:pk>", view=views.GetProductInWarehouseView.as_view()),
]
