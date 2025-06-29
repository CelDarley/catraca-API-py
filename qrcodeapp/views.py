from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import os
from .serializers import QRCodeSerializer
from .services import QRCodeService

# Create your views here.

class QRCodeRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = QRCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        qrcode = serializer.validated_data['qrcode']
        
        try:
            # Tentar adicionar o QR code (Redis verifica duplicatas automaticamente)
            success = QRCodeService.add_qrcode(qrcode)
            
            if success:
                return Response({
                    'message': 'QR code salvo com sucesso!'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error': 'QR code já existe no sistema.'
                }, status=status.HTTP_409_CONFLICT)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QRCodeListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            qrcodes = QRCodeService.get_all_qrcodes()
            total = QRCodeService.get_count()
            
            return Response({
                'qrcodes': qrcodes,
                'total': total
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QRCodeDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        qrcode = request.data.get('qrcode')
        if not qrcode:
            return Response({'error': 'O campo qrcode é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Tentar remover o QR code
            success = QRCodeService.remove_qrcode(qrcode)
            
            if success:
                return Response({
                    'message': 'QR code removido com sucesso!'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'QR code não encontrado.'
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
