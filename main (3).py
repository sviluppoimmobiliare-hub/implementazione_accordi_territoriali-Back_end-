

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from città import bergamo, firenze, bari, lecce, pescara, siena, ancona
from città import torino, foggia, brescia, pisa, genova

app = FastAPI()

#CORS decorativo al momento, non ho idea se sia necessario
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro delle città disponibili: id -> modulo della città
# Serve per gli endpoint "generici" (elenco e info)
CITTA_DISPONIBILI = {
    "bari": bari,
    "lecce": lecce,
    "pescara": pescara,
    "siena": siena,
    "ancona": ancona,
    "bergamo": bergamo,
    "firenze": firenze,
    "torino": torino,
    "foggia": foggia,
    "brescia": brescia,
    "pisa": pisa,
    "genova": genova,
}


# ENDPOINTS

#endopoint per il menù a tendina iniziale dove si seleziona la città
@app.get("/citta")
def elenco_citta():

    elenco = []
    for id_citta, modulo in CITTA_DISPONIBILI.items():
        elenco.append({
            "id": id_citta,
            "nome": modulo.INFO["nome"],
            "info": f"/citta/{id_citta}/info",
            "calcolo": f"/calcola/{id_citta}",
        })
    return elenco

#in /info c'è tutto quello che serve  per costruire il form di una città

@app.get("/citta/{id_citta}/info")
def info_citta(id_citta: str):

    if id_citta not in CITTA_DISPONIBILI:
        raise HTTPException(status_code=404, detail=f"Citta' '{id_citta}' non disponibile")
    return CITTA_DISPONIBILI[id_citta].INFO



# ENDPOINT DI CALCOLO sulla base del modello di risposta per ogni città

@app.post("/calcola/bergamo")
def calcola_bergamo(dati: bergamo.InputBergamo):
    return bergamo.calcola(dati)


@app.post("/calcola/firenze")
def calcola_firenze(dati: firenze.InputFirenze):
    return firenze.calcola(dati)


@app.post("/calcola/bari")
def calcola_bari(dati: bari.InputBari):
    return bari.calcola(dati)


#piccolo appunto per lecce
@app.post("/calcola/lecce")
def calcola_lecce(dati: lecce.InputLecce):
    return lecce.calcola(dati)
#a lecce c'è direttamente lo stradario nell'accordo, l'idea è che il front chiami
#questo endpoint mentre l'utente digita
@app.get("/citta/lecce/zona")
def zona_lecce(via: str):
    return lecce.trova_zona(via)

@app.post("/calcola/pescara")
def calcola_pescara(dati: pescara.InputPescara):
    return pescara.calcola(dati)


@app.post("/calcola/siena")
def calcola_siena(dati: siena.InputSiena):
    return siena.calcola(dati)


@app.post("/calcola/ancona")
def calcola_ancona(dati: ancona.InputAncona):
    return ancona.calcola(dati)


#piccolo appunto per torino
@app.post("/calcola/torino")
def calcola_torino(dati: torino.InputTorino):
    return torino.calcola(dati)
#come a lecce c'è lo stradario nell'accordo: il front chiama questo endpoint mentre
#l'utente digita e riceve il nome esatto della via, i tratti di civici e la zona
@app.get("/citta/torino/zona")
def zona_torino(via: str):
    return torino.trova_zona(via)


@app.post("/calcola/foggia")
def calcola_foggia(dati: foggia.InputFoggia):
    return foggia.calcola(dati)


@app.post("/calcola/brescia")
def calcola_brescia(dati: brescia.InputBrescia):
    return brescia.calcola(dati)


@app.post("/calcola/pisa")
def calcola_pisa(dati: pisa.InputPisa):
    return pisa.calcola(dati)


@app.post("/calcola/genova")
def calcola_genova(dati: genova.InputGenova):
    return genova.calcola(dati)



