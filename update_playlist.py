import requests

# URL playlist principale
source_url = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/main/paratv.m3u"

# Lista canali da aggiornare: la chiave è come appare nel #EXTINF, case sensitive!
channels_to_update = [
    "TF1 [tf1.fr]",
    "TF1 Series Films [tf1.fr]",
    "TMC [tf1.fr]",
    "46. ARTE [1080p-tf1.fr]",
    "LCI [tf1.fr]",
    "La Chaîne L'Équipe [tf1.fr]"
]

def estrai_link_parte(link):
    # Prende la parte dopo "main/"
    if "main/" in link:
        return link.split("main/")[1]
    else:
        return link.strip()

def aggiorna_playlist_locale(input_file, output_file):
    # Legge la playlist locale
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Scarica la playlist sorgente
    r = requests.get(source_url)
    r.raise_for_status()
    source_lines = r.text.splitlines()

    # Dizionario canale -> link (solo parte dopo main/)
    source_links = {}

    # Parsing playlist sorgente
    for i in range(len(source_lines)):
        line = source_lines[i]
        if line.startswith("#EXTINF"):
            for ch in channels_to_update:
                if ch in line:
                    # Link è la riga dopo
                    if i + 1 < len(source_lines):
                        link = source_lines[i + 1]
                        source_links[ch] = estrai_link_parte(link)

    # Ora aggiorniamo lines (playlist locale)
    updated_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            updated_lines.append(line)
            # Controllo se questa riga contiene un canale che vogliamo aggiornare
            updated = False
            for ch in channels_to_update:
                if ch in line:
                    # Se il canale è in source_links aggiorno la riga successiva
                    if ch in source_links:
                        # Sostituisco la riga successiva con il nuovo link "main/..."
                        new_link = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/main/" + source_links[ch]
                        updated_lines.append(new_link + "\n")
                        i += 2
                        updated = True
                        break
            if not updated:
                # Canale non da aggiornare, copio la riga successiva originale
                if i + 1 < len(lines):
                    updated_lines.append(lines[i+1])
                i += 2
        else:
            updated_lines.append(line)
            i += 1

    # Scrivo il risultato in output_file
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    print(f"Playlist aggiornata scritta in {output_file}")

# Usa la funzione, inserendo i nomi dei file locali
aggiorna_playlist_locale("playlist_locale.m3u", "playlist_locale_aggiornata.m3u")
