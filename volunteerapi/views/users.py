from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from ..models import Organization, Volunteer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email"]
        extra_kwargs = {"password": {"write_only": True}}


class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ["phone_number", "location"]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name", "description", "location"]


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"], url_path="register")
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_type = None
            if "volunteer" in request.data:
                user_type = "volunteer"
            elif "organization" in request.data:
                user_type = "organization"

            is_staff = user_type == "organization"

            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                password=serializer.validated_data["password"],
                email=serializer.validated_data["email"],
                is_staff=is_staff,
            )

            if user_type == "volunteer":
                volunteer_serializer = VolunteerSerializer(
                    data=request.data["volunteer"]
                )
                if volunteer_serializer.is_valid():
                    volunteer_serializer.save(user=user)

            if user_type == "organization":
                organization_serializer = OrganizationSerializer(
                    data=request.data["organization"]
                )
                if organization_serializer.is_valid():
                    organization_serializer.save(user=user)

            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="login")
    def user_login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token = Token.objects.get(user=user)
            return Response(
                {"token": token.key, "valid": True}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
