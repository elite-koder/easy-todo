import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from todo_item.services import TodoItemService
from todo_list.services import TodoListService


@login_required
def get_todays_todolist(request):
    page = "todays_todo"
    if request.method == "GET":
        todo_items = TodoItemService().get_todays_todo_items(request.user)
        resp_context = {"todo_items": todo_items, "page": page}
        return render(request, "todays_todolist.html", resp_context)


@login_required
def create_todo_item_view(request):
    if request.method == "POST":
        todo_desc = request.POST["todo_desc"]
        target_date = timezone.datetime.strptime(request.POST["todo_target_date"], "%d/%m/%Y")
        todo_list_id = request.POST["todo_list_id"]
        _, created = TodoItemService().create_todo_item(request.user, todo_desc, target_date, todo_list_id)
        if not created:
            msg = "Hiss!!! Found Duplicate"
            error = True
            code = 400
        else:
            msg = "Hurrah!!! Todo Item added successfully"
            error = False
            code = 200
        return JsonResponse({"msg": msg, "error": error}, status=code)
    raise NotImplementedError


@login_required
def manage_todo_item_view(request):
    if request.method == "POST":
        todo_item_id = request.POST["todo_item_id"]
        op = request.POST["op"]
        if op == "DONE":
            TodoItemService().mark_todo_item_done(request.user, todo_item_id)
            return HttpResponse(status=200)
        elif op == "DELETE":
            TodoItemService().delete_todo_item(request.user, todo_item_id)
            return HttpResponse(status=204)
    raise NotImplementedError
