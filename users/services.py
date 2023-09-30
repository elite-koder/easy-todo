from todo_list.services import TodoListService
from users.models import User


class UserService:
    def login_user(self, l):
        pass

    def logout_user(self):
        pass

    def create_user(self, username):
        user, created = User.objects.get_or_create(username=username)
        print(user, user.id, created)
        if created:
            TodoListService().create_default_list(user)
        return user, created
