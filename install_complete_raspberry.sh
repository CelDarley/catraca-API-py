#!/bin/bash

# Script completo para instalar API + QR Code Gate na mesma placa Raspberry Pi
echo "🍓 Instalação completa: API + QR Code Gate no Raspberry Pi"

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt update

# Instalar dependências do sistema
echo "📦 Instalando dependências do sistema..."
sudo apt install -y python3 python3-pip python3-venv nginx redis-server python3-opencv python3-gpiozero redis-tools

# Configurar Redis
echo "🔧 Configurando Redis..."
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Criar diretório do projeto
echo "📁 Criando diretório do projeto..."
mkdir -p ~/api-rasp-qrcode
cd ~/api-rasp-qrcode

# Criar ambiente virtual
echo "🐍 Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip install Django==4.2.23 djangorestframework==3.15.2 djangorestframework-simplejwt==5.3.1 gunicorn==21.2.0 whitenoise==6.6.0 redis==5.0.1 django-redis==5.4.0

# Instalar dependências do QR Code Gate
echo "📦 Instalando dependências do QR Code Gate..."
pip install pyzbar requests opencv-python

# Criar diretório de logs
echo "📁 Criando diretórios de log..."
sudo mkdir -p /var/log/django
sudo mkdir -p /var/log/gunicorn
sudo chown -R $USER:$USER /var/log/django
sudo chown -R $USER:$USER /var/log/gunicorn

# Configurar permissões do arquivo de QR codes
echo "🔐 Configurando permissões..."
sudo touch /home/darley/qrcodes.txt
sudo chown $USER:$USER /home/darley/qrcodes.txt
sudo chmod 644 /home/darley/qrcodes.txt

# Configurar Django
echo "⚙️ Configurando Django..."
export DJANGO_SETTINGS_MODULE=rasp_api.settings_prod
python manage.py collectstatic --noinput
python manage.py migrate

# Criar usuário de produção
echo "👤 Criando usuário de produção..."
python manage.py createsuperuser --username roboflex --email roboflex@roboflex.com.br

# Configurar Nginx
echo "🌐 Configurando Nginx..."
sudo tee /etc/nginx/sites-available/rasp_api << EOF
server {
    listen 80;
    server_name _;

    location /static/ {
        alias /home/darley/api-rasp-qrcode/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Ativar site
sudo ln -sf /etc/nginx/sites-available/rasp_api /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Configurar systemd service
echo "🔧 Configurando serviço systemd..."
sudo tee /etc/systemd/system/rasp_api.service << EOF
[Unit]
Description=Rasp API QR Code
After=network.target

[Service]
User=darley
Group=darley
WorkingDirectory=/home/darley/api-rasp-qrcode
Environment="PATH=/home/darley/api-rasp-qrcode/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=rasp_api.settings_prod"
ExecStart=/home/darley/api-rasp-qrcode/venv/bin/gunicorn --config gunicorn.conf.py rasp_api.wsgi_prod:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Iniciar serviço
sudo systemctl daemon-reload
sudo systemctl enable rasp_api
sudo systemctl start rasp_api

# Testar Redis
echo "🧪 Testando Redis..."
redis-cli ping

# Testar API
echo "🧪 Testando API..."
sleep 5
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "roboflex", "password": "Roboflex()123"}' || echo "API ainda inicializando..."

echo ""
echo "✅ Instalação completa concluída!"
echo ""
echo "📋 Serviços disponíveis:"
echo "  🌐 API: http://localhost:8000"
echo "  🔑 Usuário: roboflex"
echo "  🔑 Senha: Roboflex()123"
echo ""
echo "📋 Para executar o QR Code Gate:"
echo "  cd ~/api-rasp-qrcode"
echo "  python3 qrcode_gate_redis.py"
echo ""
echo "📋 Para verificar status:"
echo "  sudo systemctl status rasp_api"
echo "  sudo systemctl status redis-server"
echo "  sudo systemctl status nginx" 