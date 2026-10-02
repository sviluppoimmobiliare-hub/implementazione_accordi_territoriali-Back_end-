

from typing import Literal, Optional
from pydantic import BaseModel, Field
from fastapi import HTTPException




valori_a2 = {
    "1 - Centro": (33.10, 72.50),
    "2 - Panoramica": (53.10, 92.70),
    "3 - Via Crocifissa": (47.40, 71.10),
    "4 - Via Veneto": (49.80, 72.50),
    "5 - Brescia Due": (46.00, 70.10),
    "6 - Viale Piave": (38.90, 69.20),
    "7 - Q.re Abba / S. Anna": (36.50, 61.20),
    "8 - Fiumicello": (40.50, 61.30),
    "9 - Noce / Folzano": (32.80, 56.90),
    "10 - Vill. Prealpino": (43.00, 59.00),
    "11 - Vill. Badia / Violino": (30.50, 59.90),
    "12 - S. Eufemia": (43.10, 62.70),
    "13 - San Polo": (37.60, 61.90),
    "14 - Casazza": (41.70, 58.60),
    "15/20 - San Polino": (37.20, 57.40)
}

valori_a3 = {
    "1 - Centro": (27.80, 60.90),
    "2 - Panoramica": (53.10, 92.60),
    "3 - Via Crocifissa": (46.50, 69.70),
    "4 - Via Veneto": (43.80, 63.80),
    "5 - Brescia Due": (40.60, 61.80),
    "6 - Viale Piave": (32.30, 57.30),
    "7 - Q.re Abba / S. Anna": (36.60, 61.30),
    "8 - Fiumicello": (38.40, 58.10),
    "9 - Noce / Folzano": (31.60, 54.80),
    "10 - Vill. Prealpino": (41.50, 57.00),
    "11 - Vill. Badia / Violino": (29.80, 58.70),
    "12 - S. Eufemia": (39.20, 57.00),
    "13 - San Polo": (37.20, 61.40),
    "14 - Casazza": (40.50, 57.00),
    "15/20 - San Polino": (35.20, 54.30)
}

LISTA_ZONE = list(valori_a2.keys())

ELEMENTI_MASSIMO = [
    "1. Impianto di riscaldamento autonomo o centralizzato",
    "2. Box o posto auto",
    "3. Cantina o soffitta o solaio ad uso esclusivo e agevolmente fruibile",
    "4. Giardino privato o condominiale, terrazza condominiale attrezzata oppure area "
    "parcabile per ciclomotori e biciclette, ad esempio un cortile",
    "5. Immobile ultimato, ristrutturato oppure sottoposto a manutenzione costante "
    "negli ultimi 10 anni",
    "6. Classe di efficienza energetica non inferiore alla D"
]

ETICHETTA_ASCENSORE = "7. Presenza di ascensore"

NOTA_ASCENSORE = ("7. Ascensore: richiesto solo per gli edifici superiori a due piani fuori terra e "
                  "per le unita' situate oltre il secondo piano")

ELEMENTI_MINIMO = [
    "Stabile o alloggio la cui ristrutturazione e' antecedente agli ultimi 30 anni, "
    "oppure nello stesso periodo non e' avvenuta alcuna manutenzione",
    "Mancanza di impianto di riscaldamento autonomo o centralizzato",
    "Assenza di acqua corrente",
    "Assenza di bagno e servizi igienici"
]

ETICHETTE_SUPERFICIE = {
    "mq_utile": "Superficie utile - mq",
    "mq_autorimessa": "Autorimesse ad uso esclusivo - mq (calcolate al 50%)",
    "mq_posto_auto": "Posto macchina in autorimesse di uso comune - mq (calcolato al 25%)",
    "mq_accessori": "Balconi, terrazze, cantine e solai - mq (calcolati al 25%)",
    "mq_giardino": "Giardino e/o cortile esclusivo - mq (calcolato al 10% solo se superiore a 10 mq)"
}

