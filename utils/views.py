from rest_framework import views


class CustomApiView(views.APIView):

    def get_current_user(self):
        user = self.request.user
        if user.is_staff:
            from user.models import User
            user_id = self.request.GET.get('user_id')
            user_from_get = User.objects.filter(id=user_id).first()
        return user
