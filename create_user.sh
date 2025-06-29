#!/bin/bash

# Script para criar usuário roboflex em produção
echo "Criando usuário roboflex..."

# Ativar ambiente virtual
source venv/bin/activate

# Configurar Django para produção
export DJANGO_SETTINGS_MODULE=rasp_api.settings_prod

# Criar usuário roboflex
echo "Criando usuário roboflex..."
python manage.py shell << EOF
from django.contrib.auth.models import User

# Verificar se o usuário já existe
if User.objects.filter(username='roboflex').exists():
    print("Usuário roboflex já existe. Atualizando...")
    user = User.objects.get(username='roboflex')
    user.set_password('Roboflex()123')
    user.email = 'roboflex@roboflex.com.br'
    user.save()
    print("Usuário roboflex atualizado com sucesso!")
else:
    print("Criando novo usuário roboflex...")
    user = User.objects.create_user(
        username='roboflex',
        email='roboflex@roboflex.com.br',
        password='Roboflex()123'
    )
    print("Usuário roboflex criado com sucesso!")

print(f"Username: {user.username}")
print(f"Email: {user.email}")
print("Senha: Roboflex()123")
EOF

echo "Usuário roboflex configurado!"
echo "Credenciais:"
echo "  Username: roboflex"
echo "  Email: roboflex@roboflex.com.br"
echo "  Senha: Roboflex()123" 