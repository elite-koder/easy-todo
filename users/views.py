from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# from django.http import JsonResponse, HttpResponse

from users.services import UserService

from google.oauth2 import id_token
from google.auth.transport import requests


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            id_info = id_token.verify_oauth2_token(request.POST["credential"], requests.Request(), settings.GOOGLE_CLIENT_ID)
            if not request.session.session_key:
                request.session.create()
            user, _ = UserService().create_user(id_info["email"], id_info["name"], id_info["picture"])
            request.session[SESSION_KEY] = user.id
            request.session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
            request.session[HASH_SESSION_KEY] = "qwerty"
            request.session.modified = True
            return redirect("/easy_todo")
        except ValueError:
            return HttpResponse("Error Occurred!!! Please try again later.")

    elif request.method == "GET":
        if not request.session.session_key:
            request.session.create()
        return render(request, "login.html", {"GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID, "LOGIN_URI": settings.LOGIN_URI})
    raise NotImplementedError


def logout_view(request):
    if request.session:
        request.session.delete()
    return redirect("/login")


def redirect_to_main_page(request):
    return redirect("/easy_todo")