ETICHETTE_PORZIONE = {
    "porzione": "Viene locata solo una porzione dell'immobile",
    "mq_esclusiva": "Superficie utile dei vani locati ad uso esclusivo - mq",
    "mq_condivise": "Superficie utile totale delle parti e dei servizi condivisi - mq",
    "stanze_locate": "Numero di stanze ad uso esclusivo locate",
    "stanze_totali": "Numero totale di stanze ad uso esclusivo presenti nell'immobile"
}

DESCRIZIONE_SUPERFICIE_UTILE = ("Dato di partenza per la superficie utile: superficie utile riscaldata "
                                "risultante dall'APE. L'accordo prevede in via esclusiva il dato "
                                "dell'APE in corso di validita'. Si passa alla superficie catastale "
                                "netta soltanto quando l'immobile ha locali non riscaldati (ad esempio "
                                "ripostigli o magazzini) che non rientrano in quel dato.") #messaggio info

DESCRIZIONE_ARREDO = ("Il massimo si applica solo con arredamento nuovo o in ottime condizioni di "
                      "conservazione ed elettrodomestici perfettamente funzionanti. Per il "
                      "parzialmente arredato serve inoltre che sia interamente ammobiliato il vano "
                      "cucina e interamente arredato almeno un altro vano.") #messaggio info

DESCRIZIONE_RIDUZIONE = ("Punto A.8: zone degradate e prive di dotazioni infrastrutturali. Punto H.2: "
                         "condizioni sociali o reddituali particolarmente disagiate del conduttore, "
                         "precarie condizioni dell'immobile, scarsa qualita' ambientale, oneri "
                         "condominiali elevati, situazioni generali di emergenza. La riduzione va "
                         "motivata nel contratto e indicata nell'attestazione di rispondenza.") #messaggio info

ETICHETTE_MAGGIORAZIONI = {
    "metro": "e) Immobile in prossimita' di una fermata della metropolitana, a una distanza massima "
             "di percorrenza di 600 metri (fino al 5%)",
    "magg_i": "i) Impianto fisso di condizionamento dell'aria, pompa di calore o raffrescamento in "
              "almeno la meta' dei vani (+2%)",
    "magg_l": "l) Stabile con impianti per il superamento delle barriere architettoniche: montascale "
              "fruibile e funzionante e totale assenza di barriere (+2%)",
    "magg_m": "m) Impianto fotovoltaico o solare termico che copre interamente il fabbisogno per "
              "l'acqua calda e almeno in parte quello per riscaldare o raffrescare l'immobile (+1%)",
    "magg_n": "n) Presenza di impianti sportivi, piscina o palestra (+5%)",
    "vincolato": "Immobile vincolato ai sensi dell'art. 1, comma 2, lettera a) della L. 431/98 e "
                 "della L. 1/6/1939 (+20%)",
    "riduzione": "Riduzione del valore minimo (massimo 30%)"
}

OPZIONI_CONTRATTO = [
    "Contratto agevolato (art. 2, comma 3)",
    "Contratto transitorio ordinario (art. 5, comma 1)",
    "Contratto transitorio per studenti universitari (art. 5, commi 2 e 3)"
]

OPZIONI_CATEGORIA = [
    "A/1, A/2, A/7, A/8, A/9 o A/11",
    "A/3, A/4, A/5 o A/6"
]

OPZIONI_ARREDO = [
    "Non arredato",
    "Parzialmente arredato (fino al 10%)",
    "Completamente arredato (fino al 20%)"
]

OPZIONI_CLASSE = [
    "Nessuna delle classi da A1 ad A4",
    "A1 (massimo 2,5%)",
    "A2 (massimo 5%)",
    "A3 (massimo 7,5%)",
    "A4 (massimo 10%)"
]

