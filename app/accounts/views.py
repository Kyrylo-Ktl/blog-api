"""Module for describing model views"""

from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from .models import User
from .serializers import (
    ResetPasswordConfirmSerializer,
    ResetPasswordEmailRequestSerializer,
    UserSerializer,
)


class UserCreateView(CreateAPIView):
    """
    Allows you to register using your email nickname and password
    """
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    """
    Profile view, displays information about the current user.
    Only for authorized users
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ResetPasswordEmailRequest(GenericAPIView):
    """
    View for a request to send a password reset message to the specified email address.
    """
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.data['email'])
        user.send_password_reset_mail()

        return Response({'success': 'We have sent you a link to reset your password'}, status=HTTP_200_OK)


class ResetPasswordConfirm(GenericAPIView):
    """
    View for updating user password
    """
    serializer_class = ResetPasswordConfirmSerializer

    def get(self, request, uuid, token):
        if User.is_valid_password_reset_token(uuid, token):
            return Response({'success': 'Token is valid, use POST to change password.'}, status=HTTP_200_OK)
        return Response({'error': 'Token is not valid, please request a new one'}, status=HTTP_400_BAD_REQUEST)

    def post(self, request, uuid, token):
        if User.is_valid_password_reset_token(uuid, token):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = User.get_by_uuid(uuid)
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'success': 'Password has been changed successfully.'}, status=HTTP_200_OK)

        return Response({'error': 'Token is not valid, please request a new one'}, status=HTTP_400_BAD_REQUEST)
