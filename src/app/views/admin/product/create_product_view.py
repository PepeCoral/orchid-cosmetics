from django.views import View
from django.shortcuts import render, redirect
from app.forms.product.create_product_form import CreateProductForm
from app.services.product_service import ProductService
class CreateProductView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def get(self, request):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        form = CreateProductForm()
        return render(request, "admin/products/create.html", {"form": form})

    def post(self, request):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        form = CreateProductForm(request.POST)

        if not form.is_valid():
            return render(request, "admin/products/create.html", {"form": form})

        try:
            self.product_service.create_product(request, form.cleaned_data)
            return redirect("admin/products")
        except Exception as e:
            return render(
                request,
                "admin/products/create.html",
                {"form": form, "error": str(e)}
            )
