# API QR Code - Django REST Framework

API para registro e listagem de QR codes com autenticação JWT.

## Funcionalidades

- ✅ Autenticação JWT
- ✅ Registro de QR codes via POST
- ✅ Listagem de QR codes via GET
- ✅ Armazenamento em arquivo texto
- ✅ Configuração para produção

## Endpoints

### Autenticação
- `POST /api/token/` - Obter token JWT
- `POST /api/token/refresh/` - Renovar token JWT

### QR Codes
- `POST /api/qrcode/register/` - Salvar QR code
- `GET /api/qrcode/list/` - Listar todos os QR codes

## Deploy em Produção

### Opção 1: Deploy Automático
```bash
chmod +x deploy.sh
./deploy.sh
```

### Opção 2: Deploy Manual

1. **Instalar dependências do sistema:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx
```

2. **Configurar projeto:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configurar Django:**
```bash
export DJANGO_SETTINGS_MODULE=rasp_api.settings_prod
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

4. **Configurar Nginx:**
```bash
sudo cp nginx.conf /etc/nginx/sites-available/rasp_api
sudo ln -s /etc/nginx/sites-available/rasp_api /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

5. **Configurar Gunicorn:**
```bash
sudo cp rasp_api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rasp_api
sudo systemctl start rasp_api
```

## Uso da API

### 1. Obter Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "sua_senha"}'
```

### 2. Salvar QR Code
```bash
curl -X POST http://localhost:8000/api/qrcode/register/ \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"qrcode": "valor_do_qrcode"}'
```

### 3. Listar QR Codes
```bash
curl -X GET http://localhost:8000/api/qrcode/list/ \
  -H "Authorization: Bearer SEU_TOKEN"
```

## Estrutura do Projeto

```
api-rasp-qrcode/
├── rasp_api/                 # Projeto Django
│   ├── settings.py          # Configurações de desenvolvimento
│   ├── settings_prod.py     # Configurações de produção
│   ├── wsgi_prod.py         # WSGI para produção
│   └── urls.py              # URLs principais
├── qrcodeapp/               # Aplicação QR Code
│   ├── views.py             # Views da API
│   ├── serializers.py       # Serializers
│   └── urls.py              # URLs da aplicação
├── requirements.txt         # Dependências Python
├── gunicorn.conf.py         # Configuração Gunicorn
├── deploy.sh               # Script de deploy
└── README.md               # Este arquivo
```

## Configurações de Segurança

- ✅ DEBUG = False em produção
- ✅ ALLOWED_HOSTS configurado
- ✅ Headers de segurança habilitados
- ✅ Logs configurados
- ✅ Autenticação JWT obrigatória

## Monitoramento

- Logs do Django: `/var/log/django/rasp_api.log`
- Logs do Gunicorn: `/var/log/gunicorn/`
- Status do serviço: `sudo systemctl status rasp_api`

## Manutenção

### Reiniciar serviço:
```bash
sudo systemctl restart rasp_api
```

### Ver logs:
```bash
sudo journalctl -u rasp_api -f
```

### Atualizar código:
```bash
git pull
sudo systemctl restart rasp_api
``` 