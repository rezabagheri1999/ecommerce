from django.urls import path
from .views import ProductListView,products_categories_partial,ProductDetailView

app_name = 'products_app'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='products'),
    path('products/products_categories_partial', products_categories_partial, name='products_categories_partial'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    # path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    # path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]