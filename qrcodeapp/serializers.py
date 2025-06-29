from rest_framework import serializers

class QRCodeSerializer(serializers.Serializer):
    qrcode = serializers.CharField(required=True) 