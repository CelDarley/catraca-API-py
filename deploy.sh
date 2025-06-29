#!/bin/bash

# Script de Deploy para API QR Code
echo "Iniciando deploy da API QR Code..."

# Atualizar sistema
echo "Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependências do sistema
echo "Instalando dependências do sistema..."
sudo apt install -y python3 python3-pip python3-venv nginx

# Criar diretório de logs
echo "Criando diretórios de log..."
sudo mkdir -p /var/log/django
sudo mkdir -p /var/log/gunicorn
sudo chown -R $USER:$USER /var/log/django
sudo chown -R $USER:$USER /var/log/gunicorn

# Configurar permissões do arquivo de QR codes
echo "Configurando permissões do arquivo de QR codes..."
sudo touch /home/darley/qrcodes.txt
sudo chown $USER:$USER /home/darley/qrcodes.txt
sudo chmod 644 /home/darley/qrcodes.txt

# Criar ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências Python
echo "Instalando dependências Python..."
pip install -r requirements.txt

# Configurar Django
echo "Configurando Django..."
export DJANGO_SETTINGS_MODULE=rasp_api.settings_prod
python manage.py collectstatic --noinput
python manage.py migrate

# Criar usuário de produção
echo "Criando usuário de produção..."
python manage.py createsuperuser --username admin --email admin@example.com

# Configurar Nginx
echo "Configurando Nginx..."
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
echo "Configurando serviço systemd..."
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

echo "Deploy concluído!"
echo "API disponível em: http://SEU_IP_SERVIDOR"
echo "Endpoints:"
echo "  - POST /api/token/ (obter token)"
echo "  - POST /api/qrcode/register/ (salvar QR code)"
echo "  - GET /api/qrcode/list/ (listar QR codes)" 