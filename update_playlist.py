import requests
import re

URL_FONTE = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/main/paratv.m3u"

# Canali esatti da aggiornare: la chiave è il nome esatto che compare in #EXTINF, valore è un tag per sicurezza
CANALI = {
    "TF1": "tf1.fr",
    "TF1 Séries Films": "tf1.fr",
    "TMC": "tf1.fr",
    "Arte": "arte.tv",
    "LCI": "tf1.fr",
    "La Chaîne L'Équipe": "lequipe.fr",
}

# Percorso della playlist da aggiornare
PATH_PLAYLIST = "playlist.m3u"

def scarica_fonte():
    r = requests.get(URL_FONTE)
    r.raise_for_status()
    return r.text

def parse_blocchi(m3u_text):
    lines = m3u_text.splitlines()
    blocchi = []
    blocco_corrente = []
    for line in lines:
        if line.startswith("#EXTINF:"):
            if blocco_corrente:
                blocchi.append(blocco_corrente)
            blocco_corrente = [line]
        elif blocco_corrente:
            blocco_corrente.append(line)
    if blocco_corrente:
        blocchi.append(blocco_corrente)
    return blocchi

def estrai_parte_link(link):
    # Estrae la parte dopo main/
    m = re.search(r"main/(.+)", link)
    return m.group(1) if m else None

def trova_blocchi_interessanti(blocchi):
    """
    Ritorna dict con chiave = nome canale esatto, valore = (EXTINF, link relativo dopo main/)
    """
    result = {}
    for blocco in blocchi:
        extinf = blocco[0]
        if len(blocco) < 2:
            continue
        link = blocco[1]
        for canale, tag in CANALI.items():
            if canale.lower() in extinf.lower() and tag in extinf.lower():
                parte_link = estrai_parte_link(link)
                if parte_link:
                    result[canale] = (extinf, parte_link)
    return result

def aggiorna_playlist_localmente(blocchi_fonte, blocchi_locali):
    # crea dizionario dei blocchi da fonte: nome canale => parte_link
    fonte_canali = trova_blocchi_interessanti(blocchi_fonte)

    nuova_lista = []
    i = 0
    while i < len(blocchi_locali):
        blocco = blocchi_locali[i]
        extinf = blocco[0]
        trovato = False
        for canale in fonte_canali:
            if canale.lower() in extinf.lower():
                # aggiorna solo il link (seconda riga)
                nuova_lista.append([extinf, "https://raw.githubusercontent.com/Paradise-91/ParaTV/main/" + fonte_canali[canale][1]])
                trovato = True
                break
        if not trovato:
            nuova_lista.append(blocco)
        i += 1
    return nuova_lista

def salva_playlist(blocchi, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for blocco in blocchi:
            for line in blocco:
                f.write(line + "\n")

def main():
    # scarico la fonte ufficiale
    fonte = scarica_fonte()
    blocchi_fonte = parse_blocchi(fonte)

    # leggo la playlist locale
    with open(PATH_PLAYLIST, "r", encoding="utf-8") as f:
        locale = f.read()
    blocchi_locale = parse_blocchi(locale)

    # aggiorno la playlist locale con i link nuovi
    nuova_playlist = aggiorna_playlist_localmente(blocchi_fonte, blocchi_locale)

    # salvo la playlist aggiornata
    salva_playlist(nuova_playlist, "playlist_aggiornata.m3u")
    print("Playlist aggiornata e salvata in playlist_aggiornata.m3u")

if __name__ == "__main__":
    main()
