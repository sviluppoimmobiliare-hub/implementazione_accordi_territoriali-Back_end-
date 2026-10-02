

from typing import Literal, Optional
from pydantic import BaseModel, Field
from fastapi import HTTPException



zonizzazione = {

    "Lungarno Simonelli (oltre il 50% delle finestre sul lungarno)": "Pregio",
    "Lungarno Pacinotti (oltre il 50% delle finestre sul lungarno)": "Pregio",
    "Lungarno Mediceo (oltre il 50% delle finestre sul lungarno)": "Pregio",
    "Lungarno Buozzi (oltre il 50% delle finestre sul lungarno)": "Pregio",
    "Lungarno Sonnino (oltre il 50% delle finestre sul lungarno)": "Pregio",
    "Lungarno Gambacorti (oltre il 50% delle finestre sul lungarno)": "Pregio",
    "Lungarno Galilei (oltre il 50% delle finestre sul lungarno)": "Pregio",
    "Lungarno Fibonacci (oltre il 50% delle finestre sul lungarno)": "Pregio",
    "Marina di Pisa - lungomare o piazza con affaccio sul mare": "Pregio",
    "Tirrenia - viale del Tirreno con affaccio sul mare": "Pregio",
    "Calambrone - viale del Tirreno con affaccio sul mare": "Pregio",

    "S. Antonio, quartiere storico fino alla ferrovia": "A",
    "S. Martino, quartiere storico": "A",
    "S. Maria, quartiere storico fino alla ferrovia": "A",
    "S. Francesco, compresa la zona tra via di Pratale a nord, via Battelli e via De Amicis a est": "A",
    "Porta a Lucca, tra via di Gello a est, via Tino da Camaino a ovest, via Contessa Matilde e "
    "via del Brennero a sud, via G. Falcone a nord (esclusa la zona Piazzali)": "A",
    "Viale delle Piagge fino al tondo": "A",
    "Barbaricina, tra via Aurelia a est, via del Capannone, via T. Rook, via F. Tesio a ovest "
    "e via delle Cascine a nord": "A",
    "Marina di Pisa, non lungomare": "A",
    "Tirrenia, non lungomare": "A",
    "Calambrone, non lungomare": "A",

    "S. Marco, nella zona delimitata dalla ferrovia e dalla S.G.C. FI-PI-LI": "B",
    "S. Giusto, nella zona delimitata dalla ferrovia e dalla S.G.C. FI-PI-LI": "B",
    "Porta Fiorentina, tra le ex mura urbane a nord, la ferrovia a sud, via Pilla - via vecchia "
    "tranvia a sud e l'Arno a ovest (esclusa la zona da via Catalani a via Colombo)": "B",
    "Porta a Mare, tra via A. Moro, via Livornese fino al ponte del CEP e l'Arno": "B",
    "Barbaricina, tra via delle Cascine e l'Arno e a ovest di via Boccherini (escluso quanto in "
    "zona A)": "B",
    "Zona Impianti Sportivi, fino a via di Campaldo a nord, via Pietrasantina, via del "
    "Marmigliano, ferrovia a est e via Aurelia a ovest": "B",
    "Zona Piazzali, tra via U. Rindi a nord, via Piave a est e via Contessa Matilde a sud": "B",
    "Zona tra via di Gello a ovest, via Lucchese a est, via Paparelli a sud e via Chiarugi - "
    "Caserma dei Paracadutisti a nord": "B",
    "Pratale e Don Bosco, tra via Battelli e via De Amicis a ovest, via Luzzatto e via Nenni a "
    "est e il viale delle Piagge a sud": "B",
    "S. Michele, fino a via Mons. Manghi e via Padre Pio a est": "B",
    "Porta a Piagge": "B",
    "Cisanello": "B",
    "Pisanova, esclusa via Paolo VI": "B",
    "La Vettola": "B",
    "S. Piero, dalla superstrada fino a S. Piero tra via E. Scauro, via Castagnolo e via Livornese": "B",

    "Gagno": "C",
    "I Passi": "C",
    "Pisanova, limitatamente a via Paolo VI": "C",
    "S. Biagio, vie Mazzei, Taddei, Simon e Martin Lutero": "C",
    "Riglione": "C",
    "Oratoio": "C",
    "Putignano": "C",
    "S. Ermete": "C",
    "S. Giusto a sud della S.G.C. FI-PI-LI": "C",
    "Porta a Mare, escluso quanto in zona B": "C",
    "Luicchio": "C",
    "CEP, tra via Pergolesi - Pierin del Vaga a nord, via Tiziano Vecellio a ovest e via "
    "Boccherini a est": "C",
    "Zona stazione, da via Colombo a via Catalani": "C",

    "Zone artigianali e agricole": "D",
    "Ospedaletto": "D",
    "Coltano": "D"
}

