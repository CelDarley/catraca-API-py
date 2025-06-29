from django.core.cache import cache
from django_redis import get_redis_connection
from typing import List, Optional
import json

class QRCodeService:
    """Serviço para gerenciar QR codes usando Redis diretamente"""
    
    CACHE_KEY = "qrcodes"
    CACHE_TIMEOUT = 60 * 60 * 24 * 365  # 1 ano
    
    @classmethod
    def _get_redis_client(cls):
        """Obtém cliente Redis direto"""
        return get_redis_connection("default")
    
    @classmethod
    def add_qrcode(cls, qrcode: str) -> bool:
        """
        Adiciona um QR code ao Redis diretamente
        Retorna True se adicionado, False se já existia
        """
        try:
            redis_client = cls._get_redis_client()
            key = f"{cls.CACHE_KEY}:{qrcode}"
            
            # Usar SET com NX para verificar se já existe
            result = redis_client.set(key, qrcode, ex=cls.CACHE_TIMEOUT, nx=True)
            return result
        except Exception as e:
            print(f"Erro ao adicionar QR code: {e}")
            return False
    
    @classmethod
    def remove_qrcode(cls, qrcode: str) -> bool:
        """
        Remove um QR code do Redis diretamente
        Retorna True se removido, False se não existia
        """
        try:
            redis_client = cls._get_redis_client()
            key = f"{cls.CACHE_KEY}:{qrcode}"
            
            # Verificar se existe antes de remover
            exists = redis_client.exists(key)
            if exists:
                redis_client.delete(key)
                return True
            return False
        except Exception as e:
            print(f"Erro ao remover QR code: {e}")
            return False
    
    @classmethod
    def get_all_qrcodes(cls) -> List[str]:
        """
        Retorna todos os QR codes salvos diretamente do Redis
        """
        try:
            redis_client = cls._get_redis_client()
            pattern = f"{cls.CACHE_KEY}:*"
            keys = redis_client.keys(pattern)
            
            if not keys:
                return []
            
            # Buscar todos os valores de uma vez
            values = redis_client.mget(keys)
            return [v for v in values if v is not None]
            
        except Exception as e:
            print(f"Erro ao buscar QR codes: {e}")
            return []
    
    @classmethod
    def qrcode_exists(cls, qrcode: str) -> bool:
        """
        Verifica se um QR code existe diretamente no Redis
        """
        try:
            redis_client = cls._get_redis_client()
            key = f"{cls.CACHE_KEY}:{qrcode}"
            return redis_client.exists(key) > 0
        except Exception as e:
            print(f"Erro ao verificar QR code: {e}")
            return False
    
    @classmethod
    def get_count(cls) -> int:
        """
        Retorna o total de QR codes diretamente do Redis
        """
        try:
            redis_client = cls._get_redis_client()
            pattern = f"{cls.CACHE_KEY}:*"
            keys = redis_client.keys(pattern)
            return len(keys)
        except Exception as e:
            print(f"Erro ao contar QR codes: {e}")
            return 0
    
    @classmethod
    def clear_all(cls) -> bool:
        """
        Remove todos os QR codes diretamente do Redis
        """
        try:
            redis_client = cls._get_redis_client()
            pattern = f"{cls.CACHE_KEY}:*"
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
            return True
        except Exception as e:
            print(f"Erro ao limpar QR codes: {e}")
            return False 