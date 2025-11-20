from django.views import View
from django.shortcuts import render
from app.services.product_service import ProductService
from app.forms.catalog.search_catalog_form import SearchCatalogForm
from app.models import Category

class ProductCatalogView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def get(self, request):
        products = self.product_service.get_all_products()
        categories = Category.objects.all()

        return render(request, "catalog/product_catalog.html", {
            "products": products,
            "categories": categories,
            "form": SearchCatalogForm(),
        })

    def post(self, request):
        # Inicializar variables
        products = self.product_service.get_all_products()
        categories = Category.objects.all()
        
        # Contexto base
        context = {
            "products": products,
            "categories": categories,
            "form": SearchCatalogForm(),
        }
        
        # Obtener parámetros de productos
        product_name = request.POST.get('product_name', '')
        product_fabricator = request.POST.get('product_fabricator', '')
        product_min_price = request.POST.get('product_min_price', '')
        product_max_price = request.POST.get('product_max_price', '')
        selected_product_categories = request.POST.getlist('product_categories', [])
        
        # Agregar al contexto para mantener valores en el formulario
        context.update({
            'product_name': product_name,
            'product_fabricator': product_fabricator,
            'product_min_price': product_min_price,
            'product_max_price': product_max_price,
            'selected_product_categories': [int(cat) for cat in selected_product_categories if cat],
            'product_filters_active': any([product_name, product_fabricator, product_min_price, product_max_price, selected_product_categories])
        })
        
        # Construir filtros compatibles con ProductRepository
        filters = {}
        if product_name:
            filters['name'] = product_name
        if product_fabricator:
            filters['fabricator'] = product_fabricator
        if product_min_price:
            try:
                filters['min_price'] = float(product_min_price)
            except ValueError:
                pass
        if product_max_price:
            try:
                filters['max_price'] = float(product_max_price)
            except ValueError:
                pass
        if selected_product_categories:
            filters['categories'] = selected_product_categories
        
        # Aplicar filtros si hay alguno
        if filters:
            try:
                products = self.product_service.search_products(filters)
                context['products'] = products
            except Exception as e:
                context['error'] = f"Error al filtrar productos: {str(e)}"

        return render(request, "catalog/product_catalog.html", context)