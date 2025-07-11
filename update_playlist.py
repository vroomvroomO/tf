import requests
import re

# Fonte principale
URL_FONTE = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/main/paratv.m3u"

# Lista canali da aggiornare e filtro su 'tf1.fr'
CANALI = {
    "TF1": "TF1",
    "TF1 Séries Films": "TF1 Séries Films",
    "TMC": "TMC",
    "Arte": "Arte",
    "LCI": "LCI",
    "L'Équipe": "L'Équipe",
}

# Prefisso fisso nella tua lista
PREFIX = "https://raw.githubusercontent.com/Paradise-91/ParaTV/main/"

def scarica_fonte():
    r = requests.get(URL_FONTE)
    r.raise_for_status()
    return r.text

def trova_blocchi(testo):
    righe = testo.splitlines()
    blocchi = []
    corrente = []
    for r in righe:
        if r.startswith("#EXTINF:"):
            if corrente:
                blocchi.append(corrente)
            corrente = [r]
        elif corrente:
            corrente.append(r)
    if corrente:
        blocchi.append(corrente)
    return blocchi

def filtra_blocchi(blocchi):
    risultato = {}
    for b in blocchi:
        intest = b[0]
        link = b[1] if len(b) > 1 else ""
        for name_key, display in CANALI.items():
            if display.lower() in intest.lower() and "tf1.fr" in intest.lower():
                risultato[name_key] = b
    return risultato

def sostituisci(dest_path, blocchi_nuovi):
    with open(dest_path, "r", encoding="utf-8") as f:
        righe = f.readlines()

    out = []
    i = 0
    while i < len(righe):
        r = righe[i]
        if r.startswith("#EXTINF:"):
            blk = [r]
            i += 1
            while i < len(righe) and not righe[i].startswith("#EXTINF:"):
                blk.append(righe[i]); i += 1

            key = None
            for k in blocchi_nuovi:
                if k.lower() in blk[0].lower():
                    key = k
            if key:
                out.extend(blocchi_nuovi[key])
            else:
                out.extend(blk)
        else:
            out.append(r)
            i += 1

    with open("playlist_aggiornata.m3u", "w", encoding="utf-8") as f:
        f.writelines(out)

def main():
    src = scarica_fonte()
    blocchi = trova_blocchi(src)
    blocchi_nuovi = filtra_blocchi(blocchi)
    if blocchi_nuovi:
        sostituisci("playlist.m3u", blocchi_nuovi)
    else:
        print("Nessun blocco nuovo trovato.")

if __name__ == "__main__":
    main()
