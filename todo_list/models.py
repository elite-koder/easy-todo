from django.db import models

from base.models import BaseModel
from todo_list.errors import CantDeleteDefaultList
from users.models import User


# Create your models here.
class TodoList(BaseModel):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_lists")
    can_delete = models.BooleanField(default=True)

    class Meta:
        unique_together = ["title", "owner"]

    @classmethod
    def get_todo_lists(cls, owner):
        return list(TodoList.objects.filter(owner=owner).values("id", "title"))

    @classmethod
    def create_todo_list(cls, owner, todo_list_name):
        todo_list, created = TodoList.objects.get_or_create(owner=owner, title=todo_list_name)
        return todo_list.id, created

    @classmethod
    def delete_todo_list(cls, owner, todo_list_id):
        if TodoList.objects.filter(owner=owner, id=todo_list_id, can_delete=False).exists():
            raise CantDeleteDefaultList
        TodoList.objects.filter(owner=owner, id=todo_list_id, can_delete=True).delete()

    @classmethod
    def create_default_list(cls, owner):
        TodoList.objects.get_or_create(owner=owner, title="My Tasks", can_delete=False)

    @classmethod
    def get_default_list_id(cls, owner):
        return TodoList.objects.get(owner=owner, can_delete=False).id

    @classmethod
    def update_new_title(cls, owner, todo_list_id, new_title):
        TodoList.objects.filter(owner=owner, id=todo_list_id).update(title=new_title)
