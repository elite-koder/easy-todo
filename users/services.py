from todo_list.services import TodoListService
from users.models import User


class UserService:
    def login_user(self, l):
        pass

    def logout_user(self):
        pass

    def create_user(self, email, name, dp_link):
        user, created = User.create_user(email, name, dp_link)
        if created:
            TodoListService().create_default_list(user)
        return user, created
