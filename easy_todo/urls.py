"""
URL configuration for easy_todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from todo_item.views import create_todo_item_view, manage_todo_item_view, get_todays_todolist
from todo_list.views import create_todo_list_view, manage_todo_list_view, easy_todo_view
from users.views import login_view, redirect_to_main_page, logout_view

urlpatterns = [
    path("login", login_view, name="login-view"),
    path("logout", logout_view, name="logout-view"),
    path("easy_todo", easy_todo_view, name="easy_todo_view"),
    path("todo_items/todays_list", get_todays_todolist, name="get_todays_todolist"),
    path("todo_items/manage", manage_todo_item_view, name="manage_todo_item_view"),
    path("todo_lists/manage", manage_todo_list_view, name="manage_todo_list_view"),
    path("todo_lists/create", create_todo_list_view, name="create_todo_list_view"),
    path("todo_items/create", create_todo_item_view, name="create_todo_item_view"),
    path("", redirect_to_main_page, name="redirect_to_main_page"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
