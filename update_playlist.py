import requests
import re

URL_FONTE = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/main/paratv.m3u"

def scarica_playlist_fonte():
    response = requests.get(URL_FONTE)
    response.raise_for_status()
    return response.text

def estrai_parte_url(url):
    # Estrae la parte dopo "/main/"
    match = re.search(r'/main/(.+)$', url)
    if match:
        return match.group(1)
    return url

def aggiorna_playlist(input_file, output_file):
    # Leggi la playlist fonte
    fonte = scarica_playlist_fonte()
    righe_fonte = fonte.splitlines()

    # Costruisci dizionario nome_canale -> url_dopo_main
    canali_fonte = {}
    i = 0
    while i < len(righe_fonte):
        if righe_fonte[i].startswith("#EXTINF"):
            nome_canale = righe_fonte[i].split(",",1)[1].strip()
            url = righe_fonte[i+1].strip()
            url_dopo_main = estrai_parte_url(url)
            canali_fonte[nome_canale] = url_dopo_main
            i += 2
        else:
            i += 1

    # Leggi la playlist locale da aggiornare
    with open(input_file, "r", encoding="utf-8") as f:
        righe_locale = f.readlines()

    righe_aggiornate = []
    i = 0
    while i < len(righe_locale):
        riga = righe_locale[i]

        if riga.startswith("#EXTINF"):
            nome_canale = riga.split(",",1)[1].strip()
            righe_aggiornate.append(riga)

            # Riga URL subito dopo
            url_locale = righe_locale[i+1].strip()

            # Se il nome canale contiene "tf1.fr" e esiste nella fonte aggiorna l'URL
            if "tf1.fr" in nome_canale and nome_canale in canali_fonte:
                url_nuovo = canali_fonte[nome_canale]
                righe_aggiornate.append(url_nuovo + "\n")
            else:
                righe_aggiornate.append(righe_locale[i+1])

            i += 2
        else:
            righe_aggiornate.append(riga)
            i += 1

    # Scrivi il file aggiornato
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(righe_aggiornate)

if __name__ == "__main__":
    aggiorna_playlist("playlist.m3u", "playlist_aggiornata.m3u")