localita_lontane = [
    "Putignano", "Riglione", "Oratoio",
    "S. Piero, dalla superstrada fino a S. Piero tra via E. Scauro, via Castagnolo e via Livornese",
    "Marina di Pisa - lungomare o piazza con affaccio sul mare", "Marina di Pisa, non lungomare",
    "Tirrenia - viale del Tirreno con affaccio sul mare", "Tirrenia, non lungomare",
    "Calambrone - viale del Tirreno con affaccio sul mare", "Calambrone, non lungomare",
    "La Vettola"
]

fasce_tipo_A = {
    "Pregio": [7.0, 8.0, 8.0, 10.0],
    "A": [6.5, 7.5, 7.5, 8.5],
    "B": [4.8, 5.8, 5.8, 6.8],
    "C": [4.5, 5.5, 5.5, 6.5],
    "D": [4.0, 5.0, 5.0, 6.1]
}

fasce_tipo_B = {
    "Pregio": [6.5, 7.6, 7.6, 8.5],
    "A": [5.8, 6.7, 6.7, 7.6],
    "B": [4.7, 5.7, 5.7, 6.7],
    "C": [4.0, 5.0, 5.0, 6.0],
    "D": [3.5, 4.5, 4.5, 5.4]
}

fasce_tipo_C = {
    "Pregio": [5.0, 6.0, 6.0, 6.9],
    "A": [4.2, 5.2, 5.2, 6.1],
    "B": [4.0, 4.7, 4.7, 5.5],
    "C": [3.5, 4.1, 4.1, 4.7],
    "D": [3.5, 4.1, 4.1, 4.7]
}

LISTA_LOCALITA = list(zonizzazione.keys())

ETICHETTE_SUPERFICIE = {
    "mq_utile": "a) Superficie interna utile dell'alloggio - mq",
    "mq_autorimessa": "b) Autorimessa singola - mq (calcolata al 60%)",
    "mq_coperto": "c) Posto auto coperto di proprieta' esclusiva - mq (calcolato al 40%)",
    "mq_comune": "d) Posto auto di effettiva disponibilita' in area comune - mq (calcolato al 30%)",
    "mq_scoperto": "e) Posto auto scoperto di proprieta' esclusiva - mq (calcolato al 20%)",
    "mq_accessori": "f) Balconi, terrazze, cantine e altri accessori simili - mq (calcolati al 25%)",
    "mq_giardino": "g, h, i) Giardino in godimento esclusivo - mq (10% fino a 100 mq, 15% da 101 a "
                   "200 mq, 20% oltre 200 mq)",
    "mq_area_scoperta": "j) Area scoperta di pertinenza in godimento esclusivo, non a giardino - mq "
                        "(10%, solo se non inferiore a 100 mq)"
}

ETICHETTE_PORZIONE = {
    "porzione": "Viene locata solo una porzione dell'immobile",
    "mq_esclusivi": "Superficie della porzione locata ad uso esclusivo - mq",
    "mq_spazi_comuni": "Superficie degli spazi comuni dell'immobile - mq",
    "occupanti": "Numero degli occupanti dell'immobile"
}

ETICHETTE_CARATTERISTICHE = {
    "car_a": "a) Impianto idrico idoneo ed efficiente",
    "car_b": "b) Impianto elettrico a norma",
    "car_e": "e) Spazi esterni ad uso esclusivo (garage, terrazze, logge, cantine) oltre il 15% "
             "della superficie utile",
    "car_f": "f) Spazi per parcheggio con effettiva disponibilita'",
    "car_h": "h) Sistemi funzionanti di condizionamento d'aria",
    "car_i": "i) Ascensore (per le unita' oltre il 3 piano fuori terra)"
}

