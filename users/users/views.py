from rest_framework.decorators import *
from rest_framework.permissions import *
from rest_framework.response import Response
from users.users.models import Role
from carts.models import Cart
from .models import *
from .serializers import *
from rest_framework import status
from store.store.models import *
from django.contrib.auth import authenticate


from django.db import transaction


@api_view(["POST"])
def register(request):
    serializer = CustomerUserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            with transaction.atomic():
                role = request.data.get("role", None)
                if role == "ADMIN":
                    user = CustomUser(
                        email=serializer.validated_data["email"],
                        first_name=serializer.validated_data["first_name"],
                        last_name=serializer.validated_data["last_name"],
                        is_admin=True,
                        role=role,
                    )
                else:
                    user = CustomUser(
                        email=serializer.validated_data["email"],
                        first_name=serializer.validated_data["first_name"],
                        last_name=serializer.validated_data["last_name"],
                        role=Role.USER,
                    )

                user.set_password(serializer.validated_data["password"])
                user.save()

                customer = Customer.objects.create(
                    user=user, name=user.first_name, email=user.email
                )
                Cart.objects.create(customer=customer)

            return Response(
                {"message": "User registered successfully, Login to continue..."},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {
                    "error": "Something went wrong. Registration failed.",
                    "details": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if email is None or password is None:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = authenticate(request, email=email, password=password)
    if user is not None:
        token = CustomTokenObtainPairSerializer.get_token(user)

        return Response(
            {
                "refresh": str(token),
                "access": str(token.access_token),
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUsers(request):
    if request.user.role == "ADMIN":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        {"error": "You are not authorized to view the list of users."},
        status=status.HTTP_403_FORBIDDEN,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserById(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.user == user or request.user.role == "ADMIN":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        {"error": "You are not authorized to view this user's details."},
        status=status.HTTP_403_FORBIDDEN,
    )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.user == user:
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {"error": "You are not authorized to update this user's details."},
        status=status.HTTP_403_FORBIDDEN,
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteUser(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.user == user or request.user.role == "ADMIN":
        with transaction.atomic():
            user.delete()
        return Response(
            {"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )

    return Response(
        {"error": "You are not authorized to delete this user."},
        status=status.HTTP_403_FORBIDDEN,
    )
