#Schritte zum Selbsteinrichten  

##Vorbereitung
Bitte in das Terminal gehen. Es wird wird das Ausführen des Programmes Python benötigt. Im besten Fall mit der Version 3.12.5 oder neuer. Es sollte aber auch mit älteren Versionen funktionieren.  

1. Ein virtuelles python environment erstellen und aktivieren:
```bash
python3 -m venv olymp_venv
source olympic_venv/bin/activate
```

2. Die python packages installieren:
```bash
pip install -r requirements.txt
```

##Ausführen

Der folgende Befehl startet das Dashboard.
```bash
python3 multi_edit.py
```
Das Dashboard ist nun unter zwei Adressen erreichbar auf: http://127.0.0.1:8050 und auf der vergegebenen ip-Adresse des Gerätes http://<lokale ip>:8050
Zum Beenden des Programmes strg+c drücken.

