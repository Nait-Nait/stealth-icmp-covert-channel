def cifrado_cesar(mensaje, clave, modo='cifrar'):
    resultado = ""
    for letra in mensaje:
        if letra.isalpha(): 
            base = ord('A') if letra.isupper() else ord('a')
            desplazamiento = (ord(letra) - base + (clave if modo == 'cifrar' else -clave)) % 26
            resultado += chr(base + desplazamiento)
        else:
            resultado += letra
    return resultado


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Cifrado César simple")
    parser.add_argument("--modo", choices=["cifrar", "descifrar"], required=True,
                        help="Elige si quieres cifrar o descifrar")
    parser.add_argument("--clave", type=int, required=True,
                        help="Número de desplazamientos")
    parser.add_argument("--texto", type=str, required=True,
                        help="Texto a procesar")
    args = parser.parse_args()

    print(cifrado_cesar(args.texto, args.clave, args.modo))