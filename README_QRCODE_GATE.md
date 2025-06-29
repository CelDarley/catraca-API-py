# QR Code Gate com Redis - Raspberry Pi 5

Sistema de controle de acesso por QR Code que lê dados do Redis e aciona GPIO 23 quando um QR Code autorizado é detectado.

## 🚀 Funcionalidades

- ✅ Leitura contínua de QR Codes via câmera
- ✅ Verificação de autorização no Redis
- ✅ Acionamento do GPIO 23 por 5 segundos
- ✅ Cache local para performance otimizada
- ✅ Reconexão automática ao Redis
- ✅ Notificação para API externa
- ✅ Debounce para evitar leituras duplicadas

## 📋 Pré-requisitos

- Raspberry Pi 5
- Câmera USB ou câmera do módulo
- Python 3.7+
- Redis Server
- API Django rodando (para gerenciar QR codes)

## 🔧 Instalação

### 1. Instalar dependências do sistema

```bash
# Executar o script de instalação
chmod +x install_redis_dependencies.sh
./install_redis_dependencies.sh
```

### 2. Instalar dependências Python

```bash
pip install opencv-python pyzbar requests gpiozero redis
```

### 3. Verificar instalação

```bash
# Testar conexão Redis
python3 test_redis_connection.py

# Testar câmera
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Câmera OK' if cap.isOpened() else 'Erro na câmera'); cap.release()"

# Teste completo do sistema
python3 quick_test.py
```

## ⚙️ Configuração

### Configurações do Script

Edite o arquivo `qrcode_gate.py` para ajustar as configurações:

```python
# ---------- CONFIGURAÇÕES ----------
API_URL          = "https://api.thalamus.ind.br/acesso"  # URL da API
OUTPUT_PIN       = 23                                    # GPIO para acionar
REDIS_HOST       = "localhost"                           # Host do Redis
REDIS_PORT       = 6379                                  # Porta do Redis
REDIS_DB         = 1                                     # Database do Redis
REDIS_KEY_PREFIX = "qrcodes"                             # Prefixo das chaves
OUTPUT_PULSE     = 5                                     # Tempo de acionamento (segundos)
QRCODE_DEBOUNCE  = 6                                     # Debounce (segundos)
API_TIMEOUT      = 10                                    # Timeout da API (segundos)
REDIS_TIMEOUT    = 5                                     # Timeout do Redis (segundos)
CACHE_REFRESH    = 30                                    # Atualização do cache (segundos)
```

### Configurações do Redis

O sistema usa o Redis com as seguintes configurações:
- **Host**: localhost (mesma placa)
- **Porta**: 6379
- **Database**: 1
- **Prefixo das chaves**: `qrcodes:`

## 🚀 Como Usar

### 1. Adicionar QR Codes via API Django

Use a API Django para adicionar QR codes ao Redis:

```bash
# Obter token de autenticação
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "roboflex", "password": "Roboflex()123"}'

# Adicionar QR code
curl -X POST http://localhost:8000/api/qrcode/register/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{"qrcode": "SEU_QR_CODE_AQUI"}'

# Listar QR codes
curl -X GET http://localhost:8000/api/qrcode/list/ \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 2. Executar o QR Code Gate

```bash
python3 qrcode_gate.py
```

### 3. Testar

Apresente um QR Code autorizado à câmera. O sistema deve:
1. Detectar o QR Code
2. Verificar no Redis
3. Acionar o GPIO 23 por 5 segundos
4. Notificar a API externa

## 📊 Monitoramento

### Logs do Sistema

```bash
# Ver logs em tempo real
tail -f /var/log/syslog | grep qrcode

# Ver status do Redis
sudo systemctl status redis-server

# Ver logs do QR Code Gate
python3 qrcode_gate.py 2>&1 | tee qrcode_gate.log
```

### Verificar QR Codes no Redis

```bash
# Listar todos os QR codes
redis-cli -n 1 KEYS "qrcodes:*"

# Verificar um QR code específico
redis-cli -n 1 GET "qrcodes:SEU_QR_CODE"

# Contar total de QR codes
redis-cli -n 1 EVAL "return #redis.call('keys', 'qrcodes:*')" 0
```

## 🔍 Troubleshooting

### Problema: Redis não conecta

```bash
# Verificar se o Redis está rodando
sudo systemctl status redis-server

# Reiniciar Redis
sudo systemctl restart redis-server

# Verificar logs
sudo journalctl -u redis-server -f

# Testar conexão manual
python3 test_redis_connection.py
```

### Problema: Câmera não funciona

```bash
# Verificar se a câmera está sendo detectada
lsusb | grep -i camera

# Verificar permissões
sudo usermod -a -G video $USER

# Testar câmera
python3 -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened()); cap.release()"
```

### Problema: GPIO não aciona

```bash
# Verificar permissões GPIO
sudo usermod -a -G gpio $USER

# Testar GPIO
python3 -c "from gpiozero import OutputDevice; led = OutputDevice(23); led.on(); import time; time.sleep(1); led.off()"
```

### Problema: QR codes não são detectados

```bash
# Verificar se há QR codes no Redis
redis-cli -n 1 KEYS "qrcodes:*"

# Verificar se a API Django está funcionando
curl -X GET http://localhost:8000/api/qrcode/list/ \
  -H "Authorization: Bearer SEU_TOKEN"

# Testar o sistema completo
python3 quick_test.py
```

## 📈 Performance

O sistema foi otimizado para:
- **Cache local**: Atualiza a cada 30 segundos
- **Verificação rápida**: ~1000 operações/segundo
- **Reconexão automática**: Em caso de falha do Redis
- **Threading**: Não bloqueia a leitura da câmera

## 🔒 Segurança

- QR Codes são armazenados no Redis (database 1)
- Conexão local (localhost)
- Timeout configurável para evitar travamentos
- Debounce para evitar leituras duplicadas
- Autenticação via API Django

## 📝 Logs

O sistema gera logs detalhados:
- `[REDIS]` - Operações do Redis
- `[MATCH]` - QR Code autorizado detectado
- `[INFO]` - Informações gerais
- `[ERROR]` - Erros e problemas
- `[DEBUG]` - Informações de debug

## 🔄 Fluxo de Trabalho

1. **API Django** adiciona QR codes ao Redis
2. **QR Code Gate** lê continuamente a câmera
3. **Redis** verifica autorização dos QR codes
4. **GPIO 23** é acionado para QR codes autorizados
5. **API externa** é notificada do acesso

## 🤝 Contribuição

Para melhorar o sistema:
1. Teste as mudanças
2. Mantenha a compatibilidade com Redis
3. Documente novas funcionalidades
4. Teste no Raspberry Pi 5

## 📞 Suporte

Em caso de problemas:
1. Execute `python3 quick_test.py` para diagnóstico
2. Verifique os logs do sistema
3. Teste a conexão Redis
4. Verifique se a API Django está funcionando
5. Consulte a seção troubleshooting 