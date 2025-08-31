import argparse
from scapy.all import rdpcap, ICMP, Raw
from termcolor import colored

def descifrado_cesar(texto_cifrado, clave):
    """Descifra un texto cifrado con el método César dada una clave."""
    resultado = ""
    for letra in texto_cifrado:
        if letra.isalpha():
            base = ord('a')
            desplazamiento = (ord(letra) - base - clave) % 26
            resultado += chr(base + desplazamiento)
        else:
            resultado += letra
    return resultado

def es_espanol_probable(texto):
    """Verifica si un texto parece ser español contando palabras comunes."""
    palabras_comunes = ["que", "en", "un", "una", "los", "las", "el", "la", "de", "con", "por", "redes", "seguridad"]
    texto_lower = texto.lower()
    coincidencias = 0
    for palabra in palabras_comunes:
        if f' {palabra} ' in f' {texto_lower} ':
            coincidencias += 1
    return coincidencias >= 2

def main():
    """Función principal para leer, reconstruir y descifrar el mensaje."""
    parser = argparse.ArgumentParser(description="Lector de paquetes ICMP para descifrar mensaje César.")
    parser.add_argument("pcap_file", help="Archivo de captura de red (.pcapng) a analizar.")
    args = parser.parse_args()

    try:
        packets = rdpcap(args.pcap_file)
    except FileNotFoundError:
        print(colored(f"Error: El archivo '{args.pcap_file}' no fue encontrado.", "red"))
        return

    texto_cifrado_reconstruido = ""
    for pkt in packets:
        if pkt.haslayer(ICMP) and pkt[ICMP].type == 8 and pkt.haslayer(Raw):
            payload = pkt[Raw].load
            if len(payload) >= 9:
                caracter = payload[8:9].decode('utf-8', errors='ignore')
                texto_cifrado_reconstruido += caracter
    
    if not texto_cifrado_reconstruido:
        print(colored("No se encontraron paquetes ICMP con datos para analizar en la captura.", "yellow"))
        return  

    print(f"Mensaje cifrado reconstruido: {colored(texto_cifrado_reconstruido, 'cyan')}\n")
    print("--- Intentos de Descifrado (Fuerza Bruta) ---")

    for clave in range(26):
        texto_descifrado = descifrado_cesar(texto_cifrado_reconstruido, clave)
        
        if es_espanol_probable(texto_descifrado):
            print(colored(f"Clave {clave}: {texto_descifrado}", "green", attrs=['bold']))
        else:
            print(f"Clave {clave}: {texto_descifrado}")

if __name__ == "__main__":
    main()