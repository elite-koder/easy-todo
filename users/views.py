from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.shortcuts import render, redirect

from users.services import UserService


# Create your views here.
def login_view(request):
    if request.method == "POST":
        username, password = request.POST["username"], request.POST["password"]
        if username == "admin" and password == "admin":
            if not request.session.session_key:
                request.session.create()
            user, _ = UserService().create_user(request.session.session_key)
            request.session[SESSION_KEY] = user.id
            request.session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
            request.session[HASH_SESSION_KEY] = "qwerty"
            request.session.modified = True
            return redirect("/")
    elif request.method == "GET":
        if not request.session.session_key:
            request.session.create()
        return render(request, "login.html", {})
    raise NotImplementedError


def logout_view(request):
    if request.session:
        request.session.delete()
    return redirect("/login")


def redirect_to_main_page(request):
    return redirect("/easy_todo")
