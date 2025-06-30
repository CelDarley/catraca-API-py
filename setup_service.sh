#!/bin/bash

# Script para configurar a API Django como serviço systemd
echo "🚀 Configurando API Django como serviço systemd..."

# Configurações
SERVICE_NAME="rasp_api"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
PROJECT_PATH="/home/darley/api-rasp-qrcode"
USER="darley"

echo "📋 Configurações:"
echo "  Serviço: $SERVICE_NAME"
echo "  Arquivo: $SERVICE_FILE"
echo "  Projeto: $PROJECT_PATH"
echo "  Usuário: $USER"

# Verificar se o projeto existe
if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ Erro: Diretório do projeto não encontrado: $PROJECT_PATH"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "$PROJECT_PATH/venv" ]; then
    echo "❌ Erro: Ambiente virtual não encontrado: $PROJECT_PATH/venv"
    exit 1
fi

# Verificar se o arquivo de serviço existe no projeto
if [ ! -f "$PROJECT_PATH/rasp_api.service" ]; then
    echo "❌ Erro: Arquivo rasp_api.service não encontrado no projeto"
    exit 1
fi

# Copiar arquivo de serviço
echo "📦 Copiando arquivo de serviço..."
sudo cp "$PROJECT_PATH/rasp_api.service" "$SERVICE_FILE"

# Verificar se foi copiado
if [ ! -f "$SERVICE_FILE" ]; then
    echo "❌ Erro: Falha ao copiar arquivo de serviço"
    exit 1
fi

echo "✅ Arquivo de serviço copiado"

# Configurar permissões
echo "🔐 Configurando permissões..."
sudo chmod 644 "$SERVICE_FILE"
sudo chown root:root "$SERVICE_FILE"

# Recarregar systemd
echo "🔄 Recarregando systemd..."
sudo systemctl daemon-reload

# Habilitar serviço para iniciar no boot
echo "🚀 Habilitando serviço para iniciar no boot..."
sudo systemctl enable "$SERVICE_NAME"

# Verificar se foi habilitado
if sudo systemctl is-enabled "$SERVICE_NAME" > /dev/null 2>&1; then
    echo "✅ Serviço habilitado para iniciar no boot"
else
    echo "❌ Erro: Falha ao habilitar serviço"
    exit 1
fi

# Parar serviço se estiver rodando
echo "⏹️ Parando serviço se estiver rodando..."
sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true

# Iniciar serviço
echo "▶️ Iniciando serviço..."
sudo systemctl start "$SERVICE_NAME"

# Aguardar um pouco
sleep 3

# Verificar status
echo "📊 Verificando status do serviço..."
if sudo systemctl is-active "$SERVICE_NAME" > /dev/null 2>&1; then
    echo "✅ Serviço iniciado com sucesso!"
else
    echo "❌ Erro: Falha ao iniciar serviço"
    echo "📋 Logs do serviço:"
    sudo journalctl -u "$SERVICE_NAME" --no-pager -n 20
    exit 1
fi

# Mostrar status
echo ""
echo "📋 Status do serviço:"
sudo systemctl status "$SERVICE_NAME" --no-pager

echo ""
echo "🎉 Configuração concluída!"
echo ""
echo "📋 Comandos úteis:"
echo "  Status: sudo systemctl status $SERVICE_NAME"
echo "  Logs: sudo journalctl -u $SERVICE_NAME -f"
echo "  Reiniciar: sudo systemctl restart $SERVICE_NAME"
echo "  Parar: sudo systemctl stop $SERVICE_NAME"
echo "  Iniciar: sudo systemctl start $SERVICE_NAME"
echo ""
echo "🔄 A API agora iniciará automaticamente no boot do sistema!" 