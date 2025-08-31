# Canal Encubierto ICMP Sigiloso (Stealth)
Este proyecto demuestra cómo usar paquetes **ICMP (ping)** para crear un canal de comunicación encubierto y exfiltrar datos. Incluye scripts para **cifrar, enviar de forma sigilosa y recuperar/descifrar el mensaje**.

## Requisitos
- Python 3  
- Librerías necesarias:  
  ```bash
  pip install scapy termcolor
  ```
- El script de envío (`stealth_icmp_send.py`) necesita ser ejecutado con **sudo**.

## Uso Rápido
El proceso se resume en 4 pasos:

### 1. Cifrar el Mensaje
```bash
python3 caesar.py --modo cifrar --clave 9 --texto "criptografia y seguridad en redes"
# Salida: larycxpajorjh bnpdarmjm nw anmnb
```

### 2. Iniciar la Captura de Red
Usa **Wireshark** o **tshark** para empezar a capturar el tráfico en la interfaz que vayas a usar (ejemplo: `lo`).

### 3. Enviar el Mensaje Oculto
```bash
sudo python3 stealth_icmp_send.py --dst 127.0.0.1 --texto-cifrado "larycxpajorjh bnpdarmjm nw anmnb"
```
Al terminar, detén la captura y guarda el archivo (ejemplo: `captura.pcapng`).

### 4. Recuperar y Descifrar
```bash
python3 recover_caesar.py captura.pcapng
```
El script leerá la captura, **reconstruirá el mensaje y encontrará la clave correcta**.

## Prueba Rápida
Para una prueba rápida, puedes usar el archivo `caesar.pcapng` incluido en este repositorio y ejecutar directamente el **paso 4**.
