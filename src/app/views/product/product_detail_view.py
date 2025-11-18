from django.views import View
from django.shortcuts import render, redirect
from app.services.product_service import ProductService
from app.forms.product.buy_product_form import BuyProductForm

class ProductDetailView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def get(self, request, product_id):
        product = self.product_service.get_product_by_id(product_id)
        categories = product.categories.all()
        
        # Pasar el stock máximo al formulario
        form = BuyProductForm(max_stock=product.stock)
        
        return render(request, "product/detail.html", {
            "form": form, 
            "product": product,
            "categories": categories
        })

    def post(self, request, product_id):
        if request.user.is_anonymous:
            return redirect("/login")

        product = self.product_service.get_product_by_id(product_id)
        categories = product.categories.all()
        
        # Pasar el stock máximo al formulario
        form = BuyProductForm(request.POST, max_stock=product.stock)

        if not form.is_valid():
            return render(request, "product/detail.html", {
                "form": form, 
                "product": product,
                "categories": categories
            })

        try:
            # Aquí procesas la compra
            quantity = form.cleaned_data['quantity']
            # Tu lógica para añadir al carrito...
            
            return redirect("/cash")
        except Exception as e:
            return render(
                request,
                "product/detail.html",
                {
                    "form": form, 
                    "error": str(e), 
                    "product": product,
                    "categories": categories
                }
            )
