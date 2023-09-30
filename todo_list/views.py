import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from todo_item.services import TodoItemService
from todo_list.errors import CantDeleteDefaultList
from todo_list.services import TodoListService


@login_required
def create_todo_list_view(request):
    if request.method == "POST":
        todo_list_name = request.POST["todo_list_name"].strip()
        todo_list_id, created = TodoListService().create_todo_list(request.user, todo_list_name)
        msg = "Hurrah!!! Added New List Successfully."
        error = True
        if not created:
            msg = "Hiss!!! Duplicate List Found."
            error = False
        return JsonResponse({"msg": msg, "error": error, "id": todo_list_id})
    raise NotImplementedError


@login_required
def manage_todo_list_view(request):
    if request.method == "POST":
        try:
            TodoListService().delete_todo_list(request.user, request.POST["todo_list_id"])
            msg = "Hurrah!!! Deleted List Successfully."
            messages.error(request, msg)
            error = False
        except CantDeleteDefaultList:
            msg = "Hiss!!! Can't delete default list"
            messages.error(request, msg)
            error = True

        return JsonResponse({"msg": msg, "error": error})
    raise NotImplementedError


@login_required
def easy_todo_view(request):
    if request.method == "GET":
        selected_todo_list_id = request.GET.get("selected_todo_list_id", "")
        if selected_todo_list_id.isnumeric():
            selected_todo_list_id = int(selected_todo_list_id)
        else:
            selected_todo_list_id = TodoListService().get_default_list_id(request.user)
        todo_items = TodoItemService().get_todo_items(request.user, selected_todo_list_id)
        resp_context = {
            "todo_lists": TodoListService().get_todo_lists(request.user),
            "todo_items": todo_items,
            "selected_todo_list_id": selected_todo_list_id
        }
        return render(request, "easy_todo.html", resp_context)
    raise NotImplementedError