ETICHETTE_MAGGIORAZIONI = {
    "magg_pregio": "Tipo B con almeno una rifinitura di pregio: giardino esclusivo piu' grande "
                   "dell'alloggio, doppi servizi, condizionamento o ascensore (+5%)",
    "popolare": "Edificio popolare (ex ATER o simili), costruito con piani PEEP o con convenzioni o "
                "agevolazioni di enti pubblici o istituti previdenziali (-20%)",
    "classe": "Classe energetica A, B o C (+5%)",
    "breve": "Durata del contratto inferiore a 12 mesi (-10%)",
    "arredato": "Unita' immobiliare arredata",
    "magg_arredo": "Aumento per l'arredo concordato in base a quantita' e qualita' (%)",
    "sociale": "Alloggio sociale: riduzione di almeno il 20% del canone"
}

OPZIONI_CONTRATTO = [
    "Contratto agevolato",
    "Contratto transitorio ordinario",
    "Contratto transitorio per studenti universitari"
]

OPZIONI_CATEGORIA = [
    "A/7 - villa o villetta",
    "A/2 o A/3 - appartamento",
    "Altra categoria"
]

OPZIONI_RISCALDAMENTO = [
    "Efficiente e a norma in tutti i vani utili",
    "Efficiente e a norma, ma non in tutti i vani utili",
    "Assente o non a norma"
]

OPZIONI_SERVIZI = [
    "1) Doppi servizi con il secondo di almeno 3 elementi, oppure unico servizio con antibagno, "
    "almeno 4 elementi sanitari e finestra",
    "2) Servizio interno con almeno 4 elementi sanitari, con finestra o aerazione forzata",
    "3) Servizio interno con almeno 3 elementi sanitari, con finestra o aerazione forzata",
    "4) Un solo servizio con meno di 2 elementi sanitari, oppure esterno all'alloggio, oppure "
    "alloggio dichiarato antigienico",
    "5) Nessuno dei casi precedenti"
]

OPZIONI_DURATA = [
    "Tre anni",
    "Quattro anni (+2%)",
    "Cinque anni (+4%)",
    "Sei anni o piu' (+6%)"
]

OPZIONI_ARREDO_STUDENTI = [
    "Non ammobiliato, oppure senza tutti gli arredi del punto A",
    "A) Ammobiliato con cucina completa e, per ogni studente, letto, comodino, armadio, "
    "scrivania con sedie, libreria e lampada (+10%)",
    "B) Arredi del punto A piu' almeno due tra divano o due poltrone, televisore, wi-fi, "
    "lavastoviglie, condizionamento (+15%)"
]

NOTA_TRANSITORIO_BREVE = ("Per i contratti fino a 30 giorni il canone e' lasciato alla libera "
                          "contrattazione delle parti: il calcolatore vale per quelli da 31 giorni a "
                          "18 mesi.")

NOTA_PORZIONE = ("Il coefficiente correttivo della superficie si applica sul canone dell'intero "
                 "immobile, che poi viene frazionato.")

NOTA_NON_CLASSIFICABILE = ("L'alloggio non rientra in nessuno dei tipi A, B o C: l'accordo richiede "
                           "almeno impianto idrico idoneo ed efficiente, impianto elettrico a norma e "
                           "un servizio igienico con i requisiti del Tipo C")



# MODELLO DI INPUT


