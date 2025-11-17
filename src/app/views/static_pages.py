from django.views import View
from django.shortcuts import render

class ContactView(View):
    def get(self, request):
        return render(request, "static/contact.html")