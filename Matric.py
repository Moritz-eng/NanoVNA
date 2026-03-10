import os
from PIL import Image, ImageDraw, ImageFont

# Pfad zu deinen Bildern
pfad = os.path.dirname(os.path.abspath(__file__))
ausgabe_datei = "antennen_messreihe_01_beschriftet.png"

# 1. Dateien filtern (nur mit "_01")
alle_dateien = [f for f in os.listdir(pfad) if f.lower().endswith('.png') and "_01" in f]

# Antennen-Fotos (ohne Unterstrich im Namen, z.B. "Laird.png") - gleiche wie vorher
antennen_fotos = sorted([f for f in os.listdir(pfad) if f.lower().endswith('.png') and "_" not in f])
# Zustände (Reihenfolge in der Tabelle)
zustands_typen = ["Luft", "m. Körper", "Kunststoff", "Metall"]

# Prüfen ob Antennen-Fotos vorhanden
if not antennen_fotos:
    print("Keine Antennen-Fotos gefunden!")
    exit()

# 2. Größen und Abstände festlegen
ref_img = Image.open(os.path.join(pfad, antennen_fotos[0]))
w, h = ref_img.size

rand_links = 250  # Platz für Zustands-Namen
rand_oben = 150   # Platz für Antennen-Namen
spalten = len(antennen_fotos)
zeilen = 1 + len(zustands_typen)

print(f"Gefundene Antennen: {antennen_fotos}")
print(f"Erstelle Tabelle für Messreihe 01 mit {spalten} Spalten und {zeilen} Zeilen")

# Neues Bild mit Platz für Beschriftung erstellen
tabelle = Image.new('RGB', (w * spalten + rand_links, h * zeilen + rand_oben), (255, 255, 255))
draw = ImageDraw.Draw(tabelle)

# Schrift laden - Größere Schriftarten
try:
    font_titel = ImageFont.truetype("arial.ttf", 60)
    font_labels = ImageFont.truetype("arial.ttf", 50)
except:
    print("Arial-Schrift nicht gefunden, verwende Standardschrift")
    font_titel = font_labels = ImageFont.load_default()

# 3. Tabelle füllen
for col, ant_datei in enumerate(antennen_fotos):
    basis_name = os.path.splitext(ant_datei)[0]
    x_pos = col * w + rand_links
    
    # --- Kopfzeile: Text & Foto ---
    draw.text((x_pos + 10, 30), basis_name, fill=(0, 0, 0), font=font_titel)
    img_ant = Image.open(os.path.join(pfad, ant_datei)).resize((w, h))
    tabelle.paste(img_ant, (x_pos, rand_oben))
    
    # --- Die Messreihen mit _01 ---
    for row, zustand in enumerate(zustands_typen, start=1):
        y_pos = row * h + rand_oben
        
        # Beschriftung links (nur bei der ersten Antenne schreiben)
        if col == 0:
            # Zentrierten Text berechnen (vertikal)
            bbox = font_labels.getbbox(zustand)
            text_height = bbox[3] - bbox[1]
            text_y = y_pos + (h - text_height) // 2
            draw.text((20, text_y), zustand, fill=(0, 0, 0), font=font_labels)
        
        # Messbild mit _01 einfügen
        # Für die Dateisuche wird "Haut" verwendet (wegen vorhandener Dateien)
        datei_suchname = "Haut" if zustand == "m. Körper" else zustand
        datei_messung = f"{basis_name}_{datei_suchname}_01.png"
        pfad_mess = os.path.join(pfad, datei_messung)
        
        if os.path.exists(pfad_mess):
            img_m = Image.open(pfad_mess).resize((w, h))
            tabelle.paste(img_m, (x_pos, y_pos))
            print(f"  + Gefunden: {datei_messung}")
        else:
            # Alternativ auch als JPG probieren
            datei_messung_jpg = f"{basis_name}_{datei_suchname}_01.jpg"
            pfad_mess_jpg = os.path.join(pfad, datei_messung_jpg)
            if os.path.exists(pfad_mess_jpg):
                img_m = Image.open(pfad_mess_jpg).resize((w, h))
                tabelle.paste(img_m, (x_pos, y_pos))
                print(f"  + Gefunden: {datei_messung_jpg}")
            else:
                print(f"  - Nicht gefunden: {basis_name}_{datei_suchname}_01")

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

# 5. Überschrift für Messreihe 01 hinzufügen
try:
    font_uberschrift = ImageFont.truetype("arial.ttf", 80)
    uberschrift = "Messreihe 01"
    bbox = font_uberschrift.getbbox(uberschrift)
    text_width = bbox[2] - bbox[0]
    # Zentriert über der Tabelle
    draw.text(((w * spalten + rand_links - text_width) // 2, 20), uberschrift, fill=(255, 0, 0), font=font_uberschrift)
except:
    pass  # Falls Schrift nicht geladen werden kann, einfach überspringen

# 6. Speichern
tabelle.save(ausgabe_datei)
print(f"\nFertig! Die Tabelle für Messreihe 01 wurde gespeichert: {ausgabe_datei}")
print(f"Bildgröße: {tabelle.size}")