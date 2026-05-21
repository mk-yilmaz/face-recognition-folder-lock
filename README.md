# face-recognition-folder-lock

##🇬🇧 English Version
# Raspberry Pi Face Recognition Folder Unlock

A Raspberry Pi project that uses real-time face recognition with Picamera2 and OpenCV to automatically show or hide a private folder.

The system detects faces using Haar Cascade and verifies identities with the `face_recognition` library.
If the authorized person is detected, the private folder becomes visible automatically.
If the face disappears for a few seconds, the folder is hidden again.

The project is optimized for Raspberry Pi performance:

* Low camera resolution
* Faster frame processing
* Buffered recognition logic
* Stable real-time detection

Technologies used:

* Python
* OpenCV
* Picamera2
* face_recognition
* Raspberry Pi OS

This project is designed for learning computer vision, Raspberry Pi optimization, and real-time face authentication.


##DE  German Version
# Raspberry Pi Gesichtserkennung für private Ordner

Dieses Projekt verwendet eine Raspberry Pi Kamera, OpenCV und Gesichtserkennung, um einen privaten Ordner automatisch sichtbar oder unsichtbar zu machen.

Das System erkennt Gesichter mit einer Haar Cascade und überprüft die Identität mit der `face_recognition` Bibliothek.

Wenn die autorisierte Person erkannt wird:

* wird der private Ordner automatisch geöffnet.

Wenn das Gesicht einige Sekunden nicht mehr erkannt wird:

* wird der Ordner automatisch wieder versteckt.

Das Projekt wurde speziell für den Raspberry Pi optimiert:

* niedrige Kameraauflösung
* schnellere Bildverarbeitung
* stabile Echtzeit-Erkennung
* Puffer gegen Flackern

Verwendete Technologien:

* Python
* OpenCV
* Picamera2
* face_recognition
* Raspberry Pi OS

Das Projekt eignet sich gut zum Lernen von:

* Computer Vision
* Gesichtserkennung
* Raspberry Pi Optimierung
* Echtzeit-Videoverarbeitung

