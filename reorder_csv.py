#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import argparse
import os
import sys

def detectar_delimitador(archivo):
    """
    Detecta el delimitador utilizado en un archivo CSV.
    
    Args:
        archivo (str): Ruta al archivo CSV
        
    Returns:
        str: Delimitador detectado (coma, punto y coma, etc.)
    """
    with open(archivo, 'r', encoding='utf-8') as f:
        primera_linea = f.readline().strip()
        
        # Probar delimitadores comunes
        for delimitador in [',', ';', '\t', '|']:
            if delimitador in primera_linea:
                return delimitador
                
        # Si no se detecta ninguno, usar coma por defecto
        return ','

def ordenar_csv(archivo_entrada, columna, archivo_salida=None, delimitador=None):
    """
    Reordena un archivo CSV por la columna especificada de menor a mayor.
    
    Args:
        archivo_entrada (str): Ruta al archivo CSV de entrada
        columna (str): Nombre de la columna por la cual ordenar
        archivo_salida (str, opcional): Ruta al archivo CSV de salida. 
                                      Si no se especifica, sobreescribe el archivo de entrada.
        delimitador (str, opcional): Delimitador utilizado en el CSV. Si es None, se detectará automáticamente.
    """
    try:
        # Si no se especifica archivo de salida, usamos un temporal y luego reemplazamos
        if archivo_salida is None:
            archivo_salida = archivo_entrada + ".temp"
            reemplazar = True
        else:
            reemplazar = False
            
        # Verificar que el archivo de entrada existe
        if not os.path.exists(archivo_entrada):
            print(f"Error: El archivo '{archivo_entrada}' no existe.")
            return False
        
        # Detectar el delimitador si no se especifica
        if delimitador is None:
            delimitador = detectar_delimitador(archivo_entrada)
            print(f"Delimitador detectado: '{delimitador}'")
            
        # Leer el archivo CSV de entrada
        with open(archivo_entrada, 'r', newline='', encoding='utf-8') as f_entrada:
            reader = csv.DictReader(f_entrada, delimiter=delimitador)
            
            # Verificar que la columna existe
            if columna not in reader.fieldnames:
                print(f"Error: La columna '{columna}' no existe en el archivo. Columnas disponibles: {', '.join(reader.fieldnames)}")
                return False
                
            # Leer todas las filas
            filas = list(reader)
            
            # Intentar ordenar numéricamente
            try:
                filas_ordenadas = sorted(filas, key=lambda x: float(x[columna]))
            except ValueError:
                # Si falla, ordenar como texto
                print("Aviso: Algunos valores no son numéricos. Ordenando como texto.")
                filas_ordenadas = sorted(filas, key=lambda x: x[columna])
                
            # Escribir al archivo de salida con el mismo delimitador
            with open(archivo_salida, 'w', newline='', encoding='utf-8') as f_salida:
                writer = csv.DictWriter(f_salida, fieldnames=reader.fieldnames, delimiter=delimitador)
                writer.writeheader()
                writer.writerows(filas_ordenadas)
                
            # Si estamos reemplazando el archivo original
            if reemplazar:
                os.replace(archivo_salida, archivo_entrada)
                print(f"Archivo '{archivo_entrada}' reordenado exitosamente por la columna '{columna}'.")
            else:
                print(f"Datos ordenados guardados en '{archivo_salida}'.")
                
            return True
            
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")
        return False

def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Reordena un archivo CSV por una columna específica de menor a mayor.')
    parser.add_argument('archivo', help='Ruta al archivo CSV a ordenar')
    parser.add_argument('columna', help='Nombre de la columna por la cual ordenar')
    parser.add_argument('-o', '--output', help='Archivo de salida (opcional, por defecto sobreescribe el original)')
    parser.add_argument('-d', '--delimiter', help='Delimitador usado en el CSV (opcional, por defecto se detecta automáticamente)')
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Ejecutar la función principal
    ordenar_csv(args.archivo, args.columna, args.output, args.delimiter)

if __name__ == "__main__":
    main()