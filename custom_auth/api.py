from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout as auth_logout


from custom_auth.models import Otp
from custom_auth.serializer import CustomAuthSerializer, OtpSerializer
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class CreateUser(generics.CreateAPIView):
    serializer_class = CustomAuthSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        serializer = self.get_serializer(instance=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.create(validated_data=serializer.validated_data)


class OtpVerification(APIView):
    serializer_class = OtpSerializer

    def post(self, request):
        instance = get_object_or_404(Otp, user__email=request.data['email'], code=request.data['code'])
        if instance.is_active():
            user = get_object_or_404(CustomUser, email=request.data['email'])
            token, created = Token.objects.get_or_create(user=user)
            if not user.is_active:
                user.make_user_active()
            instance.delete()
        else:
            instance.delete()
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT, data={'message':"OTP Expired. Try to login again."})
        return Response({'token': token.key})


@api_view(['POST'])
def request_for_otp(request):
    user = get_object_or_404(CustomUser, email=request.data['email'])
    otp = Otp.objects.create(user=user)
    otp.send_otp_as_mail()
    return Response(status=status.HTTP_201_CREATED, data={'message':"OTP send"})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_logout(request):
    request.user.auth_token.delete()
    auth_logout(request)
    return Response(status=status.HTTP_200_OK, data={'message':"Logged out"})


