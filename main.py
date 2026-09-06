import os
import time
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Almacén temporal en memoria para nuestras llaves maestras
key_store = {}
active_key_id = None
ROTATION_INTERVAL_SECONDS = 30  # Rotación rápida a los 30 segundos para demostración

def generate_master_key():
    """Genera una llave aleatoria militar de 256 bits (AES-256)"""
    global active_key_id
    
    key_id = os.urandom(8).hex()  # ID único en formato hexadecimal
    key_bytes = AESGCM.generate_key(bit_length=256)  # 32 bytes criptográficamente seguros
    
    created_at = datetime.now()
    expires_at = created_at + timedelta(seconds=ROTATION_INTERVAL_SECONDS)
    
    key_store[key_id] = {
        "key": key_bytes,
        "created_at": created_at,
        "expires_at": expires_at
    }
    
    active_key_id = key_id
    print(f"\n[KMS]  NUEVA CLAVE MAESTRA GENERADA. ID: {key_id}")
    print(f"[KMS]  Expiración configurada para: {expires_at.strftime('%H:%M:%S')}")

def check_and_rotate_key():
    """Verifica el ciclo de vida de la llave activa y gatilla la rotación"""
    if not active_key_id:
        generate_master_key()
        return
        
    current_key = key_store[active_key_id]
    if datetime.now() > current_key["expires_at"]:
        print(f"\n[KMS]  ALERTA: La clave activa ({active_key_id}) ha expirado.")
        generate_master_key()

def encrypt_secret(plain_text: str):
    """Cifra el secreto usando AES-256-GCM con la llave activa del momento"""
    check_and_rotate_key()
    
    master_key = key_store[active_key_id]["key"]
    aesgcm = AESGCM(master_key)
    nonce = os.urandom(12)  # Vector de Inicialización único de 12 bytes exigido por GCM
    
    encrypted_bytes = aesgcm.encrypt(nonce, plain_text.encode('utf-8'), None)
    
    return {
        "key_id": active_key_id,
        "nonce": nonce.hex(),
        "ciphertext": encrypted_bytes.hex()
    }

def decrypt_secret(packet):
    """Descifra datos históricos buscando la llave correspondiente por su ID único"""
    target_key_id = packet["key_id"]
    
    if target_key_id not in key_store:
        raise Exception(f"[KMS]  Error: La clave {target_key_id} no existe en el almacén.")
        
    master_key = key_store[target_key_id]["key"]
    aesgcm = AESGCM(master_key)
    
    nonce = bytes.fromhex(packet["nonce"])
    ciphertext = bytes.fromhex(packet["ciphertext"])
    
    decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
    return decrypted_bytes.decode('utf-8')

if __name__ == "__main__":
    print("==================================================")
    print(" INICIANDO SIMULADOR SECRETVAULT-KMS ")
    print("==================================================")
    
    generate_master_key()
    paquete_antiguo = None
    
    # Simulación del ciclo continuo de cifrado
    for i in range(4):
        print(f"\n--- [Petición de Resguardo #{i+1}] ---")
        secreto_original = "Token_Super_Secreto_DB_2026"
        
        paquete_cifrado = encrypt_secret(secreto_original)
        print(f"[App]  Texto Cifrado (Hex): {paquete_cifrado['ciphertext'][:20]}...")
        print(f"[App]  Usando Key ID: {paquete_cifrado['key_id']}")
        
        if paquete_antiguo is None:
            paquete_antiguo = paquete_cifrado
            
        try:
            texto_recuperado = decrypt_secret(paquete_antiguo)
            print(f"[App]  Descifrado histórico exitoso: '{texto_recuperado}'")
        except Exception as e:
            print(str(e))
            
        time.sleep(15)
