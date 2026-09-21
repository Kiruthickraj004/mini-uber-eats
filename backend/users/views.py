from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from config.rate_limit import is_rate_limited
from rest_framework_simplejwt.views import TokenObtainPairView  # type: ignore[reportMissingImports]


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully",
                    "user_id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                "role": request.user.role,
            }
        )


class RateLimitedTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        ip_address = self.get_client_ip(request)

        key = f"rate:login:{ip_address}"

        if is_rate_limited(
            key=key,
            limit=5,
            window=60,
        ):
            return Response(
                {
                    "code": "RATE_LIMITED",
                    "detail": "Too many login attempts. Try again later.",
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        return super().post(request, *args, **kwargs)

    @staticmethod
    def get_client_ip(request):
        return request.META.get(
            "REMOTE_ADDR",
            "unknown",
        )