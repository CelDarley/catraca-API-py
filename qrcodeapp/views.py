from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import os
from .serializers import QRCodeSerializer

# Create your views here.

class QRCodeRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = QRCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        qrcode = serializer.validated_data['qrcode']
        
        try:
            # Verificar se o arquivo existe
            if os.path.exists('/home/darley/qrcodes.txt'):
                # Ler QR codes existentes
                with open('/home/darley/qrcodes.txt', 'r') as f:
                    existing_qrcodes = [line.strip() for line in f.readlines()]
                
                # Verificar se o QR code já existe
                if qrcode in existing_qrcodes:
                    return Response({
                        'error': 'QR code já existe no sistema.'
                    }, status=status.HTTP_409_CONFLICT)
            
            # Salvar o novo QR code
            with open('/home/darley/qrcodes.txt', 'a') as f:
                f.write(qrcode + '\n')
            
            return Response({
                'message': 'QR code salvo com sucesso!'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QRCodeListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            qrcodes = []
            if os.path.exists('/home/darley/qrcodes.txt'):
                with open('/home/darley/qrcodes.txt', 'r') as f:
                    qrcodes = [line.strip() for line in f.readlines() if line.strip()]
            
            return Response({
                'qrcodes': qrcodes,
                'total': len(qrcodes)
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
            if not os.path.exists('/home/darley/qrcodes.txt'):
                return Response({'error': 'Arquivo de QR codes não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            
            # Ler todos os QR codes
            with open('/home/darley/qrcodes.txt', 'r') as f:
                qrcodes = f.readlines()
            
            # Filtrar o QR code a ser removido
            original_count = len(qrcodes)
            qrcodes = [line for line in qrcodes if line.strip() != qrcode]
            
            if len(qrcodes) == original_count:
                return Response({'error': 'QR code não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            
            # Reescrever o arquivo sem o QR code removido
            with open('/home/darley/qrcodes.txt', 'w') as f:
                f.writelines(qrcodes)
            
            return Response({'message': 'QR code removido com sucesso!'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
