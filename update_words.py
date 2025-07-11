{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import requests\
\
url = "https://esempio.com/parole.txt"  # <-- cambia con il tuo URL reale\
\
response = requests.get(url)\
text = response.text.strip()\
\
# Estrai la parola dopo "Giovanni"\
if text.startswith("Giovanni "):\
    parola = text.split(" ", 1)[1].strip()\
else:\
    parola = "[ERRORE] formato inatteso"\
\
with open("words.txt", "w", encoding="utf-8") as f:\
    f.write(parola)\
}