OPZIONI_INTERVENTI = [
    "Nessuno di questi interventi",
    "f) Completamente ristrutturato anche nell'isolamento termico dopo il 2011, con passaggio in "
    "classe energetica pari o superiore a D (+10%)",
    "g) Edificato dopo il 2011 e progettato con isolamento termico che lo colloca in classe "
    "energetica pari o superiore a D (+10%)",
    "h) Completamente ristrutturato dopo il 1968, senza interventi di efficientamento energetico (+5%)"
]

OPZIONI_DURATA = [
    "Tre anni",
    "Quattro anni (+3,00%)",
    "Cinque anni (+5,50%)",
    "Sei anni (+8,00%)",
    "Superiore a sei anni (+10,50%)"
]

NOTA_DURATA = ("La maggiorazione per la durata non si applica: i contratti transitori ordinari durano "
               "al massimo diciotto mesi e quelli per studenti al massimo tre anni.")

NOTA_STUDENTI = ("Per i contratti destinati agli studenti universitari le fasce di oscillazione non "
                 "subiscono alcun aumento per gli immobili vincolati (punto C.5).")



# MODELLO DI INPUT



class InputBrescia(BaseModel):
    tipo_contratto: Literal[
        "Contratto agevolato (art. 2, comma 3)",
        "Contratto transitorio ordinario (art. 5, comma 1)",
        "Contratto transitorio per studenti universitari (art. 5, commi 2 e 3)"
    ] = "Contratto agevolato (art. 2, comma 3)"

    categoria: Literal[
        "A/1, A/2, A/7, A/8, A/9 o A/11",
        "A/3, A/4, A/5 o A/6"
    ] = Field("A/1, A/2, A/7, A/8, A/9 o A/11", description="Categoria catastale dell'immobile")

    zona: Literal[
        "1 - Centro",
        "2 - Panoramica",
        "3 - Via Crocifissa",
        "4 - Via Veneto",
        "5 - Brescia Due",
        "6 - Viale Piave",
        "7 - Q.re Abba / S. Anna",
        "8 - Fiumicello",
        "9 - Noce / Folzano",
        "10 - Vill. Prealpino",
        "11 - Vill. Badia / Violino",
        "12 - S. Eufemia",
        "13 - San Polo",
        "14 - Casazza",
        "15/20 - San Polino"
    ] = Field("1 - Centro", description="Area omogenea")

    piano: int = Field(1, ge=0, le=40, description="Piano dell'appartamento (0 per piano terra)")
    edificio_alto: bool = Field(False, description="L'edificio ha piu' di due piani fuori terra")

    # superficie
    porzione: bool = Field(False, description=ETICHETTE_PORZIONE["porzione"])
    mq_esclusiva: float = Field(0.0, ge=0, description=ETICHETTE_PORZIONE["mq_esclusiva"] +
                                                       ". Considerato solo se porzione = true.")
    mq_condivise: float = Field(0.0, ge=0, description=ETICHETTE_PORZIONE["mq_condivise"] +
                                                       ". Considerato solo se porzione = true.")
    stanze_locate: int = Field(1, ge=0, le=30, description=ETICHETTE_PORZIONE["stanze_locate"] +
                                                           ". Considerato solo se porzione = true.")
    stanze_totali: int = Field(1, ge=1, le=30, description=ETICHETTE_PORZIONE["stanze_totali"] +
                                                           ". Considerato solo se porzione = true.")
    mq_utile: float = Field(
        0.0, ge=0,
        description=ETICHETTE_SUPERFICIE["mq_utile"] + ". Considerato solo se porzione = false. " +
                    DESCRIZIONE_SUPERFICIE_UTILE
    )

    # pertinenze, calcolate sulla superficie utile non maggiorata
    mq_autorimessa: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_autorimessa"])
    mq_posto_auto: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_posto_auto"])
    mq_accessori: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_accessori"])
    mq_giardino: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_giardino"])

    # elementi per l'applicazione del valore massimo
    elementi_massimo: list[bool] = Field(
        default_factory=lambda: [False] * len(ELEMENTI_MASSIMO),
        min_length=len(ELEMENTI_MASSIMO), max_length=len(ELEMENTI_MASSIMO),
        description="6 caselle true/false, nello stesso ordine della lista ELEMENTI_MASSIMO "
                    "(vedi GET /citta/brescia/info)"
    )
    ascensore: bool = Field(
        False,
        description=ETICHETTA_ASCENSORE + ". Considerato solo se piano > 2 ed edificio_alto = true: "
                    "negli altri casi l'ascensore non e' richiesto."
    )

    # elementi che impongono il valore minimo (punto A.8)
    elementi_minimo: list[bool] = Field(
        default_factory=lambda: [False] * len(ELEMENTI_MINIMO),
        min_length=len(ELEMENTI_MINIMO), max_length=len(ELEMENTI_MINIMO),
        description="4 caselle true/false, nello stesso ordine della lista ELEMENTI_MINIMO "
                    "(vedi GET /citta/brescia/info). Ne basta una per imporre il valore minimo."
    )

    # maggiorazioni
    arredo: Literal[
        "Non arredato",
        "Parzialmente arredato (fino al 10%)",
        "Completamente arredato (fino al 20%)"
    ] = Field("Non arredato", description="Arredamento (Allegato 4, punti b e c). " + DESCRIZIONE_ARREDO)
    magg_arredo: Optional[float] = Field(
        None, ge=0, le=20,
        description="Maggiorazione per l'arredo effettivamente concordata (%). Se omessa si usa il "
                    "tetto massimo dell'opzione di arredo scelta. Non puo' superare il tetto "
                    "dell'opzione (10 / 20)."
    )

    classe: Literal[
        "Nessuna delle classi da A1 ad A4",
        "A1 (massimo 2,5%)",
        "A2 (massimo 5%)",
        "A3 (massimo 7,5%)",
        "A4 (massimo 10%)"
    ] = Field("Nessuna delle classi da A1 ad A4", description="Classe energetica da A1 ad A4")
    magg_classe: Optional[float] = Field(
        None, ge=0, le=10,
        description="Maggiorazione per la classe energetica concordata (%). Se omessa si usa il "
                    "tetto massimo della classe scelta. Non puo' superare il tetto della classe "
                    "(2,5 / 5 / 7,5 / 10)."
    )

    metro: bool = Field(False, description=ETICHETTE_MAGGIORAZIONI["metro"])
    magg_metro: Optional[float] = Field(
        None, ge=0, le=5,
        description="Maggiorazione per la vicinanza alla metropolitana concordata (%). Se omessa si "
                    "usa il massimo (5%). Considerata solo se metro = true."
    )

    interventi: Literal[
        "Nessuno di questi interventi",
        "f) Completamente ristrutturato anche nell'isolamento termico dopo il 2011, con passaggio in "
        "classe energetica pari o superiore a D (+10%)",
        "g) Edificato dopo il 2011 e progettato con isolamento termico che lo colloca in classe "
        "energetica pari o superiore a D (+10%)",
        "h) Completamente ristrutturato dopo il 1968, senza interventi di efficientamento energetico (+5%)"
    ] = Field("Nessuno di questi interventi", description="Interventi sull'immobile")

    magg_i: bool = Field(False, description=ETICHETTE_MAGGIORAZIONI["magg_i"])
    magg_l: bool = Field(False, description=ETICHETTE_MAGGIORAZIONI["magg_l"])
    magg_m: bool = Field(
        False,
        description=ETICHETTE_MAGGIORAZIONI["magg_m"] + ". Considerato solo se interventi = "
                    "'Nessuno di questi interventi' oppure 'h) ...'."
    )
    magg_n: bool = Field(False, description=ETICHETTE_MAGGIORAZIONI["magg_n"])

    durata: Literal[
        "Tre anni",
        "Quattro anni (+3,00%)",
        "Cinque anni (+5,50%)",
        "Sei anni (+8,00%)",
        "Superiore a sei anni (+10,50%)"
    ] = Field("Tre anni", description="Durata del primo periodo contrattuale. Considerata solo per "
                                      "il contratto agevolato.")

    vincolato: bool = Field(
        False,
        description=ETICHETTE_MAGGIORAZIONI["vincolato"] + ". Non considerato per il contratto "
                    "transitorio per studenti universitari (punto C.5)."
    )

    riduzione: float = Field(
        0.0, ge=0, le=30,
        description=ETICHETTE_MAGGIORAZIONI["riduzione"] + ". " + DESCRIZIONE_RIDUZIONE
    )



