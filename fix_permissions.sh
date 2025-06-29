#!/bin/bash

# Script para corrigir permissões do arquivo qrcodes.txt
echo "Corrigindo permissões do arquivo qrcodes.txt..."

# Verificar se o arquivo existe
if [ ! -f "/home/darley/qrcodes.txt" ]; then
    echo "Criando arquivo qrcodes.txt..."
    sudo touch /home/darley/qrcodes.txt
fi

# Corrigir permissões
echo "Ajustando permissões..."
sudo chown darley:darley /home/darley/qrcodes.txt
sudo chmod 644 /home/darley/qrcodes.txt

# Verificar permissões do diretório
echo "Verificando permissões do diretório..."
sudo chown darley:darley /home/darley/

# Verificar resultado
echo "Permissões atuais:"
ls -la /home/darley/qrcodes.txt

# Reiniciar serviço para aplicar mudanças
echo "Reiniciando serviço..."
sudo systemctl restart rasp_api

echo "Permissões corrigidas!" 