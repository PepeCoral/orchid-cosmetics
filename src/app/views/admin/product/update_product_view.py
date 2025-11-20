from django.views import View
from django.shortcuts import render, redirect
from app.forms.product.update_product_form import UpdateProductForm
from app.services.product_service import ProductService

class UpdateProductView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def get(self, request, product_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        product = self.product_service.get_product_by_id(product_id)
        form = UpdateProductForm(instance=product)

        return render(request, "admin/products/update.html", {
            "form": form, 
            "product": product  # ← Añade el producto al contexto
        })

    def post(self, request, product_id):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        # Obtener el producto primero
        product = self.product_service.get_product_by_id(product_id)
        

        form = UpdateProductForm(request.POST, request.FILES, instance=product)

        if not form.is_valid():
            return render(request, "admin/products/update.html", {
                "form": form, 
                "product": product,
                "error": "Por favor, corrige los errores del formulario."
            })

        try:

            form.save()
            return redirect(f"/admin/products/{product_id}")
        except Exception as e:
            return render(
                request,
                "admin/products/update.html",
                {
                    "form": form, 
                    "product": product,
                    "error": str(e)
                }
            )