# INFO PER IL FRONTEND


INFO = {
    "id": "brescia",
    "nome": "Brescia",
    "titolo": "Calcolatore canone concordato - Comune di Brescia",
    "unita_fasce": "euro/mq annui",
    "valori_a2": valori_a2,
    "valori_a3": valori_a3,
    "lista_zone": LISTA_ZONE,
    "elementi_massimo": ELEMENTI_MASSIMO,
    "elementi_minimo": ELEMENTI_MINIMO,
    "etichette_superficie": ETICHETTE_SUPERFICIE,
    "etichette_porzione": ETICHETTE_PORZIONE,
    "etichette_maggiorazioni": ETICHETTE_MAGGIORAZIONI,
    "etichette": {
        "ascensore": ETICHETTA_ASCENSORE,
        "superficie_utile": DESCRIZIONE_SUPERFICIE_UTILE,
        "arredo": DESCRIZIONE_ARREDO,
        "riduzione": DESCRIZIONE_RIDUZIONE
    },
    "opzioni": {
        "tipo_contratto": OPZIONI_CONTRATTO,
        "categoria": OPZIONI_CATEGORIA,
        "arredo": OPZIONI_ARREDO,
        "classe": OPZIONI_CLASSE,
        "interventi": OPZIONI_INTERVENTI,
        "durata": OPZIONI_DURATA
    },
    "note": [
        "I valori delle tabelle sono ANNUI in euro al mq: il canone mensile e' il canone annuo "
        "diviso 12.",
        "valori_a2 si usa per le categorie catastali A/1, A/2, A/7, A/8, A/9 e A/11; valori_a3 per "
        "le categorie A/3, A/4, A/5 e A/6.",
        "La superficie utile dell'immobile principale e' maggiorata del 12,50%; poi +20% fino a "
        "60 mq e +10% da 60,01 a 65 mq, con il limite di 72,59 mq. Le pertinenze si sommano senza "
        "maggiorazione.",
        NOTA_ASCENSORE,
        "Il valore massimo della fascia e' applicabile solo se sono presenti tutti e sette gli "
        "elementi dell'Allegato 4 punto a: altrimenti il canone va concordato al di sotto di esso.",
        "Se e' presente anche uno solo degli elementi del punto A.8 si applica il valore minimo "
        "della fascia.",
        "Le maggiorazioni sono sommate tra loro e applicate sui valori di fascia.",
        NOTA_DURATA,
        NOTA_STUDENTI
    ]
}



