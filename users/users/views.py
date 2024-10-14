from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from store.store.models import *


@api_view(["POST"])
def register(request):
    serializer = CustomerUserSerializer(data=request.data)
    if serializer.is_valid:
        if serializer.is_valid():
            role = request.data.get("role", None)
            if role == "ADMIN":
                user = CustomUser(
                    email=serializer.validated_data["email"],
                    first_name=serializer.validated_data["first_name"],
                    last_name=serializer.validated_data["last_name"],
                    is_admin=True,
                    role=role,
                )
                user.set_password(serializer.validated_data["password"])
                user.save()
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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
