#!/usr/bin/env python3
"""
qrcode_gate_django_redis.py - Leitura contínua de QR Code - Raspberry Pi 5
Versão que usa a mesma configuração Redis do Django
"""

import os
import time
import threading
import cv2
import requests
import json
import redis
from pyzbar import pyzbar
from gpiozero import OutputDevice
from gpiozero.pins.lgpio import LGPIOFactory

# ---------- CONFIGURAÇÕES ----------
API_URL          = "https://api.thalamus.ind.br/acesso"  # URL configurável
OUTPUT_PIN       = 23
REDIS_HOST       = "127.0.0.1"  # Mesmo que Django
REDIS_PORT       = 6379
REDIS_DB         = 1            # Mesmo que Django
REDIS_KEY_PREFIX = "qrcodes"    # Mesmo que Django
OUTPUT_PULSE     = 5      # segundos que a saída fica acionada
QRCODE_DEBOUNCE  = 6      # segundos para ignorar o mesmo QR Code
API_TIMEOUT      = 10     # timeout para chamadas da API
REDIS_TIMEOUT    = 5      # timeout para conexão Redis

# ---------- CLASSE PARA GERENCIAR REDIS (MESMA CONFIGURAÇÃO DO DJANGO) ----------
class QRCodeRedisManager:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB):
        self.host = host
        self.port = port
        self.db = db
        self.redis_client = None
        self.connect()
    
    def connect(self):
        """Conecta ao Redis com a mesma configuração do Django"""
        try:
            # Usar exatamente a mesma configuração do Django
            self.redis_client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                socket_timeout=REDIS_TIMEOUT,
                socket_connect_timeout=REDIS_TIMEOUT,
                decode_responses=True,
                # Configurações adicionais do Django Redis
                socket_keepalive=True,
                socket_keepalive_options={},
                retry_on_timeout=True,
                health_check_interval=30
            )
            # Testa conexão
            self.redis_client.ping()
            print(f"[REDIS] Conectado com sucesso: {self.host}:{self.port} (DB:{self.db})")
            print(f"[REDIS] Usando mesma configuração do Django")
            return True
        except Exception as e:
            print(f"[REDIS] Erro ao conectar: {e}")
            return False
    
    def is_connected(self):
        """Verifica se está conectado ao Redis"""
        try:
            if self.redis_client:
                self.redis_client.ping()
                return True
        except:
            pass
        return False
    
    def reconnect(self):
        """Tenta reconectar ao Redis"""
        print("[REDIS] Tentando reconectar...")
        return self.connect()
    
    def qrcode_exists(self, qrcode):
        """Verifica se um QR code existe no Redis SEM cache local"""
        try:
            if not self.is_connected():
                if not self.reconnect():
                    return False
            # Consulta diretamente no Redis SEM cache local
            value = self.redis_client.get(f"{REDIS_KEY_PREFIX}:{qrcode}")
            return value is not None
        except Exception as e:
            print(f"[REDIS] Erro ao verificar QR code: {e}")
            return False
    
    def get_qrcode_count(self):
        """Retorna o total de QR codes"""
        try:
            if not self.is_connected():
                return 0
            
            pattern = f"{REDIS_KEY_PREFIX}:*"
            keys = self.redis_client.keys(pattern)
            return len(keys)
            
        except Exception as e:
            print(f"[REDIS] Erro ao contar QR codes: {e}")
            return 0
    
    def debug_redis_keys(self):
        """Debug: mostra todas as chaves no Redis"""
        try:
            if not self.is_connected():
                return
            
            all_keys = self.redis_client.keys("*")
            print(f"[DEBUG] Total de chaves no Redis: {len(all_keys)}")
            
            if all_keys:
                print("[DEBUG] Todas as chaves:")
                for key in all_keys:
                    value = self.redis_client.get(key)
                    print(f"  - {key} = {value}")
            
            # Chaves específicas do QR code
            qr_keys = self.redis_client.keys(f"{REDIS_KEY_PREFIX}:*")
            print(f"[DEBUG] Chaves QR codes: {len(qr_keys)}")
            for key in qr_keys:
                value = self.redis_client.get(key)
                print(f"  - {key} = {value}")
                
        except Exception as e:
            print(f"[DEBUG] Erro ao debugar chaves: {e}")

# ---------- FUNÇÃO PARA NOTIFICAR API ----------
def notificar_api_acesso(cod_qrcode, sentido="E"):
    """
    Notifica a API sobre o acesso - apenas para registro
    """
    # payload = {
    #     "cod_qrcode": cod_qrcode,
    #     "sentido": sentido
    # }
    
    # try:
    #     print(f"[DEBUG] Notificando API: {API_URL}")
    #     print(f"[DEBUG] Payload: {json.dumps(payload, indent=2)}")
        
    #     response = requests.post(API_URL, json=payload, timeout=API_TIMEOUT)
        
    #     print(f"[DEBUG] Status Code: {response.status_code}")
    #     print(f"[DEBUG] Response: {response.text}")
        
    #     if response.status_code == 200:
    #         print("[API] Notificação enviada com sucesso!")
    #         return True
    #     else:
    #         print(f"[ERROR] Erro ao notificar API - Status: {response.status_code}")
    #         return False
            
    # except requests.exceptions.ConnectionError:
    #     print("[ERROR] Erro de conexão - Verifique a internet e a URL da API")
    #     return False
    # except requests.exceptions.Timeout:
    #     print(f"[ERROR] Timeout na notificação da API ({API_TIMEOUT}s)")
    #     return False
    # except Exception as e:
    #     print(f"[ERROR] Erro inesperado ao notificar API: {e}")
    #     return False
    
    # Comentado temporariamente
    return True

