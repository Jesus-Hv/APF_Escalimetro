import cv2

#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap = cv2.VideoCapture("http://10.217.240.78:4747/video")
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

CascoBClassif = cv2.CascadeClassifier('cascade.xml')

escala = 0.5   # detecta en una imagen a la mitad de tamaño

while True:

    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_chico = cv2.resize(gray, None, fx=escala, fy=escala)

    toy = CascoBClassif.detectMultiScale(gray_chico, scaleFactor=1.2, minNeighbors=450, minSize=(100,100), maxSize=(220,220))

    for (x,y,w,h) in toy:
        x, y, w, h = int(x/escala), int(y/escala), int(w/escala), int(h/escala)

        # ajuste manual del recuadro (en píxeles)
        x = x - 20      # izquierda (-) / derecha (+)
        y = y + 10      # arriba (-) / abajo (+)
        w = w + 90      # más ancho
        h = h + 20       # más alto

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, 'Escalimetro ', (x,y-10), 2, 0.7, (0,255,0), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
