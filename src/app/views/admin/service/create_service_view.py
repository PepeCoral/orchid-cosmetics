from django.views import View
from django.shortcuts import render, redirect
from app.forms.service.create_service_form import ServiceForm
from django.http import HttpRequest
from app.services.service_service import ServiceService

class CreateServiceView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_service = ServiceService()

    def get(self,request:HttpRequest):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")

        form = ServiceForm()

        return render(request,"admin/services/create.html",{"form":form})
    
    def post(self,request:HttpRequest):
        if request.user.is_anonymous:
            return redirect("/")

        if not request.user.is_superuser:
            return redirect("/")
        
        form = ServiceForm(request.POST)

        if not form.is_valid():
            return render(request,"admin/services/create.html",{"form":form})

        try:
            self.service_service.create_service(request, form.cleaned_data)
            return redirect("admin/cosmeticservices")
        except Exception as e:
            return render(
                request,
                "admin/services/create.html",
                {"form": form, "error": str(e)}
            )