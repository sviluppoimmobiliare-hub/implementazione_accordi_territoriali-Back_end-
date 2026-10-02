# Calcolatore canone concordato - backend

Backend FastAPI che stima il canone concordato (minimo e massimo). Sono i calcolatori che
avevo in Streamlit portati in un'API, i conti sono gli stessi.

Città: bari, lecce, pescara, siena, ancona, bergamo, firenze, torino, foggia, brescia, pisa,
genova.

## Avvio

Dalla cartella dove c'è main.py:

pip install -r requirements.txt

uvicorn main:app --reload

Poi trovi tutto su http://127.0.0.1:8000/docs

## Endpoint

- GET /citta elenco delle città
- GET /citta/{id}/info etichette, opzioni e note per costruire il form
- POST /calcola/{id} il calcolo
- GET /citta/{id}/zona?via=... solo lecce e torino, ricava la zona dalla via

## ATTENZIONE: zone di genova, foggia e brescia

In queste tre città **non c'è uno stradario**, quindi la zona la sceglie l'utente a mano:

- **genova**: solo i codici di zona del Geoportale (tipo C05A, D13)
- **foggia**: Zona 1, 2, 3, 4, con i confini descritti a parole nell'accordo
- **brescia**: le aree con il nome (Centro, San Polo, ecc.) ma senza elenco delle vie

Se l'utente sbaglia zona il canone esce sbagliato senza nessun errore, quindi va preso con le
pinze finché non ci mappi sopra uno stradario. Si può fare come per lecce e torino, il
calcolo non va toccato.

Su genova ci sono altre due cose da confermare: le tre sottofasce le ho ricavate dividendo in
tre parti uguali l'intervallo della zona, e per D41, D41A, D47, D48, D49 il valore massimo
nel file dell'accordo era mezzo coperto da un timbro.

## Note

- Il CORS è aperto a tutti, da sistemare prima di andare online.
- A brescia e genova i valori dell'accordo sono annui.
- I valori sono quelli degli accordi, senza aggiornamento ISTAT.
- Dove l'accordo dice "fino al X%" c'è un campo per la percentuale concordata: se non lo
  mandi prende il massimo.
