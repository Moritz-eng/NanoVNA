import os
from PIL import Image, ImageDraw, ImageFont

# Pfad zu deinen Bildern
pfad = os.path.dirname(os.path.abspath(__file__))
ausgabe_datei = "antennen_messreihe_beschriftet.png"

# 1. Dateien filtern (kein "_01")
alle_dateien = [f for f in os.listdir(pfad) if f.lower().endswith('.png') and "_01" not in f]

# Antennen-Fotos (ohne Unterstrich im Namen, z.B. "Laird.jpg")
antennen_fotos = sorted([f for f in alle_dateien if "_" not in f])
# Zustände (Reihenfolge in der Tabelle) - "Haut" wurde zu "m. Körper" umbenannt
zustands_typen = ["Luft", "m. Körper", "Kunststoff", "Metall"]

# 2. Größen und Abstände festlegen
ref_img = Image.open(os.path.join(pfad, antennen_fotos[0]))
w, h = ref_img.size

rand_links = 250  # Mehr Platz für größeren Text
rand_oben = 150   # Mehr Platz für größeren Text
spalten = len(antennen_fotos)
zeilen = 1 + len(zustands_typen)

# Neues Bild mit Platz für Beschriftung erstellen
tabelle = Image.new('RGB', (w * spalten + rand_links, h * zeilen + rand_oben), (255, 255, 255))
draw = ImageDraw.Draw(tabelle)

# Schrift laden - Größere Schriftarten
try:
    font_titel = ImageFont.truetype("arial.ttf", 60)  # Größer: von 45 auf 60
    font_labels = ImageFont.truetype("arial.ttf", 50)  # Größer: von 35 auf 50
except:
    print("Arial-Schrift nicht gefunden, verwende Standardschrift")
    font_titel = font_labels = ImageFont.load_default()

# 3. Tabelle füllen
for col, ant_datei in enumerate(antennen_fotos):
    basis_name = os.path.splitext(ant_datei)[0]
    x_pos = col * w + rand_links
    
    # --- Kopfzeile: Text & Foto ---
    draw.text((x_pos + 10, 30), basis_name, fill=(0, 0, 0), font=font_titel)  # Y-Position angepasst
    img_ant = Image.open(os.path.join(pfad, ant_datei)).resize((w, h))
    tabelle.paste(img_ant, (x_pos, rand_oben))
    
    # --- Die Messreihen ---
    for row, zustand in enumerate(zustands_typen, start=1):
        y_pos = row * h + rand_oben
        
        # Beschriftung links (nur bei der ersten Antenne schreiben)
        if col == 0:
            # Zentrierten Text berechnen (vertikal)
            bbox = font_labels.getbbox(zustand)
            text_height = bbox[3] - bbox[1]
            text_y = y_pos + (h - text_height) // 2
            draw.text((20, text_y), zustand, fill=(0, 0, 0), font=font_labels)
        
        # Messbild einfügen
        # Beachte: Für die Suche nach der Datei muss noch "Haut" verwendet werden, 
        # da die Dateinamen wahrscheinlich noch "Haut" enthalten
        datei_suchname = "Haut" if zustand == "m. Körper" else zustand
        datei_messung = f"{basis_name}_{datei_suchname}.png"
        pfad_mess = os.path.join(pfad, datei_messung)
        
        if os.path.exists(pfad_mess):
            img_m = Image.open(pfad_mess).resize((w, h))
            tabelle.paste(img_m, (x_pos, y_pos))

# 4. Rote Tabellenlinien einzeichnen
linien_farbe = (255, 0, 0)  # Rot
linien_breite = 3

# Vertikale Linien (zwischen den Spalten)
for col in range(spalten + 1):
    x = col * w + rand_links
    draw.line([(x, rand_oben), (x, rand_oben + h * zeilen)], fill=linien_farbe, width=linien_breite)

# Horizontale Linien (zwischen den Zeilen)
for row in range(zeilen + 1):
    y = row * h + rand_oben
    draw.line([(rand_links, y), (rand_links + w * spalten, y)], fill=linien_farbe, width=linien_breite)

# Äußere Umrandung der Tabelle
draw.rectangle(
    [(rand_links, rand_oben), (rand_links + w * spalten, rand_oben + h * zeilen)], 
    outline=linien_farbe, 
    width=linien_breite
)

# 5. Speichern
tabelle.save(ausgabe_datei)
print(f"Fertig! Die Tabelle mit Beschriftung wurde gespeichert: {ausgabe_datei}")
print(f"Bildgröße: {tabelle.size}")