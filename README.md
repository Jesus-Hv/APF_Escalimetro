# APF-3: Detector de escalímetro con Haar Cascade

**Autor:** Jesús Huamán Velásquez
**Universidad:** Universidad Tecnológica del Perú (UTP) – Ingeniería Civil

Proyecto individual de Visión Computacional aplicada a Ingeniería Civil. Se entrena un clasificador Haar Cascade para detectar un **escalímetro** en tiempo real con OpenCV y DroidCam/webcam.

## Estructura del repositorio

```
├── APF3_JesusHuaman.py        # Detector en tiempo real
├── cascade.xml                # Modelo entrenado (Cascade Trainer GUI)
├── p/                         # Dataset positivo (imágenes con el escalímetro)
├── n/                         # Dataset negativo (imágenes sin el escalímetro)
├── pos.lst / neg.lst          # Listas de muestras
├── pos_samples.vec            # Muestras positivas generadas
├── Detector_escalimetro_p.py  # Captura de imágenes positivas
├── Detector_escalimetro_n.py  # Captura de imágenes negativas
└── resultados/                # Capturas de la detección
```

## Dataset

- **Positivo (p):** 101 imágenes del escalímetro, recortadas de la región de interés (895×145 px) y redimensionadas a 38×6 px.
- **Negativo (n):** 227 imágenes de fondos sin el objeto.
- Capturadas por mí con DroidCam variando distancia, iluminación, ángulo y fondo.

## Entrenamiento

1. Captura de imágenes con `Detector_escalimetro_p.py` y `Detector_escalimetro_n.py` (tecla `s`).
2. Generación de muestras (`pos_samples.vec`) en Cascade Trainer GUI.
3. Entrenamiento con Cascade Trainer GUI:
   - Tipo de característica: HAAR, boost GAB
   - Tamaño de ventana: 38 × 6
   - Etapas: 3
   - minHitRate 0.995, maxFalseAlarm 0.5
4. Resultado: `cascade.xml`.

## Uso

```bash
pip install opencv-python
python APF3_JesusHuaman.py
```

Edita `FUENTE_VIDEO` en el script con la IP de DroidCam (o usa `0` para webcam).
Teclas: `ESC` salir, `s` guardar captura en `resultados/`.

## Parámetros de detección

| Parámetro | Valor |
|---|---|
| scaleFactor | 5 |
| minNeighbors | 91 |
| minSize | (70, 78) |

## Resultados

_Agregar aquí capturas de `resultados/` y el conteo de detecciones correctas, falsos positivos y falsos negativos._

## Aplicaciones en Ingeniería Civil

- Verificación de que se cuenta con la herramienta de medición en laboratorio/obra.
- Base para sistemas de inventario y control de herramientas en obra.
- Punto de partida para detectar otros objetos de seguridad/construcción (EPP, materiales).

## Limitaciones y mejoras

- Haar Cascade es sensible a iluminación, ángulo y fondo.
- Mejoras: más muestras con mayor variedad, más etapas de entrenamiento, o migrar a modelos como YOLO.
