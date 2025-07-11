{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import requests\
import re\
\
url_fonte = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/main/paratv.m3u"\
\
r = requests.get(url_fonte)\
lista_fonte = r.text\
\
def trova_link_relativo(canale, testo):\
    pattern = re.compile(rf'#EXTINF:.*\{canale\}.*\\n(https://raw\\.githubusercontent\\.com/Paradise-91/ParaTV/main/(.*))')\
    match = pattern.search(testo)\
    if match:\
        return match.group(2).strip()\
    else:\
        return None\
\
link_tf1_rel = trova_link_relativo("TF1", lista_fonte)\
link_tfx_rel = trova_link_relativo("TFX", lista_fonte)\
\
if not link_tf1_rel or not link_tfx_rel:\
    print("Errore: link relativi TF1 o TFX non trovati nella lista fonte")\
    exit(1)\
\
prefisso = "https://raw.githubusercontent.com/Paradise-91/ParaTV/main/"\
\
with open("playlist.m3u", "r", encoding="utf-8") as f:\
    lista_personale = f.read()\
\
def sostituisci_link_relativo(canale, nuovo_path_rel, testo):\
    pattern = re.compile(rf'(#EXTINF:.*\{canale\}.*\\n)\{re.escape(prefisso)\}.*')\
    return pattern.sub(rf'\\1\{prefisso\}\{nuovo_path_rel\}', testo)\
\
lista_personale = sostituisci_link_relativo("TF1", link_tf1_rel, lista_personale)\
lista_personale = sostituisci_link_relativo("TFX", link_tfx_rel, lista_personale)\
\
with open("playlist_aggiornata.m3u", "w", encoding="utf-8") as f:\
    f.write(lista_personale)\
}