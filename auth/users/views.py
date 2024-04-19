import datetime

import jwt
import pytz
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import create_jwt_token
from .models import User
from .serializers import UserSerializer, UserRefreshTokenSerializer, UserDeleteTokenSerializer


@extend_schema(
    summary="API endpoint that allows users to register with email and password",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"}}
        }},
)
class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@extend_schema(
    summary="API endpoint that allows users to login with email and password",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"}}
        }}
)
class LoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        jwt_token = create_jwt_token(user.id)

        serializer = UserRefreshTokenSerializer(data={"refresh_token": None}, instance=user)
        serializer.is_valid()
        serializer.save()

        response = Response()
        # response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'access_token': jwt_token,
            'refresh_token': serializer.data['refresh_token']
        }
        return response


@extend_schema(
    summary="API endpoint that allows users to be viewed or edited",
)
class UserView(APIView):
    """
    For this API endpoint you have to authorize in the upper right corner
    with access token you get when you login. In format "bearer {access_token}"
    """
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # token = request.COOKIES.get('jwt')
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Access token is expired')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def put(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Access token is expired')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(data=request.data, instance=user, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


@extend_schema(
    summary="API endpoint that allows users to logout, after which refresh token will be deleted",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "refresh_token": {"type": "string"}}
        }}
)
class LogoutView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        refresh_token = request.data['refresh_token']
        user = User.objects.filter(refresh_token=refresh_token).first()
        if user is None:
            raise AuthenticationFailed('user not found')

        serializer = UserDeleteTokenSerializer(data=request.data, instance=user)
        serializer.is_valid()
        serializer.save()

        response = Response()
        response.data = {
            'success': 'User logged out.'
        }
        return response


@extend_schema(
    summary="API endpoint that allows users to refresh their tokens",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "refresh_token": {"type": "string"}}
        }}
)
class RefreshView(APIView):
    serializer_class = UserRefreshTokenSerializer

    def post(self, request):
        refresh_token = request.data["refresh_token"]
        user = User.objects.filter(refresh_token=refresh_token).first()
        if user is None:
            raise AuthenticationFailed('user not found')

        exp_date = user.exp_date
        utc = pytz.utc
        if exp_date.replace(tzinfo=utc) < datetime.datetime.utcnow().replace(tzinfo=utc):
            raise AuthenticationFailed('Refresh token is expired')

        serializer = UserRefreshTokenSerializer(data=request.data, instance=user)
        serializer.is_valid()
        serializer.save()

        token = create_jwt_token(user.id)

        response = Response()
        response.data = {
            "access_token": token,
            "refresh_token": serializer.data['refresh_token'],
        }
        return response
