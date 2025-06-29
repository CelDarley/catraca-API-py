#!/bin/bash

# Script completo para atualização segura da aplicação
echo "🚀 Atualização Completa e Segura da Aplicação"

# Configurações
RASPBERRY_USER="darley"
RASPBERRY_IP="10.100.0.105"
RASPBERRY_PATH="/home/darley/api-rasp-qrcode"

echo "📤 Conectando ao Raspberry Pi: $RASPBERRY_USER@$RASPBERRY_IP"

# 1. Fazer backup
echo "💾 Fazendo backup da aplicação atual..."
ssh $RASPBERRY_USER@$RASPBERRY_IP << 'EOF'
    # Parar serviços
    sudo systemctl stop rasp_api
    
    # Criar backup
    if [ -d "/home/darley/api-rasp-qrcode" ]; then
        echo "Criando backup..."
        cp -r /home/darley/api-rasp-qrcode /home/darley/api-rasp-qrcode-backup-$(date +%Y%m%d_%H%M%S)
        echo "Backup criado com sucesso!"
    else
        echo "Diretório não existe, criando novo..."
    fi
EOF

# 2. Copiar arquivos atualizados
echo "📦 Copiando arquivos atualizados..."
scp -r rasp_api/ $RASPBERRY_USER@$RASPBERRY_IP:$RASPBERRY_PATH/
scp -r qrcodeapp/ $RASPBERRY_USER@$RASPBERRY_IP:$RASPBERRY_PATH/
scp requirements.txt $RASPBERRY_USER@$RASPBERRY_IP:$RASPBERRY_PATH/
scp manage.py $RASPBERRY_USER@$RASPBERRY_IP:$RASPBERRY_PATH/
scp gunicorn.conf.py $RASPBERRY_USER@$RASPBERRY_IP:$RASPBERRY_PATH/

# 3. Copiar arquivos do QR Code Gate
echo "📦 Copiando arquivos do QR Code Gate..."
scp qrcode_gate_redis.py $RASPBERRY_USER@$RASPBERRY_IP:$RASPBERRY_PATH/
scp configure_raspberry_redis.py $RASPBERRY_USER@$RASPBERRY_IP:$RASPBERRY_PATH/

# 4. Atualizar no Raspberry Pi
echo "🔄 Atualizando no Raspberry Pi..."
ssh $RASPBERRY_USER@$RASPBERRY_IP << 'EOF'
    cd /home/darley/api-rasp-qrcode
    
    # Restaurar banco de dados se existir no backup
    if [ -f "/home/darley/api-rasp-qrcode-backup-$(date +%Y%m%d)*/db.sqlite3" ]; then
        echo "Restaurando banco de dados..."
        cp /home/darley/api-rasp-qrcode-backup-$(date +%Y%m%d)*/db.sqlite3 .
    fi
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Instalar dependências Redis (corrigir erro)
    echo "Instalando dependências Redis..."
    pip install redis==5.0.1 django-redis==5.4.0
    
    # Instalar outras dependências
    echo "Instalando outras dependências..."
    pip install -r requirements.txt
    
    # Verificar instalação Redis
    echo "Verificando Redis..."
    python -c "import redis; print('Redis OK')"
    python -c "import django_redis; print('Django Redis OK')"
    
    # Executar migrações (preserva dados)
    echo "Executando migrações..."
    python manage.py migrate
    
    # Coletar arquivos estáticos
    echo "Coletando arquivos estáticos..."
    python manage.py collectstatic --noinput
    
    # Verificar se o usuário roboflex existe
    echo "Verificando usuário roboflex..."
    python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='roboflex').exists():
    User.objects.create_user('roboflex', 'roboflex@roboflex.com.br', 'Roboflex()123')
    print('Usuário roboflex criado')
else:
    print('Usuário roboflex já existe')
"
    
    # Testar configuração Django
    echo "Testando configuração Django..."
    python manage.py check
    
    # Reiniciar serviços
    echo "Reiniciando serviços..."
    sudo systemctl restart rasp_api
    
    # Verificar status
    echo "Verificando status..."
    sudo systemctl status rasp_api --no-pager
EOF

echo "✅ Atualização completa concluída!"
echo ""
echo "📋 Verificações:"
echo "1. API: curl -X POST http://$RASPBERRY_IP/api/token/ -H 'Content-Type: application/json' -d '{\"username\": \"roboflex\", \"password\": \"Roboflex()123\"}'"
echo "2. Redis: ssh $RASPBERRY_USER@$RASPBERRY_IP 'redis-cli ping'"
echo "3. QR Code Gate: ssh $RASPBERRY_USER@$RASPBERRY_IP 'cd $RASPBERRY_PATH && python3 qrcode_gate_redis.py'"
echo "4. Logs: ssh $RASPBERRY_USER@$RASPBERRY_IP 'sudo journalctl -u rasp_api -f'" 