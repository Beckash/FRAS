from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()

class EmailBackEnd(ModelBackend):
    def authenticate(self, request, username=None, password=None, user_type=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Check if username contains @ (email)
            if '@' in username:
                user = UserModel.objects.get(email=username)
            else:
                user = UserModel.objects.get(username=username)
            
            if user.check_password(password):
                # Set backend path on user
                user.backend = 'facial_recognition_based__attendance_system_app.EmailBackEnd.EmailBackEnd'
                return user
        except UserModel.DoesNotExist:
            # Try with email field if username doesn't work
            try:
                user = UserModel.objects.get(email=username)
                if user.check_password(password):
                    user.backend = 'facial_recognition_based__attendance_system_app.EmailBackEnd.EmailBackEnd'
                    return user
            except UserModel.DoesNotExist:
                return None
        return None