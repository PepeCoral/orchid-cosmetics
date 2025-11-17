from django.views import View
from django.shortcuts import render


class HomeView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):
        return render(request, "home.html")
