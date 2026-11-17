"""
APF-3 - Detector de escalímetro con Haar Cascade (OpenCV)
Autor: Jesús Huamán Velásquez
Curso: Inteligencia Artificial aplicada a Ingeniería Civil - UTP

Descripción
-----------
Carga el modelo `cascade.xml` (entrenado con Cascade Trainer GUI, ventana 38x6 px,
3 etapas, características HAAR) y detecta un escalímetro en tiempo real usando
DroidCam o una webcam.

Teclas
------
  ESC -> salir
  s   -> guardar captura en la carpeta 'resultados/' (evidencia para el informe)
"""

import os
import time
import cv2

# ----------------------------------------------------------------------
# CONFIGURACIÓN
# ----------------------------------------------------------------------
# Fuente de video: DroidCam (IP del celular) o webcam (0)
FUENTE_VIDEO = "http://10.74.182.150:4747/video"   # DroidCam
# FUENTE_VIDEO = 0                                  # Webcam

MODELO = "cascade.xml"
ETIQUETA = "Escalimetro"          # cv2.putText no dibuja tildes ni ñ

# Parámetros de detectMultiScale
# El modelo se entrenó con ventanas de 38x6 px (relación ~6.3:1), generadas a
# partir de recortes de 895x145 px del escalímetro.
SCALE_FACTOR = 5        # salto de escala entre ventanas (ventanas de 38x6 -> x5 -> x25 ...)
MIN_NEIGHBORS = 91      # vecinos mínimos: más alto = menos falsos positivos
MIN_SIZE = (70, 78)     # tamaño mínimo de ventana a considerar

# Margen para ampliar el rectángulo de detección (proporción del ancho/alto)
MARGEN_X = 0.70
MARGEN_Y = 0.40

COLOR = (0, 255, 0)     # verde (BGR)

# ----------------------------------------------------------------------
# INICIALIZACIÓN
# ----------------------------------------------------------------------
clasificador = cv2.CascadeClassifier(MODELO)
if clasificador.empty():
    raise SystemExit(f"No se pudo cargar el modelo '{MODELO}'. Verifica que esté junto al script.")

cap = cv2.VideoCapture(FUENTE_VIDEO)
if not cap.isOpened():
    raise SystemExit("No se pudo abrir la cámara/DroidCam. Revisa la IP o el índice de la webcam.")
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)   # reduce el retraso del stream

os.makedirs("resultados", exist_ok=True)
n_capturas = 0
t_prev = time.time()

# ----------------------------------------------------------------------
# BUCLE PRINCIPAL
# ----------------------------------------------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("No se recibió imagen de la cámara. Finalizando.")
        break

    # Haar Cascade trabaja en escala de grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detecciones = clasificador.detectMultiScale(
        gris,
        scaleFactor=SCALE_FACTOR,
        minNeighbors=MIN_NEIGHBORS,
        minSize=MIN_SIZE,
    )

    alto_img, ancho_img = frame.shape[:2]
    for (x, y, w, h) in detecciones:
        # Ampliar el recuadro para cubrir todo el objeto
        mx, my = int(w * MARGEN_X), int(h * MARGEN_Y)
        x1, y1 = max(x - mx, 0), max(y - my, 0)
        x2, y2 = min(x + w + mx, ancho_img - 1), min(y + h + my, alto_img - 1)

        cv2.rectangle(frame, (x1, y1), (x2, y2), COLOR, 2)
        cv2.putText(frame, ETIQUETA, (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR, 2, cv2.LINE_AA)

    # FPS y número de detecciones (útil para el análisis de resultados)
    t_now = time.time()
    fps = 1.0 / max(t_now - t_prev, 1e-6)
    t_prev = t_now
    cv2.putText(frame, f"FPS: {fps:.1f}  Detecciones: {len(detecciones)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow("APF-3 - Detector de escalimetro", frame)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == 27:                       # ESC
        break
    if tecla == ord('s'):                 # guardar evidencia
        ruta = f"resultados/captura_{n_capturas}.jpg"
        cv2.imwrite(ruta, frame)
        print("Captura guardada:", ruta)
        n_capturas += 1

cap.release()
cv2.destroyAllWindows()
