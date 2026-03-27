import kagglehub
import shutil
import os

print("Downloading dataset...")
path = kagglehub.dataset_download("davidcariboo/player-scores")
print("Path to dataset files:", path)
print("Files:", os.listdir(path))

# Copy files to data folder
dest = r"c:\Users\adria\OneDrive\Documentos\Clase\DAW\proyecte\ProjecteBarca\data"
os.makedirs(dest, exist_ok=True)
for item in os.listdir(path):
    s = os.path.join(path, item)
    d = os.path.join(dest, item)
    if os.path.isfile(s):
        shutil.copy2(s, d)
        print(f"Copied {item} to {dest}")
print(f"All files copied to {dest}")
