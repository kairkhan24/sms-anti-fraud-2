from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import serializers, status

from hrm.services import send_sms_message


class SendSmsMessageApi(APIView):
    class InputSerializer(serializers.Serializer):
        recipient_phone = serializers.CharField(max_length=20)
        text = serializers.CharField(max_length=150)

    def get(self, request):
        query_params = request.query_params.dict()
        serializer = self.InputSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        recipient_phone = validated_data['recipient_phone']
        text = validated_data['text']
        send_sms_message(
            recipient_phone=recipient_phone,
            text=text,
        )
        return Response(status=status.HTTP_200_OK)

