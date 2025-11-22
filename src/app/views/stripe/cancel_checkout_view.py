from django.views import View
from django.shortcuts import render,redirect
from django.http import HttpRequest
import stripe

class CancelCheckoutView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get(self,request:HttpRequest):
        session_id = request.GET.get("session_id")
        if not session_id:
            return redirect("/", {"message": "No se encontró la sesión"})
        
        session = stripe.checkout.Session.retrieve(session_id)
       
        return render(request, "checkout/cancel.html")