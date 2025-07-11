import requests

URL_FONTE = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/main/paratv.m3u"
FILE_LOCALE = "playlist.m3u"
FILE_AGGIORNATA = "playlist_aggiornata.m3u"

KEYWORDS_CANALI = {
    "TF1": "tf1.fr",
    "Arte": "tf1.fr",
    "TMC": "tf1.fr",
    "LCI": "tf1.fr",
    "La Chaîne L'Équipe": "tf1.fr",
    "TF1 Series Films": "tf1.fr"
}

def scarica_playlist_fonte(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

def estrai_canali_fonte(righe_fonte):
    canali = {}
    i = 0
    while i < len(righe_fonte):
        if righe_fonte[i].startswith("#EXTINF"):
            nome = righe_fonte[i].split(",", 1)[1].strip()
            url = righe_fonte[i+1].strip()

            idx = url.find("/refs/")
            if idx != -1:
                parte_url = url[idx:]  # includo "/refs/..."
                url_pulito = "https://raw.githubusercontent.com/Paradise-91/ParaTV" + parte_url
            else:
                url_pulito = url  # fallback se non trova /refs/

            canali[nome] = url_pulito
            i += 2
        else:
            i += 1
    return canali

def aggiorna_playlist_locale(input_file, output_file, canali_fonte):
    with open(input_file, "r", encoding="utf-8") as f:
        righe_locale = f.readlines()

    righe_aggiornate = []
    i = 0
    while i < len(righe_locale):
        riga = righe_locale[i]

        if riga.startswith("#EXTINF"):
            nome_locale = riga.split(",", 1)[1].strip()
            righe_aggiornate.append(riga)

            url_locale = righe_locale[i+1].strip()

            keyword = None
            for k in KEYWORDS_CANALI.keys():
                if nome_locale.lower() == k.lower():
                    keyword = KEYWORDS_CANALI[k].lower()
                    break

            url_nuovo = None
            if keyword:
                for nome_fonte, url in canali_fonte.items():
                    if nome_locale.lower() in nome_fonte.lower() and keyword in nome_fonte.lower():
                        url_nuovo = url
                        break
            else:
                for nome_fonte, url in canali_fonte.items():
                    if nome_locale.lower() in nome_fonte.lower():
                        url_nuovo = url
                        break

            if url_nuovo:
                righe_aggiornate.append(url_nuovo + "\n")
            else:
                righe_aggiornate.append(righe_locale[i+1])

            i += 2
        else:
            righe_aggiornate.append(riga)
            i += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(righe_aggiornate)

def main():
    righe_fonte = scarica_playlist_fonte(URL_FONTE)
    canali_fonte = estrai_canali_fonte(righe_fonte)
    aggiorna_playlist_locale(FILE_LOCALE, FILE_AGGIORNATA, canali_fonte)
    print(f"Playlist aggiornata salvata in {FILE_AGGIORNATA}")

if __name__ == "__main__":
    main()