class InputPisa(BaseModel):
    tipo_contratto: Literal[
        "Contratto agevolato",
        "Contratto transitorio ordinario",
        "Contratto transitorio per studenti universitari"
    ] = "Contratto agevolato"

    localita: str = Field(
        ...,
        description="Localita' (art. 2), scritta come nell'elenco lista_localita di "
                    "GET /citta/pisa/info: la zona e' individuata in automatico. Gli alloggi situati "
                    "nelle vie di confine tra due zone rientrano nella zona con il valore al mq piu' "
                    "elevato."
    )

    # superficie convenzionale
    mq_utile: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_utile"])
    mq_autorimessa: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_autorimessa"])
    mq_coperto: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_coperto"])
    mq_comune: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_comune"])
    mq_scoperto: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_scoperto"])
    mq_accessori: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_accessori"])
    mq_giardino: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_giardino"])
    mq_area_scoperta: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_area_scoperta"])

    # locazione di porzione di immobile
    porzione: bool = Field(False, description=ETICHETTE_PORZIONE["porzione"])
    mq_esclusivi: float = Field(0.0, ge=0, description=ETICHETTE_PORZIONE["mq_esclusivi"] +
                                                       ". Considerato solo se porzione = true.")
    mq_spazi_comuni: float = Field(0.0, ge=0, description=ETICHETTE_PORZIONE["mq_spazi_comuni"] +
                                                          ". Considerato solo se porzione = true.")
    occupanti: int = Field(1, ge=1, le=20, description=ETICHETTE_PORZIONE["occupanti"] +
                                                       ". Considerato solo se porzione = true.")

    # classificazione dell'immobile (art. 5)
    categoria: Literal[
        "A/7 - villa o villetta",
        "A/2 o A/3 - appartamento",
        "Altra categoria"
    ] = Field("A/7 - villa o villetta", description="Categoria catastale")

    anni: int = Field(20, ge=0, le=300, description="Anni dalla costruzione, oppure dall'ultima "
                                                    "ristrutturazione interna")

    car_a: bool = Field(False, description=ETICHETTE_CARATTERISTICHE["car_a"])
    car_b: bool = Field(False, description=ETICHETTE_CARATTERISTICHE["car_b"])

    riscaldamento: Literal[
        "Efficiente e a norma in tutti i vani utili",
        "Efficiente e a norma, ma non in tutti i vani utili",
        "Assente o non a norma"
    ] = Field("Efficiente e a norma in tutti i vani utili", description="Riscaldamento")

    servizi: Literal[
        "1) Doppi servizi con il secondo di almeno 3 elementi, oppure unico servizio con antibagno, "
        "almeno 4 elementi sanitari e finestra",
        "2) Servizio interno con almeno 4 elementi sanitari, con finestra o aerazione forzata",
        "3) Servizio interno con almeno 3 elementi sanitari, con finestra o aerazione forzata",
        "4) Un solo servizio con meno di 2 elementi sanitari, oppure esterno all'alloggio, oppure "
        "alloggio dichiarato antigienico",
        "5) Nessuno dei casi precedenti"
    ] = Field("1) Doppi servizi con il secondo di almeno 3 elementi, oppure unico servizio con "
              "antibagno, almeno 4 elementi sanitari e finestra", description="Servizi igienici")

    car_e: bool = Field(False, description=ETICHETTE_CARATTERISTICHE["car_e"])
    car_f: bool = Field(False, description=ETICHETTE_CARATTERISTICHE["car_f"])
    car_h: bool = Field(False, description=ETICHETTE_CARATTERISTICHE["car_h"])
    car_i: bool = Field(False, description=ETICHETTE_CARATTERISTICHE["car_i"])

    # maggiorazioni e riduzioni
    magg_pregio: bool = Field(
        False,
        description=ETICHETTE_MAGGIORAZIONI["magg_pregio"] + ". Considerato solo se l'alloggio "
                    "risulta di Tipo B e ha almeno una delle rifiniture di pregio."
    )
    popolare: bool = Field(False, description=ETICHETTE_MAGGIORAZIONI["popolare"])
    classe: bool = Field(False, description=ETICHETTE_MAGGIORAZIONI["classe"])

    durata: Literal[
        "Tre anni",
        "Quattro anni (+2%)",
        "Cinque anni (+4%)",
        "Sei anni o piu' (+6%)"
    ] = Field("Tre anni", description="Durata del contratto. Considerata solo per il contratto "
                                      "agevolato.")

    arredo_studenti: Literal[
        "Non ammobiliato, oppure senza tutti gli arredi del punto A",
        "A) Ammobiliato con cucina completa e, per ogni studente, letto, comodino, armadio, "
        "scrivania con sedie, libreria e lampada (+10%)",
        "B) Arredi del punto A piu' almeno due tra divano o due poltrone, televisore, wi-fi, "
        "lavastoviglie, condizionamento (+15%)"
    ] = Field("Non ammobiliato, oppure senza tutti gli arredi del punto A",
              description="Arredamento. Considerato solo per il contratto transitorio per studenti "
                          "universitari.")
    breve: bool = Field(
        False,
        description=ETICHETTE_MAGGIORAZIONI["breve"] + ". Considerato solo per il contratto "
                    "transitorio per studenti universitari."
    )

    arredato: bool = Field(
        False,
        description=ETICHETTE_MAGGIORAZIONI["arredato"] + ". Considerato solo per il contratto "
                    "agevolato e per il transitorio ordinario."
    )
    # era uno slider da 0 a 20 con default 20: se non viene inviato (None) si usa 20
    magg_arredo: Optional[float] = Field(
        None, ge=0, le=20,
        description=ETICHETTE_MAGGIORAZIONI["magg_arredo"] + ". Se omesso si usa il massimo (20%). "
                    "Considerato solo se arredato = true."
    )

    sociale: bool = Field(False, description=ETICHETTE_MAGGIORAZIONI["sociale"])



