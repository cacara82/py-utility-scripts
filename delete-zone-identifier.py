import os

def eliminar_zone_identifier(carpeta):
    if not os.path.isdir(carpeta):
        print(f"La carpeta '{carpeta}' no existe.")
        return
    
    for item in os.listdir(carpeta):
        ruta_item = os.path.join(carpeta, item)
        
        # Procesar archivos
        if os.path.isfile(ruta_item):
            if item.endswith(':Zone.Identifier'):
                try:
                    os.remove(ruta_item)
                    print(f"Eliminado: {ruta_item}")
                except Exception as e:
                    print(f"Error eliminando {ruta_item}: {e}")
        
        # Procesar subcarpetas recursivamente
        elif os.path.isdir(ruta_item):
            eliminar_zone_identifier(ruta_item)

# Especifica la carpeta donde quieres eliminar los archivos
carpeta_objetivo = "/home/cacara/proj/BOHEMIA"
eliminar_zone_identifier(carpeta_objetivo)