# CALCOLO (stessi passaggi, nello stesso ordine, del file Streamlit)


def calcola(dati: InputBrescia) -> dict:
    note = []
    avvertenze = []

    tipo_contratto = dati.tipo_contratto
    categoria = dati.categoria
    zona = dati.zona
    piano = dati.piano
    edificio_alto = dati.edificio_alto

    # SUPERFICIE

    porzione = dati.porzione

    if porzione == True:
        mq_esclusiva = dati.mq_esclusiva
        mq_condivise = dati.mq_condivise
        stanze_locate = dati.stanze_locate
        stanze_totali = dati.stanze_totali
        mq_utile = mq_esclusiva + mq_condivise * stanze_locate / stanze_totali
    else:
        mq_utile = dati.mq_utile

    mq_principale = mq_utile * 1.125

    mq_maggiorata = mq_principale
    if mq_principale <= 60.0:
        mq_maggiorata = mq_principale * 1.20
        if mq_maggiorata > 72.59:
            mq_maggiorata = 72.59
    elif mq_principale <= 65.0:
        mq_maggiorata = mq_principale * 1.10
        if mq_maggiorata > 72.59:
            mq_maggiorata = 72.59

    mq_giardino = dati.mq_giardino
    mq_giardino_conv = 0.0
    if mq_giardino > 10.0:
        mq_giardino_conv = mq_giardino * 0.10

    mq_finali = (mq_maggiorata + dati.mq_autorimessa * 0.50 + dati.mq_posto_auto * 0.25
                 + dati.mq_accessori * 0.25 + mq_giardino_conv)

    if mq_finali <= 0.0:
        raise HTTPException(
            status_code=400,
            detail="Inserire la superficie dell'immobile per ottenere la stima"
        )

    # ELEMENTI PER L'APPLICAZIONE DEL VALORE MASSIMO

    mx1 = dati.elementi_massimo[0]  # Impianto di riscaldamento autonomo o centralizzato
    mx2 = dati.elementi_massimo[1]  # Box o posto auto
    mx3 = dati.elementi_massimo[2]  # Cantina o soffitta o solaio ad uso esclusivo
    mx4 = dati.elementi_massimo[3]  # Giardino, terrazza condominiale attrezzata o area parcabile
    mx5 = dati.elementi_massimo[4]  # Ultimato, ristrutturato o manutenuto negli ultimi 10 anni
    mx6 = dati.elementi_massimo[5]  # Classe energetica non inferiore alla D

    mx7 = True
    if piano > 2 and edificio_alto == True:
        mx7 = dati.ascensore
    else:
        note.append(NOTA_ASCENSORE)

    elementi_massimo = [mx1, mx2, mx3, mx4, mx5, mx6, mx7]
    n_massimo = sum(e for e in elementi_massimo if e == True)

    # ELEMENTI CHE IMPONGONO IL VALORE MINIMO 

    condizioni_negative = dati.elementi_minimo
    n_negative = sum(c for c in condizioni_negative if c == True)

    # MAGGIORAZIONI 

    perc_totale = 0.0

    arredo = dati.arredo
    tetto_arredo = 0
    if arredo.startswith("Parzialmente"):
        tetto_arredo = 10
    elif arredo.startswith("Completamente"):
        tetto_arredo = 20

    if tetto_arredo > 0:
        # lo slider aveva come default il tetto massimo
        if dati.magg_arredo is None:
            magg_arredo = tetto_arredo
        else:
            magg_arredo = dati.magg_arredo
        if magg_arredo > tetto_arredo:
            raise HTTPException(
                status_code=400,
                detail=f"La maggiorazione per l'arredo ({magg_arredo}%) supera il tetto massimo "
                       f"({tetto_arredo}%) previsto per l'opzione '{arredo}'"
            )
        perc_totale = perc_totale + magg_arredo / 100.0

    classe = dati.classe
    tetto_classe = 0.0
    if classe.startswith("A1"):
        tetto_classe = 2.5
    elif classe.startswith("A2"):
        tetto_classe = 5.0
    elif classe.startswith("A3"):
        tetto_classe = 7.5
    elif classe.startswith("A4"):
        tetto_classe = 10.0

    if tetto_classe > 0:
        if dati.magg_classe is None:
            magg_classe = tetto_classe
        else:
            magg_classe = dati.magg_classe
        if magg_classe > tetto_classe:
            raise HTTPException(
                status_code=400,
                detail=f"La maggiorazione per la classe energetica ({magg_classe}%) supera il tetto "
                       f"massimo ({tetto_classe}%) previsto per l'opzione '{classe}'"
            )
        perc_totale = perc_totale + magg_classe / 100.0

    metro = dati.metro
    if metro == True:
        if dati.magg_metro is None:
            magg_metro = 5
        else:
            magg_metro = dati.magg_metro
        perc_totale = perc_totale + magg_metro / 100.0

    interventi = dati.interventi
    if interventi.startswith("f)") or interventi.startswith("g)"):
        perc_totale = perc_totale + 0.10
    elif interventi.startswith("h)"):
        perc_totale = perc_totale + 0.05

    magg_i = dati.magg_i
    if magg_i == True:
        perc_totale = perc_totale + 0.02

    magg_l = dati.magg_l
    if magg_l == True:
        perc_totale = perc_totale + 0.02

    if interventi.startswith("Nessuno") or interventi.startswith("h)"):
        magg_m = dati.magg_m
        if magg_m == True:
            perc_totale = perc_totale + 0.01

    magg_n = dati.magg_n
    if magg_n == True:
        perc_totale = perc_totale + 0.05

    if tipo_contratto.startswith("Contratto agevolato"):
        durata = dati.durata
        if durata.startswith("Quattro"):
            perc_totale = perc_totale + 0.03
        elif durata.startswith("Cinque"):
            perc_totale = perc_totale + 0.055
        elif durata.startswith("Sei"):
            perc_totale = perc_totale + 0.08
        elif durata.startswith("Superiore"):
            perc_totale = perc_totale + 0.105
    else:
        note.append(NOTA_DURATA)

    if tipo_contratto.startswith("Contratto transitorio per studenti"):
        note.append(NOTA_STUDENTI)
    else:
        vincolato = dati.vincolato
        if vincolato == True:
            perc_totale = perc_totale + 0.20

    riduzione = dati.riduzione

    # CANONE

    if categoria.startswith("A/1"):
        val_min, val_max = valori_a2[zona]
    else:
        val_min, val_max = valori_a3[zona]

    canone_mq_base_min = val_min
    canone_mq_base_max = val_max

    val_min = val_min + val_min * perc_totale
    val_max = val_max + val_max * perc_totale
    val_min = val_min - val_min * riduzione / 100.0

    if n_negative >= 1:
        val_max = val_min

    canone_annuo_min = mq_finali * val_min
    canone_annuo_max = mq_finali * val_max

    if n_negative >= 1:
        note.append(f"Sono presenti {n_negative} degli elementi del punto A.8: si applica il valore "
                    f"minimo della fascia")
    elif n_massimo < 7:
        avvertenze.append("Non essendo presenti tutti e sette gli elementi dell'Allegato 4 punto a, "
                          "il valore massimo indicato non e' applicabile: il canone va concordato al "
                          "di sotto di esso.")

    return {
        "citta": "Brescia",
        "zona": zona,
        "categoria": categoria,
        "superficie_utile": round(mq_utile, 2),
        "superficie_principale_maggiorata": round(mq_maggiorata, 2),
        "superficie_calcolo": round(mq_finali, 2),
        "elementi_massimo": n_massimo,
        "valore_massimo_applicabile": n_massimo == 7,
        "elementi_minimo": n_negative,
        "canone_mq_base_min": round(canone_mq_base_min, 2),
        "canone_mq_base_max": round(canone_mq_base_max, 2),
        "percentuale_maggiorazioni": round(perc_totale * 100, 2),
        "riduzione_minimo": riduzione,
        "canone_mq_min": round(val_min, 4),
        "canone_mq_max": round(val_max, 4),
        "canone_mensile_min": round(canone_annuo_min / 12.0, 2),
        "canone_mensile_max": round(canone_annuo_max / 12.0, 2),
        "canone_annuo_min": round(canone_annuo_min, 2),
        "canone_annuo_max": round(canone_annuo_max, 2),
        "note": note,
        "avvertenze": avvertenze
    }
