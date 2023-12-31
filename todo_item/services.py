from django.utils import timezone

from todo_item.models import TodoItem


class TodoItemService:
    def create_todo_item(self, owner, todo_desc, target_date, todo_list_id):
        return TodoItem.create_todo_item(owner, todo_desc, target_date, todo_list_id)

    def get_todo_items(self, owner, todo_list_id, todo_item_status):
        return TodoItem.get_todo_items_from_list(owner, todo_list_id, todo_item_status)

    def mark_todo_item_done(self, owner, todo_item_id):
        TodoItem.mark_todo_item_done(owner, todo_item_id)

    def delete_todo_item(self, owner, todo_item_id):
        TodoItem.delete_todo_item(owner, todo_item_id)

    def update_todo_item(self, owner, todo_item_id, desc, todo_list_id, target_date):
        TodoItem.update_todo_item(owner, todo_item_id, desc, todo_list_id, target_date)
