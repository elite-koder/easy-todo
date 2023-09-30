from todo_list.models import TodoList


class TodoListService:
    def get_todo_lists(self, owner):
        return TodoList.get_todo_lists(owner)

    def create_todo_list(self, owner, todo_list_name):
        return TodoList.create_todo_list(owner, todo_list_name)

    def delete_todo_list(self, owner, todo_list_id):
        TodoList.delete_todo_list(owner, todo_list_id)

    def create_default_list(self, owner):
        TodoList.create_default_list(owner)

    def get_default_list_id(self, owner):
        return TodoList.get_default_list_id(owner)