# INFO PER IL FRONTEND


INFO = {
    "id": "pisa",
    "nome": "Pisa",
    "titolo": "Calcolatore canone concordato - Comune di Pisa",
    "unita_fasce": "euro/mq mensili",
    "zonizzazione": zonizzazione,
    "lista_localita": LISTA_LOCALITA,
    "localita_lontane": localita_lontane,
    "fasce_tipo_A": fasce_tipo_A,
    "fasce_tipo_B": fasce_tipo_B,
    "fasce_tipo_C": fasce_tipo_C,
    "etichette_superficie": ETICHETTE_SUPERFICIE,
    "etichette_porzione": ETICHETTE_PORZIONE,
    "etichette_caratteristiche": ETICHETTE_CARATTERISTICHE,
    "etichette_maggiorazioni": ETICHETTE_MAGGIORAZIONI,
    "opzioni": {
        "tipo_contratto": OPZIONI_CONTRATTO,
        "categoria": OPZIONI_CATEGORIA,
        "riscaldamento": OPZIONI_RISCALDAMENTO,
        "servizi": OPZIONI_SERVIZI,
        "durata": OPZIONI_DURATA,
        "arredo_studenti": OPZIONI_ARREDO_STUDENTI
    },
    "note": [
        "La zona (Pregio, A, B, C, D) e' individuata in automatico dalla localita' tramite il "
        "dizionario zonizzazione. Gli alloggi situati nelle vie di confine tra due zone rientrano "
        "nella zona con il valore al mq piu' elevato.",
        "Fasce: ogni riga ha quattro valori [minimo, massimo, minimo, massimo]. I primi due valgono "
        "per gli edifici piu' vecchi della soglia, gli ultimi due per quelli piu' recenti. Soglie: "
        "10 anni per il Tipo A, 25 per il Tipo B, 50 per il Tipo C.",
        "Il tipo di immobile (A, B o C) e' ricavato in automatico dalle caratteristiche dell'art. 5.",
        "Superficie interna utile: fino a 45 mq e' aumentata del 20% (con il limite di 49,60 mq); "
        "fino a 70 mq del 10% (con il limite di 70 mq); oltre 110 mq e' ridotta del 10% (con il "
        "minimo di 110 mq).",
        "Maggiorazioni e riduzioni sono sommate tra loro (art. 8: cumulative e non progressive).",
        "Contratto transitorio ordinario: le fasce di oscillazione sono aumentate del 5%.",
        "Contratto per studenti: nelle localita' dell'elenco localita_lontane si applica il "
        "coefficiente correttivo di 0,9 (Capitolo III, punto 5).",
        NOTA_TRANSITORIO_BREVE,
        NOTA_PORZIONE
    ]
}



# CALCOLO (stessi passaggi, nello stesso ordine, del file Streamlit)