# ---------- INICIALIZAÇÃO ----------
redis_manager = QRCodeRedisManager()

# Tentar inicializar GPIO de forma simples
try:
    # Configurar LGPIO explicitamente para Pi 5
    from gpiozero import Device
    Device.pin_factory = LGPIOFactory()
    
    output = OutputDevice(OUTPUT_PIN, active_high=True, initial_value=False)
    print(f"[GPIO] Saída configurada no pino {OUTPUT_PIN} (LGPIO)")
    gpio_available = True
except Exception as e:
    print(f"[GPIO] Erro ao configurar GPIO: {e}")
    print("[GPIO] Continuando sem GPIO (modo simulação)")
    gpio_available = False

output_active = threading.Event()

# ---------- FUNÇÃO PARA ACIONAR SAÍDA ----------
def acionar_saida(qr_data):
    if output_active.is_set():
        print("[INFO] Saída já está acionada, ignorando novo acionamento.")
        return
    
    def thread_acionamento():
        output_active.set()
        if gpio_available:
            output.on()
            print(f"[INFO] Saída ACESA por {OUTPUT_PULSE} segundos (QR Code: {qr_data}).")
        else:
            print(f"[SIMULAÇÃO] Saída seria ACIONADA por {OUTPUT_PULSE} segundos (QR Code: {qr_data}).")
        
        time.sleep(OUTPUT_PULSE)
        
        if gpio_available:
            output.off()
            print("[INFO] Saída APAGADA.")
        else:
            print("[SIMULAÇÃO] Saída seria DESLIGADA.")
        
        output_active.clear()
    
    # Executa em thread separada para não bloquear o loop principal
    threading.Thread(target=thread_acionamento, daemon=True).start()

# ---------- LOOP PRINCIPAL ----------
def main_loop():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERRO] Não foi possível abrir a webcam.")
        return

    # Debug: mostrar chaves do Redis
    print("\n[DEBUG] Verificando chaves do Redis...")
    redis_manager.debug_redis_keys()

    print("\n[READY] Sistema de QR Code com Redis Django iniciado.")
    print(f"[CONFIG] API URL: {API_URL}")
    print(f"[CONFIG] Redis: {REDIS_HOST}:{REDIS_PORT} (DB:{REDIS_DB})")
    print(f"[CONFIG] Saída: GPIO {OUTPUT_PIN} ({'ATIVO' if gpio_available else 'SIMULAÇÃO'})")
    print(f"[CONFIG] QR Codes autorizados: {redis_manager.get_qrcode_count()}")
    print(f"[CONFIG] Debounce QR Code: {QRCODE_DEBOUNCE} segundos")
    print(f"[CONFIG] Tempo de acionamento: {OUTPUT_PULSE} segundos")
    print(f"[CONFIG] Timeout API: {API_TIMEOUT} segundos")
    print("[INFO] Pressione Ctrl+C para sair.")

    ultimo_qrcode = None
    ultimo_qrcode_time = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.1)
                continue

            agora = time.time()

            # Leitura de QR Code
            qrcodes = pyzbar.decode(frame)
            for qr in qrcodes:
                qr_data = qr.data.decode('utf-8')
                
                # Verifica se é um QR Code válido no Redis (mesmo método do Django)
                if redis_manager.qrcode_exists(qr_data):
                    # Só processa se for um QR Code diferente ou se já passou o tempo de debounce
                    if qr_data != ultimo_qrcode or (agora - ultimo_qrcode_time) > QRCODE_DEBOUNCE:
                        print(f"[MATCH] QR Code autorizado detectado: {qr_data}")
                        
                        # ACIONA O PINO 23 IMEDIATAMENTE (sem depender da API)
                        acionar_saida(qr_data)
                        
                        # Notifica a API em thread separada para não bloquear
                        # def thread_notificacao():
                        #     sucesso = notificar_api_acesso(qr_data, "E")
                        #     if sucesso:
                        #         print("[API] Acesso registrado com sucesso na API")
                        #     else:
                        #         print("[API] Falha ao registrar acesso na API (mas porta foi acionada)")
                        
                        # threading.Thread(target=thread_notificacao, daemon=True).start()
                        
                        ultimo_qrcode = qr_data
                        ultimo_qrcode_time = agora
                    break
                else:
                    print(f"[INFO] QR Code NÃO autorizado: {qr_data}")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n[INFO] Encerrando sistema...")
    finally:
        cap.release()
        if gpio_available:
            output.off()
        print("[INFO] Sistema encerrado.")

if __name__ == "__main__":
    main_loop() 