# Schritte zum Selbsteinrichten  

## Vorbereitung
Bitte das Terminal öffnen und in das Verzeichnis, wohin die Dateien heruntergeladen wurden, gehen. Es wird wird zum Ausführen des Programmes Python benötigt. Im besten Fall mit der Version 3.12.5 oder neuer. Es sollte aber auch mit älteren Versionen funktionieren.  

1. Ein virtuelles python environment erstellen und aktivieren:

für Linux:
```bash
python3 -m venv olympic_venv
source olympic_venv/bin/activate
```
für Windows (Powershell):
```bash
python -m venv olympic_venv
.\olympic_venv\Scripts\Activate
```

2. Die python packages installieren:
```bash
pip install -r requirements.txt
```

## Ausführen

Der folgende Befehl startet das Dashboard.
```bash
python3 multi_edit.py
```
Das Dashboard ist nun unter zwei Adressen erreichbar auf: http://127.0.0.1:8050 und auf der vergegebenen ip-Adresse des Gerätes http://"lokaleip":8050

Zum Beenden des Programmes bitte strg+c drücken.

