# zakb Jahreskalender Downoad
## Docker Container für ICS / Ical Download

Wer in der Gegend um Viernheim lebt und den Ical Kalender für eine Hausautomation wie bspw ioBroker braucht, der kann leider nicht direkt ein ICS File mit den Abholterminen runterladen. Das liegt an der seltsamen Umsetzung des Downloads von zakb mit einem Typo3 Formular, welches auch noch mit Sessions arbeitet.
Eigentlich sollte das nur einmal im Jahr notwendig sein aber es ging mir auf den Keks, das bei jeder Neuinstallation zu machen. Daher hier als Docker Version. Damit kann man das einfach zusammen mit ioBroker, HomeAssistant oder sonst was, in ein docker-compose File packen und gut ist. Damit ist auch ein Backup und dessen Wiederherstellung kein Problem mehr.
Da ist als Familien-Admin jetzt auch nicht überalle einfach nur eine Datei ablegen will, habe ich den Container erstellt.

## Features

- Läuft in einer Schleife und ruft einmal täglich die Datei für das aktuelle Jahr ab
- Sollte die zakb Seite (mal wieder) spinnen, dann wird nach einer Stunde wieder versucht
- Konstanter Dateiname calendar.ics (am besten per Bind mappen!)
- Konfiguration der Adresse über Umgebungsvariablen

## Docker
### Dockerfile
```
FROM python:3

WORKDIR /usr/src/app
ENV ENV_CITY Viernheim
ENV ENV_STREET Am Hofböhl
ENV ENV_HOUSENO 1
VOLUME /usr/src/app/calendar.ics


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./muell.py" ]
```

Einfach die ENV Variablen auf die aktuelle Adresse setzen und die calendar.ics Datei auf eine lokale Datei mappen. Dann wird einmal täglich eine neue Kopie des aktuellen Jahreskalenders heruntergeladen. Im Fehlerfall wird nach 60 Minuten nochmal versucht.
