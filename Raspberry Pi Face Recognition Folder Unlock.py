from picamera2 import Picamera2
import cv2
import face_recognition
import os
import subprocess
import time

# =========================
# EINSTELLUNGEN
# =========================

PROFIL_NAME = "Erkannt"
TOLERANZ = 0.5

SICHTBAR = "/home/admin/Desktop/Privat"
VERSTECKT = "/home/admin/Desktop/.Privat"

PUFFER_ZEIT = 2.0  # Sekunden bis Ordner wieder verschwindet

# =========================
# ORDNER FUNKTIONEN
# =========================

ordner_ist_da = False

def ordner_sichtbar_machen():
    if os.path.exists(VERSTECKT):
        os.rename(VERSTECKT, SICHTBAR)
        subprocess.Popen(['pcmanfm', SICHTBAR])

def ordner_unsichtbar_machen():
    os.system("pkill pcmanfm")

    if os.path.exists(SICHTBAR):
        os.rename(SICHTBAR, VERSTECKT)

# =========================
# HAAR CASCADE
# =========================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)

# =========================
# KAMERA SETUP
# =========================

picam2 = Picamera2()

picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (320, 240)}
    )
)

picam2.start()

# =========================
# REFERENZBILD LADEN
# =========================

print("Lade Referenzbild...")

bild = face_recognition.load_image_file(
    "/home/admin/Desktop/profilbild.jpg"
)

encodings = face_recognition.face_encodings(bild)

if len(encodings) == 0:
    print("Kein Gesicht im Referenzbild gefunden!")
    exit()

referenz_encoding = encodings[0]

print("Erkennung gestartet")

# =========================
# HAUPTSCHLEIFE
# =========================

frame_count = 0
zeit_letzte_erkennung = 0

try:

    while True:

        frame = picam2.capture_array()

        frame_count += 1

        erkannt = False

        # Graubild
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Gesicht finden
        gesichter = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        for (x, y, w, h) in gesichter:

            # Gesicht ausschneiden
            gesicht = frame[y:y+h, x:x+w]

            # RGB
            rgb_gesicht = cv2.cvtColor(
                gesicht,
                cv2.COLOR_BGR2RGB
            )

            # Nur jedes 5. Frame KI berechnen
            if frame_count % 5 == 0:

                encodings = face_recognition.face_encodings(
                    rgb_gesicht
                )

                if encodings:

                    abstand = face_recognition.face_distance(
                        [referenz_encoding],
                        encodings[0]
                    )[0]

                    sicherheit = (1 - abstand) * 100

                    if abstand < TOLERANZ:

                        erkannt = True

                        zeit_letzte_erkennung = time.time()

                        text = f"{PROFIL_NAME} ({sicherheit:.1f}%)"

                        farbe = (0, 255, 0)

                    else:

                        text = "Unbekannt"

                        farbe = (0, 0, 255)

                else:

                    text = "Kein Gesicht"

                    farbe = (0, 0, 255)

            else:
                # Zwischenframes
                text = "Suche..."
                farbe = (255, 255, 0)

            # Rechteck
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                farbe,
                2
            )

            # Text
            cv2.putText(
                frame,
                text,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                farbe,
                2
            )

        # =========================
        # ORDNER LOGIK
        # =========================

        aktuelle_zeit = time.time()

        if erkannt:

            if not ordner_ist_da:

                ordner_sichtbar_machen()

                ordner_ist_da = True

                print("Ordner sichtbar")

        else:

            if ordner_ist_da:

                if aktuelle_zeit - zeit_letzte_erkennung > PUFFER_ZEIT:

                    ordner_unsichtbar_machen()

                    ordner_ist_da = False

                    print("Ordner versteckt")

        # =========================
        # VIDEO ANZEIGE
        # =========================

        cv2.imshow("Gesichtserkennung", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:

    picam2.stop()

    ordner_unsichtbar_machen()

    cv2.destroyAllWindows()
