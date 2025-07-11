import requests

URL_FONTE = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/main/paratv.m3u"
FILE_LOCALE = "playlist.m3u"
FILE_AGGIORNATA = "playlist_aggiornata.m3u"

def scarica_playlist_fonte(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

def estrai_canali_fonte(righe_fonte):
    canali = {}
    i = 0
    while i < len(righe_fonte):
        if righe_fonte[i].startswith("#EXTINF"):
            nome = righe_fonte[i].split(",",1)[1].strip()
            url = righe_fonte[i+1].strip()
            # Prendo solo la parte dell'url dopo "/main/"
            parte_url = url.split("/main/")[-1]
            url_pulito = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/main/" + parte_url
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
            nome_locale = riga.split(",",1)[1].strip()
            righe_aggiornate.append(riga)

            url_locale = righe_locale[i+1].strip()

            # Cerco nella fonte un canale che contiene nome_locale e la stringa chiave (es: 'tf1.fr', 'arte', ecc.)
            url_nuovo = None
            for nome_fonte, url in canali_fonte.items():
                # Prendo la parte in parentesi quadre nel nome_fonte per sapere qual è la stringa chiave
                # esempio: "TF1 [720p-tf1.fr]" -> cerca se nome_locale in nome_fonte e 'tf1.fr' in nome_fonte
                if nome_locale in nome_fonte:
                    # Estraggo la parte tra parentesi quadre, se presente
                    start = nome_fonte.find('[')
                    end = nome_fonte.find(']')
                    if start != -1 and end != -1:
                        tag = nome_fonte[start+1:end].lower()
                        # Ad esempio se nome_locale è TF1 cerco "tf1.fr" nel tag
                        if nome_locale.lower() in nome_fonte.lower() and nome_locale.lower() in tag:
                            url_nuovo = url
                            break
                    else:
                        # Se non ci sono parentesi, accetto se il nome_locale è contenuto
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
