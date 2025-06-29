#!/usr/bin/env python
"""
Script para criar usuário roboflex
Execute: python create_roboflex_user.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rasp_api.settings_prod')
django.setup()

from django.contrib.auth.models import User

def create_roboflex_user():
    username = 'roboflex'
    email = 'roboflex@roboflex.com.br'
    password = 'Roboflex()123'
    
    try:
        # Verificar se o usuário já existe
        if User.objects.filter(username=username).exists():
            print(f"Usuário {username} já existe. Atualizando...")
            user = User.objects.get(username=username)
            user.set_password(password)
            user.email = email
            user.save()
            print(f"Usuário {username} atualizado com sucesso!")
        else:
            print(f"Criando novo usuário {username}...")
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            print(f"Usuário {username} criado com sucesso!")
        
        print("\nCredenciais do usuário:")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Senha: {password}")
        
        return True
        
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return False

if __name__ == '__main__':
    success = create_roboflex_user()
    if success:
        print("\n✅ Usuário roboflex configurado com sucesso!")
    else:
        print("\n❌ Erro ao configurar usuário roboflex!")
        sys.exit(1) 