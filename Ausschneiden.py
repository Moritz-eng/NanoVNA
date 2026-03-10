import os
from PIL import Image
import glob

# Zielgröße
TARGET_WIDTH = 1572
TARGET_HEIGHT = 821
TARGET_ASPECT = TARGET_WIDTH / TARGET_HEIGHT

# Finde alle JPEG-Dateien im aktuellen Verzeichnis
jpeg_files = glob.glob("*.jpeg") + glob.glob("*.jpg") + glob.glob("*.JPEG") + glob.glob("*.JPG")

for jpeg_file in jpeg_files:
    try:
        # Öffne das Bild
        with Image.open(jpeg_file) as img:
            orig_width, orig_height = img.size
            orig_aspect = orig_width / orig_height
            
            # Berechne den Beschnitt, um das Seitenverhältnis anzupassen
            if orig_aspect > TARGET_ASPECT:
                # Bild ist breiter als Ziel - beschneide die Breite
                new_width = int(orig_height * TARGET_ASPECT)
                left = (orig_width - new_width) // 2
                right = left + new_width
                cropped_img = img.crop((left, 0, right, orig_height))
                print(f"  - Beschneide Breite von {orig_width}px auf {new_width}px")
            else:
                # Bild ist höher als Ziel - beschneide die Höhe
                new_height = int(orig_width / TARGET_ASPECT)
                top = (orig_height - new_height) // 2
                bottom = top + new_height
                cropped_img = img.crop((0, top, orig_width, bottom))
                print(f"  - Beschneide Höhe von {orig_height}px auf {new_height}px")
            
            # Jetzt haben wir das richtige Seitenverhältnis und können gleichmäßig skalieren
            resized_img = cropped_img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
            
            # Speichern
            png_filename = os.path.splitext(jpeg_file)[0] + ".png"
            resized_img.save(png_filename, "PNG", optimize=True)
            
            print(f"Erfolgreich konvertiert: {jpeg_file} -> {png_filename}")
            print(f"  - Seitenverhältnis: {orig_aspect:.2f} -> {TARGET_ASPECT:.2f}")
            print(f"  - Gleichmäßig skaliert auf: {TARGET_WIDTH}x{TARGET_HEIGHT}")
            
    except Exception as e:
        print(f"Fehler bei {jpeg_file}: {e}")

print("\nFertig!")