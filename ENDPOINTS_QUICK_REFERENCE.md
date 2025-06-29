# 🚀 Referência Rápida - Endpoints API QR Code

## 🔑 Autenticação
```
POST /api/token/
Body: {"username": "roboflex", "password": "Roboflex()123"}
```

## 📱 QR Codes

### Salvar QR Code
```
POST /api/qrcode/register/
Headers: Authorization: Bearer TOKEN
Body: {"qrcode": "VALOR"}
```

### Listar QR Codes
```
GET /api/qrcode/list/
Headers: Authorization: Bearer TOKEN
```

### Remover QR Code
```
DELETE /api/qrcode/delete/
Headers: Authorization: Bearer TOKEN
Body: {"qrcode": "VALOR"}
```

## 📊 Status Codes
- `200` - Sucesso
- `201` - Criado
- `400` - Dados inválidos
- `401` - Não autorizado
- `404` - Não encontrado
- `409` - Conflito (duplicado)

## 🧪 Exemplo cURL
```bash
# 1. Obter token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "roboflex", "password": "Roboflex()123"}'

# 2. Salvar QR code
curl -X POST http://localhost:8000/api/qrcode/register/ \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"qrcode": "TESTE123"}'

# 3. Listar QR codes
curl -X GET http://localhost:8000/api/qrcode/list/ \
  -H "Authorization: Bearer SEU_TOKEN"

# 4. Remover QR code
curl -X DELETE http://localhost:8000/api/qrcode/delete/ \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"qrcode": "TESTE123"}'
``` 