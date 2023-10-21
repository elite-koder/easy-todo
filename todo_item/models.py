from django.db import models
from django.db.models import F
from django.utils import timezone

from base.models import BaseModel
from todo_list.models import TodoList
from users.models import User


class TodoItemStatus(models.TextChoices):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


# Create your models here.
class TodoItem(BaseModel):
    desc = models.CharField(max_length=250)
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="todo_items")
    status = models.CharField(max_length=50, choices=TodoItemStatus.choices, default=TodoItemStatus.OPEN)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_items")
    target_date = models.DateField()

    @classmethod
    def create_todo_item(cls, owner, todo_desc, target_date, todolist_id):
        return cls.objects.get_or_create(desc=todo_desc, owner=owner, target_date=timezone.make_aware(target_date, timezone.get_default_timezone()), todo_list_id=todolist_id)

    @classmethod
    def get_todo_items_from_list(cls, owner, todo_list_id, todo_item_status):
        todo_items = cls.objects.filter(owner=owner, todo_list_id=todo_list_id)
        if todo_item_status == TodoItemStatus.OPEN:
            todo_items = todo_items.filter(status=todo_item_status)
        todo_items = todo_items.order_by("target_date").values("id", "desc", "status", "target_date")
        for item in todo_items:
            item["target_date"] = item["target_date"].strftime("%d/%m/%Y")
        return todo_items

    @classmethod
    def mark_todo_item_done(cls, owner, todo_item_id):
        cls.objects.filter(owner=owner, id=todo_item_id).update(status=TodoItemStatus.CLOSED)

    @classmethod
    def delete_todo_item(cls, owner, todo_item_id):
        cls.objects.filter(owner=owner, id=todo_item_id).delete()
