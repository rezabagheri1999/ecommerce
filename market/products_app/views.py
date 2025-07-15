from unicodedata import category

from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.views.generic import ListView

from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from .models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'  # Default: 'object_list'
    paginate_by = 3 # Optional: Add pagination

    def get_queryset(self):
        """Filter active products and apply category filtering."""
        queryset = super().get_queryset().filter(is_active=True)
        sort_option = self.request.GET.get('sort','newest')
        if sort_option == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_option == 'cheapest':
            queryset = queryset.order_by('price')
        elif sort_option == 'most_expensive':
            queryset = queryset.order_by('-price')
        elif sort_option == 'popular':
            queryset = queryset.annotate(num_orders=Count('orders')).order_by('-num_orders')
        #
        # in_stock_only = self.request.GET.get('stock') == True
        # if in_stock_only:
        #     queryset = filter(stock__quantity__gt=0)
        # category_slug = self.kwargs.get('category_slug')
        #
        # if category_slug:
        #     category = get_object_or_404(Category, slug=category_slug)
        #     queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        """Add categories and current category to context."""
        context = super().get_context_data(**kwargs)

        try:
            context['categories'] = Category.objects.all()
        except Exception as e:
            raise ImproperlyConfigured(f"Failed to fetch categories: {e}")

        category_slug = self.kwargs.get('category_slug')
        context['category'] = get_object_or_404(Category, slug=category_slug) if category_slug else None
        context['sort_option'] = self.request.GET.get('sort','newest')
        context['in_stock_checked'] = self.request.GET.get('stock') == True,
        context['newest_products'] = Product.objects.filter(
            is_active=True
        ).order_by('-created_at')[:3]
        return context

def show_newest_products(count=3):
    return {
        'newest_products': Product.objects.filter(
            is_active=True
        ).order_by('-created_at')[:count]
    }

def products_categories_partial(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request,'category_view_partial.html',context)



###################################################################################
###################################################################################
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail_product.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Add additional context data
        context['main_image'] = product.images.filter(is_featured=True).first()
        context['other_images'] = product.images.exclude(id=context['main_image'].id) if context[
            'main_image'] else product.images.all()
        context['related_products'] = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]

        return context