import requests
import re

URL_FONTE = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/main/paratv.m3u"

CANALI_INTERESSATI = [
    "TF1 [tf1.fr]",
    "TF1 Series Films [tf1.fr]",
    "TMC [tf1.fr]",
    "46. ARTE [1080p-tf1.fr]",
    "LCI [tf1.fr]",
    "La Chaîne L'Équipe [tf1.fr]"
]

def scarica_playlist():
    r = requests.get(URL_FONTE)
    r.raise_for_status()
    return r.text

def estrai_url_dopo_main(url_completo):
    m = re.search(r"/main/(.+)$", url_completo)
    if m:
        return m.group(1)
    return url_completo

def aggiorna_playlist_locale(input_file, output_file):
    playlist_fonte = scarica_playlist()

    canali_fonte = {}
    righe = playlist_fonte.splitlines()
    i = 0
    while i < len(righe):
        if righe[i].startswith("#EXTINF"):
            nome = righe[i].split(",", 1)[1].strip()
            url = righe[i+1].strip()
            canali_fonte[nome] = url
            i += 2
        else:
            i += 1

    with open(input_file, "r", encoding="utf-8") as f:
        righe_locale = f.readlines()

    righe_aggiornate = []
    i = 0
    while i < len(righe_locale):
        riga = righe_locale[i]

        if riga.startswith("#EXTINF"):
            nome_canale = riga.split(",", 1)[1].strip()
            righe_aggiornate.append(riga)

            if nome_canale in CANALI_INTERESSATI and "tf1.fr" in nome_canale:
                url_originale = canali_fonte.get(nome_canale)
                if url_originale:
                    url_nuovo = estrai_url_dopo_main(url_originale)
                    righe_aggiornate.append(url_nuovo + "\n")
                else:
                    righe_aggiornate.append(righe_locale[i+1])
            else:
                righe_aggiornate.append(righe_locale[i+1])

            i += 2
        else:
            righe_aggiornate.append(riga)
            i += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(righe_aggiornate)

if __name__ == "__main__":
    aggiorna_playlist_locale("playlist.m3u", "playlist_aggiornata.m3u")
