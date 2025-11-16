from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
import json
from app.models import User
from app.services.user_service import UserService
from app.forms.user_register_form import UserRegisterForm

def profile(request):
    items = User.objects.all()
    return render(request, "profile.html", {'users': items})

@csrf_exempt
@require_http_methods(["POST", "GET"])
def register(request: HttpRequest):

    if not request.user.is_anonymous:
        return redirect("/profile")

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            validate_access = UserService.get_user_by_username(username=username)
            if validate_access is not None:
                return render(request, "register.html", {'usernameAlreadyUse': True, "form":form})
            user = UserService.create_user(form.cleaned_data)
            auth_login(request=request,user=user)
            return redirect("/profile",  "register.html",)
        else:
            return render(request,"register.html",context={"form":form})

    form = UserRegisterForm()
    print(form)
    return render(request,template_name="register.html",context={"form":form})
@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    # try:
        # Obtener datos del request
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()

        print(data)
        email = data['email']
        password = data['password']


    # Autenticar usuario
        user = UserService.authenticate_user(request,email, password)

    # Realizar login
        auth_login(request, user)
        return redirect("/profile")


    # except ValidationError as e:
    #     return JsonResponse({
    #         'success': False,
    #         'error': str(e)
    #     }, status=401)
    # except Exception as e:
    #     return JsonResponse({
    #         'success': False,
    #         'error': str(e)
    #     }, status=500)


@require_http_methods(["POST", "GET"])
@login_required(login_url="/account/login")
def logout(request):
    auth_logout(request)
    return redirect("/")
