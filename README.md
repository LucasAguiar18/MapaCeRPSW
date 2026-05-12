# MapaCeRPSW

Aplicación de orientación institucional para el tótem interactivo del instituto.

## Estructura del proyecto

- `main.py` - punto de entrada principal.
- `app/gui/main_window.py` - lanzamiento de la aplicación y configuración general.
- `app/scene/scene_view.py` - renderizador 3D Panda3D y sistema de interacción.
- `app/navigation/navigation_manager.py` - destinos, rutas y sistema reutilizable.
- `app/utils/styles.py` - paleta de colores y estilos de interfaz.

## Instalación de dependencias

1. Abre un terminal en la carpeta del proyecto.
2. Crea un entorno virtual opcional:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Instala dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

## Archivo 3D requerido

Coloca el archivo `mapa_cerp.glb` en la raíz del proyecto:

- `c:\Users\Usuario\Downloads\_Tercer_Año_CeRPSW\MapaCeRPSW\mapa_cerp.glb`

## Ejecución

```powershell
python main.py
```

## Características

- Interfaz fullscreen profesional.
- Renderizado 3D con `panda3d` y soporte glTF.
- Menú lateral elegante con búsqueda de salones.
- Selección de destinos con ruta animada.
- Destino resaltado con marcador y línea luminosa.
- Navegación de cámara suave con zoom y rotación.
- Diseño modular y fácil de extender.
