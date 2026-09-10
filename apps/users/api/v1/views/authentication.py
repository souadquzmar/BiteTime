from rest_framework import generics
from rest_framework.permissions import AllowAny
from apps.users.api.v1.serializers.authentication import RegisterSerializer
from apps.users.models import User


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
