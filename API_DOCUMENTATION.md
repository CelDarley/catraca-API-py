# 📋 Documentação da API QR Code

API para gerenciamento de QR codes com autenticação JWT.

## 🔐 Autenticação

Todos os endpoints (exceto autenticação) requerem token JWT no header:
```
Authorization: Bearer SEU_TOKEN_JWT
```

---

## 🔑 Endpoints de Autenticação

### 1. Obter Token JWT
**POST** `/api/token/`

**Descrição:** Obtém token de acesso JWT para autenticação.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "username": "roboflex",
  "password": "Roboflex()123"
}
```

**Resposta de Sucesso (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Resposta de Erro (401):**
```json
{
  "detail": "No valid credentials provided."
}
```

---

### 2. Renovar Token JWT
**POST** `/api/token/refresh/`

**Descrição:** Renova o token de acesso usando o refresh token.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Resposta de Sucesso (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 📱 Endpoints de QR Codes

### 3. Registrar QR Code
**POST** `/api/qrcode/register/`

**Descrição:** Salva um novo QR code no sistema (não permite duplicatas).

**Headers:**
```
Authorization: Bearer SEU_TOKEN_JWT
Content-Type: application/json
```

**Body:**
```json
{
  "qrcode": "VALOR_DO_QRCODE"
}
```

**Resposta de Sucesso (201):**
```json
{
  "message": "QR code salvo com sucesso!"
}
```

**Resposta de Erro - QR Code Duplicado (409):**
```json
{
  "error": "QR code já existe no sistema."
}
```

**Resposta de Erro - Dados Inválidos (400):**
```json
{
  "qrcode": ["Este campo é obrigatório."]
}
```

**Resposta de Erro - Não Autorizado (401):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 4. Listar QR Codes
**GET** `/api/qrcode/list/`

**Descrição:** Retorna todos os QR codes salvos no sistema.

**Headers:**
```
Authorization: Bearer SEU_TOKEN_JWT
```

**Resposta de Sucesso (200):**
```json
{
  "qrcodes": [
    "QR_CODE_1",
    "QR_CODE_2",
    "QR_CODE_3"
  ],
  "total": 3
}
```

**Resposta de Erro - Não Autorizado (401):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 5. Remover QR Code
**DELETE** `/api/qrcode/delete/`

**Descrição:** Remove um QR code específico do sistema.

**Headers:**
```
Authorization: Bearer SEU_TOKEN_JWT
Content-Type: application/json
```

**Body:**
```json
{
  "qrcode": "VALOR_DO_QRCODE_A_REMOVER"
}
```

**Resposta de Sucesso (200):**
```json
{
  "message": "QR code removido com sucesso!"
}
```

**Resposta de Erro - QR Code Não Encontrado (404):**
```json
{
  "error": "QR code não encontrado."
}
```

**Resposta de Erro - Campo Obrigatório (400):**
```json
{
  "error": "O campo qrcode é obrigatório."
}
```

**Resposta de Erro - Não Autorizado (401):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 🧪 Exemplos de Uso

### Exemplo Completo com cURL

#### 1. Obter Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "roboflex",
    "password": "Roboflex()123"
  }'
```

#### 2. Salvar QR Code
```bash
curl -X POST http://localhost:8000/api/qrcode/register/ \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "qrcode": "QR123456789"
  }'
```

#### 3. Listar QR Codes
```bash
curl -X GET http://localhost:8000/api/qrcode/list/ \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### 4. Remover QR Code
```bash
curl -X DELETE http://localhost:8000/api/qrcode/delete/ \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "qrcode": "QR123456789"
  }'
```

---

## 📊 Códigos de Status HTTP

| Código | Descrição | Uso |
|--------|-----------|-----|
| 200 | OK | Operação realizada com sucesso |
| 201 | Created | QR code criado com sucesso |
| 400 | Bad Request | Dados inválidos ou campo obrigatório faltando |
| 401 | Unauthorized | Token JWT inválido ou não fornecido |
| 404 | Not Found | QR code não encontrado |
| 409 | Conflict | QR code já existe (duplicado) |
| 500 | Internal Server Error | Erro interno do servidor |

---

## 🔧 Configuração de Produção

### URLs de Produção
Substitua `localhost:8000` pelo IP ou domínio do seu servidor:

- **Desenvolvimento:** `http://localhost:8000`
- **Produção:** `http://SEU_IP_SERVIDOR` ou `http://seu-dominio.com`

### Credenciais Padrão
- **Username:** `roboflex`
- **Email:** `roboflex@roboflex.com.br`
- **Password:** `Roboflex()123`

---

## 📝 Notas Importantes

1. **Autenticação Obrigatória:** Todos os endpoints de QR codes requerem token JWT válido
2. **Sem Duplicatas:** O sistema não permite QR codes repetidos
3. **Persistência:** QR codes são salvos em `/home/darley/qrcodes.txt`
4. **Case Sensitive:** QR codes são tratados como case sensitive
5. **Logs:** Todas as operações são logadas para auditoria

---

## 🚀 Monitoramento

### Verificar Status da API
```bash
sudo systemctl status rasp_api
```

### Ver Logs
```bash
sudo journalctl -u rasp_api -f
```

### Reiniciar Serviço
```bash
sudo systemctl restart rasp_api
``` 