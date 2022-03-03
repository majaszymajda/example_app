from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.filters import UserFilters
from users.pagination import PostLimitOffsetPagination
from users.permissions import IsOwner, IsOwnerOrIsAdminOrReadOnly
from users.serializers import (
    UserLoginSerializer,
    UserPasswordUpdateSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserCreateSerializer,
)
from users.models import User


class UserViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    action_serializers = {
        "update_password": UserPasswordUpdateSerializer,
        "update": UserUpdateSerializer,
    }

    action_permissions = {
        "update": [IsAdminUser],
        "create": [AllowAny],
    }

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PostLimitOffsetPagination

    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=["PUT"],
        name="password-update",
        url_path="password",
        permission_classes=[IsOwner],
    )
    def update_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            data={"message": "Hasło zostało zmienione"}, status=status.HTTP_200_OK
        )


class RegisterAPIView(CreateAPIView):

    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class LoginAPIView(CreateAPIView):

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            token = serializer.create(user)

            return Response(
                {
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "token": token,
                }
            )
        except BaseException:
            return Response(
                data={"message": "Logowanie zakończyło się niepowodzeniem."},
                status=status.HTTP_400_BAD_REQUEST,
            )