def calcola(dati: InputPisa) -> dict:
    note = []
    avvertenze = []

    tipo_contratto = dati.tipo_contratto

    if tipo_contratto.startswith("Contratto transitorio ordinario"):
        avvertenze.append(NOTA_TRANSITORIO_BREVE)

    localita = dati.localita

    if localita not in zonizzazione:
        raise HTTPException(
            status_code=400,
            detail="La localita' non e' stata trovata: usare uno dei nomi dell'elenco "
                   "lista_localita di GET /citta/pisa/info"
        )

    zona = zonizzazione[localita]

    # SUPERFICIE CONVENZIONALE

    mq_utile = dati.mq_utile
    mq_giardino = dati.mq_giardino
    mq_area_scoperta = dati.mq_area_scoperta

    if mq_utile <= 45.0:
        mq_utile_corretta = mq_utile * 1.20
        if mq_utile_corretta > 49.60:
            mq_utile_corretta = 49.60
    elif mq_utile <= 70.0:
        mq_utile_corretta = mq_utile * 1.10
        if mq_utile_corretta > 70.0:
            mq_utile_corretta = 70.0
    elif mq_utile <= 110.0:
        mq_utile_corretta = mq_utile
    else:
        mq_utile_corretta = mq_utile * 0.90
        if mq_utile_corretta < 110.0:
            mq_utile_corretta = 110.0

    if mq_giardino <= 100.0:
        mq_giardino_conv = mq_giardino * 0.10
    elif mq_giardino <= 200.0:
        mq_giardino_conv = mq_giardino * 0.15
    else:
        mq_giardino_conv = mq_giardino * 0.20

    mq_area_scoperta_conv = 0.0
    if mq_area_scoperta >= 100.0:
        mq_area_scoperta_conv = mq_area_scoperta * 0.10

    mq_finali = (mq_utile_corretta
                 + dati.mq_autorimessa * 0.60
                 + dati.mq_coperto * 0.40
                 + dati.mq_comune * 0.30
                 + dati.mq_scoperto * 0.20
                 + dati.mq_accessori * 0.25
                 + mq_giardino_conv
                 + mq_area_scoperta_conv)

    porzione = dati.porzione
    quota_porzione = 1.0
    if porzione == True:
        mq_esclusivi = dati.mq_esclusivi
        mq_spazi_comuni = dati.mq_spazi_comuni
        occupanti = dati.occupanti
        if mq_utile > 0.0:
            quota_porzione = (mq_esclusivi + mq_spazi_comuni / occupanti) / mq_utile
        if quota_porzione > 1.0:
            quota_porzione = 1.0
        note.append(NOTA_PORZIONE)

    # CLASSIFICAZIONE DELL'IMMOBILE (art. 5)

    categoria = dati.categoria
    anni = dati.anni
    car_a = dati.car_a
    car_b = dati.car_b
    riscaldamento = dati.riscaldamento
    servizi = dati.servizi
    car_e = dati.car_e
    car_f = dati.car_f
    car_h = dati.car_h
    car_i = dati.car_i

    # g) giardino esclusivo oltre il 40% della superficie utile: ricavato in automatico
    car_g = False
    if mq_utile > 0.0 and mq_giardino > mq_utile * 0.40:
        car_g = True

    car_c = False
    if riscaldamento.startswith("Efficiente e a norma in tutti"):
        car_c = True
    car_d = False
    if servizi.startswith("1)"):
        car_d = True

    caratteristiche_A = [car_a, car_b, car_c, car_d, car_e, car_f, car_g, car_h, car_i]
    n_caratteristiche = sum(x for x in caratteristiche_A if x == True)

    abbattimento_50 = False
    if car_a == False or car_b == False:
        tipo = "nessuno"
    elif (categoria.startswith("Altra") == False and car_c == True and n_caratteristiche >= 6):
        tipo = "A"
    elif riscaldamento.startswith("Assente") == False and (servizi.startswith("1)") or servizi.startswith("2)")):
        tipo = "B"
    elif servizi.startswith("1)") or servizi.startswith("2)") or servizi.startswith("3)"):
        tipo = "C"
    elif servizi.startswith("4)"):
        tipo = "C"
        abbattimento_50 = True
    else:
        tipo = "nessuno"

    if tipo == "nessuno":
        raise HTTPException(
            status_code=400,
            detail="L'alloggio non e' classificabile secondo l'art. 5: il canone non si puo' "
                   "calcolare. " + NOTA_NON_CLASSIFICABILE
        )

    if mq_utile <= 0.0:
        raise HTTPException(
            status_code=400,
            detail="Inserire la superficie interna utile per ottenere la stima"
        )

    if tipo == "A":
        valori = fasce_tipo_A[zona]
        vecchio = anni > 10
    elif tipo == "B":
        valori = fasce_tipo_B[zona]
        vecchio = anni > 25
    else:
        valori = fasce_tipo_C[zona]
        vecchio = anni > 50

    if vecchio == True:
        val_min = valori[0]
        val_max = valori[1]
        colonna = "edificio piu' vecchio della soglia"
    else:
        val_min = valori[2]
        val_max = valori[3]
        colonna = "edificio piu' recente della soglia"

    if abbattimento_50 == True:
        val_min = val_min * 0.50
        val_max = val_min
        note.append("Servizio igienico insufficiente o esterno: si applica il 50% del valore minimo.")

    canone_mq_base_min = val_min
    canone_mq_base_max = val_max

    # MAGGIORAZIONI E RIDUZIONI (sommate)

    perc_totale = 0.0

    if tipo == "B":
        rifinitura = False
        if mq_giardino > mq_utile and mq_utile > 0.0:
            rifinitura = True
        if car_d == True or car_h == True or car_i == True:
            rifinitura = True
        if rifinitura == True:
            magg_pregio = dati.magg_pregio
            if magg_pregio == True:
                perc_totale = perc_totale + 0.05

    popolare = dati.popolare
    if popolare == True:
        perc_totale = perc_totale - 0.20

    classe = dati.classe
    if classe == True:
        perc_totale = perc_totale + 0.05

    if tipo_contratto.startswith("Contratto agevolato"):
        durata = dati.durata
        if durata.startswith("Quattro"):
            perc_totale = perc_totale + 0.02
        elif durata.startswith("Cinque"):
            perc_totale = perc_totale + 0.04
        elif durata.startswith("Sei"):
            perc_totale = perc_totale + 0.06

    if tipo_contratto.startswith("Contratto transitorio ordinario"):
        perc_totale = perc_totale + 0.05
        note.append("Contratto transitorio: le fasce di oscillazione sono aumentate del 5%.")

    if tipo_contratto.startswith("Contratto transitorio per studenti"):
        arredo_studenti = dati.arredo_studenti
        if arredo_studenti.startswith("A)"):
            perc_totale = perc_totale + 0.10
        elif arredo_studenti.startswith("B)"):
            perc_totale = perc_totale + 0.15
        breve = dati.breve
        if breve == True:
            perc_totale = perc_totale - 0.10
        if localita in localita_lontane:
            perc_totale = perc_totale - 0.10
            note.append("Localita' troppo distante dalle sedi universitarie: coefficiente correttivo "
                        "di 0,9 (Capitolo III, punto 5).")
    else:
        arredato = dati.arredato
        if arredato == True:
            # lo slider aveva come default il massimo (20)
            if dati.magg_arredo is None:
                magg_arredo = 20
            else:
                magg_arredo = dati.magg_arredo
            perc_totale = perc_totale + magg_arredo / 100.0

    sociale = dati.sociale
    if sociale == True:
        perc_totale = perc_totale - 0.20

    val_min = val_min + val_min * perc_totale
    val_max = val_max + val_max * perc_totale

    canone_min = mq_finali * val_min * quota_porzione
    canone_max = mq_finali * val_max * quota_porzione

    return {
        "citta": "Pisa",
        "localita": localita,
        "zona": zona,
        "tipo": tipo,
        "caratteristiche_tipo_A": n_caratteristiche,
        "colonna": colonna,
        "superficie_interna_corretta": round(mq_utile_corretta, 2),
        "superficie_convenzionale": round(mq_finali, 2),
        "canone_mq_base_min": round(canone_mq_base_min, 2),
        "canone_mq_base_max": round(canone_mq_base_max, 2),
        "percentuale_maggiorazioni": round(perc_totale * 100, 2),
        "quota_porzione": round(quota_porzione, 4),
        "canone_mq_min": round(val_min, 4),
        "canone_mq_max": round(val_max, 4),
        "canone_mensile_min": round(canone_min, 2),
        "canone_mensile_max": round(canone_max, 2),
        "canone_annuo_min": round(canone_min * 12, 2),
        "canone_annuo_max": round(canone_max * 12, 2),
        "note": note,
        "avvertenze": avvertenze
    }
