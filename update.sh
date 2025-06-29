#!/bin/bash

# Script de Atualização da API QR Code
echo "Iniciando atualização da API QR Code..."

# Parar o serviço
echo "Parando serviço..."
sudo systemctl stop rasp_api

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar dependências (se necessário)
echo "Verificando dependências..."
pip install -r requirements.txt

# Executar migrações (se houver)
echo "Executando migrações..."
python manage.py migrate

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Reiniciar o serviço
echo "Reiniciando serviço..."
sudo systemctl start rasp_api

# Verificar status
echo "Verificando status do serviço..."
sudo systemctl status rasp_api

echo "Atualização concluída!"
echo "Novos endpoints disponíveis:"
echo "  - DELETE /api/qrcode/delete/ (remover QR code)" 