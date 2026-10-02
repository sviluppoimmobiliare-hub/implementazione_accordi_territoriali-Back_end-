from typing import Literal, Optional
from pydantic import BaseModel, Field
from fastapi import HTTPException

FOGLI = {
    1: [2, 3, 4, 5, 8, 9, 13, 14, 15, 16, 20, 21, 22, 23],
    2: [25, 26, 28, 29, 32, 37],
    3: [1, 6, 7, 10, 11, 12, 17, 18, 19, 35, 36, 42, 43, 44, 45],
    4: [24, 30, 31, 33, 34, 38, 39, 40, 41]
}

NOMI_ZONE = {
    1: "Zona omogenea 1 - centrale",
    2: "Zona omogenea 2 - semicentrale",
    3: "Zona omogenea 3 - Colli",
    4: "Zona omogenea 4 - periferica"
}

TABELLA_CANONI = {
    1: {
        "unifamiliare": {1: (48.90, 62.87), 2: (62.87, 69.86), 3: (69.86, 76.84)},
        "oltre_111":    {1: (48.90, 55.89), 2: (55.89, 62.87), 3: (62.87, 69.86)},
        "da_96_a_110":  {1: (54.82, 61.67), 2: (61.67, 75.37), 3: (75.37, 82.23)},
        "da_71_a_95":   {1: (52.00, 60.67), 2: (60.67, 78.00), 3: (78.00, 86.67)},
        "da_51_a_70":   {1: (59.88, 71.85), 2: (71.85, 83.83), 3: (83.83, 95.81)},
        "fino_a_50":    {1: (70.73, 84.88), 2: (84.88, 99.03), 3: (99.03, 113.17)}
    },
    2: {
        "unifamiliare": {1: (34.93, 55.89), 2: (55.89, 62.87), 3: (62.87, 76.84)},
        "oltre_111":    {1: (34.93, 55.89), 2: (55.89, 62.87), 3: (62.87, 69.86)},
        "da_96_a_110":  {1: (47.96, 54.82), 2: (54.82, 68.52), 3: (68.52, 75.37)},
        "da_71_a_95":   {1: (52.00, 60.67), 2: (60.67, 78.00), 3: (78.00, 86.67)},
        "da_51_a_70":   {1: (59.88, 71.85), 2: (71.85, 95.81), 3: (95.81, 107.78)},
        "fino_a_50":    {1: (70.73, 84.88), 2: (84.88, 99.03), 3: (99.03, 113.17)}
    },
    3: {
        "unifamiliare": {1: (27.94, 41.91), 2: (41.91, 55.89), 3: (55.89, 69.86)},
        "oltre_111":    {1: (27.94, 41.91), 2: (41.91, 48.90), 3: (48.90, 62.87)},
        "da_96_a_110":  {1: (41.11, 47.96), 2: (47.96, 61.67), 3: (61.67, 75.37)},
        "da_71_a_95":   {1: (52.00, 60.67), 2: (60.67, 69.33), 3: (69.33, 78.00)},
        "da_51_a_70":   {1: (59.88, 71.85), 2: (71.85, 83.83), 3: (83.83, 95.81)},
        "fino_a_50":    {1: (70.73, 84.88), 2: (84.88, 99.03), 3: (99.03, 113.17)}
    },
    4: {
        "unifamiliare": {1: (20.96, 27.94), 2: (27.94, 41.91), 3: (41.91, 55.89)},
        "oltre_111":    {1: (20.96, 27.94), 2: (27.94, 41.91), 3: (41.91, 55.89)},
        "da_96_a_110":  {1: (41.11, 47.96), 2: (47.96, 61.67), 3: (61.67, 68.52)},
        "da_71_a_95":   {1: (43.33, 52.00), 2: (52.00, 69.33), 3: (69.33, 78.00)},
        "da_51_a_70":   {1: (59.88, 71.85), 2: (71.85, 83.83), 3: (83.83, 95.81)},
        "fino_a_50":    {1: (56.58, 70.73), 2: (70.73, 84.88), 3: (84.88, 99.03)}
    }
}

DESCRIZIONI_TIPOLOGIE = {
    "unifamiliare": "abitazione unifamiliare",
    "oltre_111": "unita' immobiliare con superficie superiore a 111 mq",
    "da_96_a_110": "unita' immobiliare con superficie da 96 a 110 mq",
    "da_71_a_95": "unita' immobiliare con superficie da 71 a 95 mq",
    "da_51_a_70": "unita' immobiliare con superficie da 51 a 70 mq",
    "fino_a_50": "unita' immobiliare con superficie fino a 50 mq"
}

ORDINE_RIGHE = ["fino_a_50", "da_51_a_70", "da_71_a_95", "da_96_a_110", "oltre_111"]
TETTO_RIGHE = {"fino_a_50": 50.0, "da_51_a_70": 70.0, "da_71_a_95": 95.0, "da_96_a_110": 110.0}

PERC_PERTINENZE_ZONA = {1: 1.00, 2: 0.75, 3: 0.50, 4: 0.50}

NOTA_ZONE_PREGIO = ("Zone di particolare pregio individuate dall'accordo: Viale Primo Vere (1 tratto), "
                    "Via O. Braga, Via Scarfoglio, Via L. D'Annunzio (ultimo tratto), Via Modesto della "
                    "Porta, Viale Figlia di Iorio, Via C. De Titta, Lungomare Matteotti (da Via Balilla), "
                    "Piazza 1 Maggio, Piazza della Rinascita, Viale Riviera, Viale Regina Elena, Viale "
                    "Regina Margherita, Viale Kennedy, Strada Parco, Via Solferino (tratto lato mare). "
                    "L'accordo non associa a tali zone una specifica maggiorazione del canone. Non sono "
                    "individuate zone di degrado.")

OPZIONI_CATEGORIA = ["Non disponibile / altra", "A/1", "A/2", "A/3 classe 1", "A/3 altre classi",
                     "A/4", "A/5", "A/6", "A/7", "A/8", "A/9", "A/11"]

OPZIONI_PARTE_27 = ["Sponda del fiume - zona portuale nord (Zona 1)", "Parte restante (Zona 2)"]

OPZIONI_MODO_SUPERFICIE = ["Si', da certificato catastale",
                           "No, la ricavo dalla planimetria catastale (criteri dell'art. 7)"]

ELEMENTI_A = [
    "A1 - Bagno interno completo di tutti gli elementi (tazza, lavabo, vasca da bagno o doccia) e con almeno una finestra o dispositivo di areazione meccanica",
    "A2 - Impianti tecnologici essenziali e funzionanti: adduzione acqua potabile, impianto predisposto per l'installazione di uno scaldabagno che eroghi acqua calda in bagno, impianto elettrico, impianto gas"
]

ELEMENTI_B = [
    "B1 - Cucina abitabile con almeno una finestra",
    "B2 - Ascensore per unita' abitative situate al 2 piano o piano superiore",
    "B3 - Stato di manutenzione e conservazione dell'unita' immobiliare normale in tutti i suoi elementi costitutivi: impianti tecnologici, infissi, pavimenti, pareti e soffitti",
    "B4 - Impianti tecnologici, di esalazione e scarico conformi alle norme igienico-sanitarie e di sicurezza vigenti alla data di stipula del contratto",
    "B5 - Riscaldamento centralizzato o autonomo"
]

ELEMENTI_C = [
    "C1 - Doppio bagno di cui almeno uno completo di tutti gli elementi (tazza, lavabo, vasca da bagno o doccia) e con almeno una finestra o dispositivo di aereazione meccanica",
    "C2 - Autorimessa o posto auto coperto (esclusivo o in comune)",
    "C3 - Giardino condominiale",
    "C4 - Stato di manutenzione e conservazione dell'unita' immobiliare buono in tutti i suoi elementi costitutivi, impianti tecnologici propri dell'abitazione, infissi, pavimenti, pareti e soffitti",
    "C5 - Stato di manutenzione e conservazione dello stabile normale in tutti i suoi elementi costitutivi: impianti tecnologici comuni, facciate, coperture, scale e spazi comuni interni",
    "C6 - Porte blindate e doppi vetri",
    "C7 - Prossimita' dell'abitazione all'insieme dei servizi: rete dei trasporti pubblici, esercizi commerciali e servizi sociali"
]

ELEMENTI_D = [
    "D1 - Presenza di elementi accessori: balconi o terrazzo",
    "D2 - Presenza di elementi funzionali: cantina o soffitta",
    "D3 - Appartamento con vetusta' inferiore a 30 anni, tranne che si tratti di immobile di pregio edilizio, ancorche' non vincolato ai sensi di legge",
    "D4 - Assenza di fonti specifiche di inquinamento ambientale ed acustico",
    "D5 - Affaccio esterno di pregio",
    "D6 - Giardino privato o spazio aperto esclusivo",
    "D7 - Posto auto scoperto",
    "D8 - Appartamento fatto oggetto, negli ultimi 15 anni, di intervento edilizio manutentivo con dichiarazione in Comune di inizio attivita' (D.I.A.) ovvero autorizzazione o concessione edilizia",
    "D9 - Terrazza di superficie superiore a 20 mq",
    "D10 - Impianto di climatizzazione",
    "D11 - Impianto di riscaldamento a pavimento",
    "D12 - Unita' immobiliare dotata di impianto di allarme",
    "D13 - Presenza di impianto di domotica"
]

OPZIONI_CONTRATTO = [
    "Agevolato 3 anni + 2 (art. 2, comma 3, L. 431/98)",
    "Transitorio, durata massima 18 mesi (art. 5, comma 1, L. 431/98)",
    "Transitorio per studenti universitari, da 6 mesi a 3 anni (art. 5, commi 2 e 3, L. 431/98)"
]

OPZIONI_DURATA = ["3 anni + 2 (ordinaria)", "4 anni (+5%)", "5 anni (+6%)", "6 o piu' anni (+7%)"]

OPZIONI_CLASSE_ENERGETICA = ["Non dichiarata", "A", "B", "C", "D", "E", "F", "G"]


class InputPescara(BaseModel):
    foglio: int = Field(
        ..., ge=1, le=45,
        description="Foglio di mappa catastale dell'immobile (1-45). Ogni edificio e' localizzato "
                    "nelle zone omogenee attraverso il foglio di mappa attribuito dal catasto urbano. "
                    "Gli edifici attraversati dalla linea di confine tra due zone sono inclusi nella "
                    "zona di maggior valore; i confini si intendono tracciati sulla mezzeria delle strade."
    )
    parte_27: Literal[
        "Sponda del fiume - zona portuale nord (Zona 1)",
        "Parte restante (Zona 2)"
    ] = Field(
        "Sponda del fiume - zona portuale nord (Zona 1)",
        description="Solo per il foglio 27, ripartito tra due zone (pag. 3 dell'accordo): dove "
                    "ricade l'immobile?"
    )

    categoria_catastale: Literal[
        "Non disponibile / altra", "A/1", "A/2", "A/3 classe 1", "A/3 altre classi",
        "A/4", "A/5", "A/6", "A/7", "A/8", "A/9", "A/11"
    ] = Field(
        "Non disponibile / altra",
        description="La categoria A/5 comporta la collocazione in sub-fascia 1; le categorie "
                    "A/3 classe 1, A/4 e A/6 non possono essere collocate in sub-fascia 3."
    )

    unifamiliare: bool = Field(False, description="L'immobile e' un'abitazione unifamiliare?")

    modo_superficie: Literal[
        "Si', da certificato catastale",
        "No, la ricavo dalla planimetria catastale (criteri dell'art. 7)"
    ] = Field("Si', da certificato catastale",
              description="La superficie catastale dell'abitazione e' disponibile?")
    mq_abitazione: float = Field(
        0.0, ge=0,
        description="Superficie catastale dell'abitazione in mq, comprensiva delle aree scoperte "
                    "(escluse le pertinenze da indicare a parte). Considerata solo con superficie "
                    "da certificato catastale."
    )
    mq_lordi: float = Field(
        0.0, ge=0,
        description="Superficie lorda dell'abitazione in mq ricavata dalla planimetria catastale "
                    "(ridotta del 10% ex art. 7). Considerata solo con superficie da planimetria."
    )
    presenti_balconi: bool = Field(False, description="Presenti balconi o terrazzi? (solo con "
                                                      "superficie da planimetria)")
    mq_balconi: float = Field(0.0, ge=0, description="Mq complessivi di balconi e terrazzi "
                                                     "(al 25% fino a 30 mq, 10% oltre; solo con "
                                                     "superficie da planimetria)")

    presente_garage: bool = Field(False, description="Presente garage o box di pertinenza?")
    mq_garage: float = Field(0.0, ge=0, description="Mq da certificazione catastale del garage o box")
    presente_cantina: bool = Field(False, description="Presente cantina di pertinenza? Indicare solo "
                                                      "se non gia' compresa nella superficie "
                                                      "catastale dell'abitazione.")
    mq_cantina: float = Field(0.0, ge=0, description="Mq da certificazione catastale della cantina")
    presente_posto_auto: bool = Field(False, description="Presente posto auto di pertinenza o "
                                                         "assegnato in via esclusiva?")
    mq_posto_auto: float = Field(0.0, ge=0, description="Mq del posto auto, da certificazione "
                                                        "catastale ovvero da misurazione")

    elementi_a: list[bool] = Field(
        default_factory=lambda: [False] * len(ELEMENTI_A),
        min_length=len(ELEMENTI_A), max_length=len(ELEMENTI_A),
        description="2 caselle true/false, nello stesso ordine della lista ELEMENTI_A "
                    "(vedi GET /citta/pescara/info)"
    )
    elementi_b: list[bool] = Field(
        default_factory=lambda: [False] * len(ELEMENTI_B),
        min_length=len(ELEMENTI_B), max_length=len(ELEMENTI_B),
        description="5 caselle true/false, nello stesso ordine della lista ELEMENTI_B "
                    "(vedi GET /citta/pescara/info)"
    )
    stufe: bool = Field(
        False,
        description="Immobile che, pur dotato di riscaldamento, e' riscaldato con stufe nei singoli "
                    "locali, comunque alimentate. Comporta la collocazione in sub-fascia 1, fatta "
                    "eccezione per gli immobili che hanno almeno quattro elementi di tipo B. "
                    "Incompatibile con l'elemento B5."
    )
    elementi_c: list[bool] = Field(
        default_factory=lambda: [False] * len(ELEMENTI_C),
        min_length=len(ELEMENTI_C), max_length=len(ELEMENTI_C),
        description="7 caselle true/false, nello stesso ordine della lista ELEMENTI_C "
                    "(vedi GET /citta/pescara/info)"
    )
    elementi_d: list[bool] = Field(
        default_factory=lambda: [False] * len(ELEMENTI_D),
        min_length=len(ELEMENTI_D), max_length=len(ELEMENTI_D),
        description="13 caselle true/false, nello stesso ordine della lista ELEMENTI_D "
                    "(vedi GET /citta/pescara/info)"
    )

    contratto: Literal[
        "Agevolato 3 anni + 2 (art. 2, comma 3, L. 431/98)",
        "Transitorio, durata massima 18 mesi (art. 5, comma 1, L. 431/98)",
        "Transitorio per studenti universitari, da 6 mesi a 3 anni (art. 5, commi 2 e 3, L. 431/98)"
    ] = "Agevolato 3 anni + 2 (art. 2, comma 3, L. 431/98)"
    durata: Literal[
        "3 anni + 2 (ordinaria)", "4 anni (+5%)", "5 anni (+6%)", "6 o piu' anni (+7%)"
    ] = Field("3 anni + 2 (ordinaria)",
              description="Durata del contratto (art. 15). Considerata solo per il contratto agevolato.")
    perc_transitorio: int = Field(
        0, ge=0, le=15,
        description="Incremento concordato per il contratto transitorio (fino al 15%, punto 20 "
                    "dell'accordo). Considerato solo per il contratto transitorio."
    )
    perc_studenti: int = Field(
        0, ge=0, le=20,
        description="Incremento concordato per il contratto per studenti universitari (fino al 20%, "
                    "punto 22 dell'accordo). Considerato solo per il contratto studenti."
    )
    ammobiliato: bool = Field(False, description="Alloggio ammobiliato, con mobilio efficiente ed "
                                                 "elettrodomestici funzionanti (art. 11)?")
    perc_arredo: int = Field(
        0, ge=0, le=15,
        description="Aumento concordato per l'arredo (fino ad un massimo del 15%). Considerato solo "
                    "se ammobiliato = true."
    )
    classe_energetica: Literal[
        "Non dichiarata", "A", "B", "C", "D", "E", "F", "G"
    ] = "Non dichiarata"
    perc_energia: int = Field(
        0, ge=0, le=8,
        description="Aumento concordato per la classe energetica (art. 12): fino all'8% per la "
                    "classe A, fino al 4% per la classe B. Considerato solo per le classi A e B."
    )

    locazione_parziale: bool = Field(False, description="Viene locata solo una porzione dell'immobile?")
    mq_porzione: float = Field(0.0, ge=0, description="Mq della porzione locata, anche considerando "
                                                      "parti e servizi condivisi. Considerati solo se "
                                                      "locazione_parziale = true.")

    grande_proprietario: bool = Field(
        False,
        description="Il locatore e' un grande proprietario (disponibilita' di piu' di 30 unita' "
                    "immobiliari ad uso abitativo, anche ubicate in modo diffuso e frazionato sul "
                    "territorio comunale)?"
    )

INFO = {
    "id": "pescara",
    "nome": "Pescara",
    "titolo": "Calcolatore Canone Concordato - Comune di Pescara",
    "accordo": "Accordo territoriale del 29.05.2018 - Legge 431/98 - D.M. 16.01.2017. Valori della "
               "tabella 1 dell'accordo; l'accordo prevede l'aggiornamento annuale delle fasce nella "
               "misura del 75% della variazione dell'indice Istat FOI, non applicato dal calcolatore.",
    "unita_fasce": "euro/mq annui",
    "fogli_zone": FOGLI,
    "nomi_zone": NOMI_ZONE,
    "nota_zone_pregio": NOTA_ZONE_PREGIO,
    "elementi_a": ELEMENTI_A,
    "elementi_b": ELEMENTI_B,
    "elementi_c": ELEMENTI_C,
    "elementi_d": ELEMENTI_D,
    "descrizioni_tipologie": DESCRIZIONI_TIPOLOGIE,
    "opzioni": {
        "parte_27": OPZIONI_PARTE_27,
        "categoria_catastale": OPZIONI_CATEGORIA,
        "modo_superficie": OPZIONI_MODO_SUPERFICIE,
        "contratto": OPZIONI_CONTRATTO,
        "durata": OPZIONI_DURATA,
        "classe_energetica": OPZIONI_CLASSE_ENERGETICA
    },
    "note": [
        "Il garage o posto auto di pertinenza sono in ogni caso inclusi nel contratto e la relativa "
        "superficie catastale, ridotta in base alla zona, concorre ai mq utili: garage, box e cantina "
        "al 100% in Zona 1, non oltre il 75% in Zona 2, non oltre il 50% nelle Zone 3 e 4; posto "
        "auto non oltre il 10% (art. 7).",
        "I mq utili dell'unita' immobiliare e delle relative pertinenze sono calcolati con una "
        "tolleranza del 5% in piu' o in meno (art. 7).",
        "Elementi di tipo D: l'assenza implica il valore minimo della sub-fascia; la presenza di "
        "almeno cinque elementi consente il valore massimo; da 1 a 4 elementi collocano il canone in "
        "tanti quinti della differenza tra minimo e massimo quanti sono gli elementi presenti.",
        "E' consentito alle parti concordare anche un canone inferiore alla sub-fascia di "
        "appartenenza (pag. 6 dell'accordo)."
    ]
}


def calcola(dati: InputPescara) -> dict:
    avvertenze = []
    note = []

    zona = 0
    for k in FOGLI.keys():
        if dati.foglio in FOGLI[k]:
            zona = k

    if dati.foglio == 27:
        if dati.parte_27 == "Sponda del fiume - zona portuale nord (Zona 1)":
            zona = 1
        else:
            zona = 2

    if zona == 0:
        raise HTTPException(
            status_code=400,
            detail="Il foglio di mappa non e' stato trovato nelle zone omogenee dell'accordo"
        )

    mq_abitazione = 0.0
    if dati.modo_superficie == "Si', da certificato catastale":
        mq_abitazione = dati.mq_abitazione
    else:
        mq_abitazione = dati.mq_lordi * 0.90
        if dati.presenti_balconi:
            mq_balconi = dati.mq_balconi
            if mq_balconi > 30.0:
                mq_abitazione = mq_abitazione + 30.0 * 0.25 + (mq_balconi - 30.0) * 0.10
            else:
                mq_abitazione = mq_abitazione + mq_balconi * 0.25

    mq_pertinenze = 0.0
    if dati.presente_garage:
        mq_pertinenze = mq_pertinenze + dati.mq_garage * PERC_PERTINENZE_ZONA[zona]
    if dati.presente_cantina:
        mq_pertinenze = mq_pertinenze + dati.mq_cantina * PERC_PERTINENZE_ZONA[zona]
    if dati.presente_posto_auto:
        mq_pertinenze = mq_pertinenze + dati.mq_posto_auto * 0.10

    mq_utili = mq_abitazione + mq_pertinenze

    if mq_utili <= 0.0:
        raise HTTPException(
            status_code=400,
            detail="Inserire la superficie dell'abitazione: i metri quadrati utili per il calcolo "
                   "devono essere maggiori di zero"
        )

    if dati.unifamiliare == True:
        tipologia = "unifamiliare"
    elif mq_utili > 111.0:
        tipologia = "oltre_111"
    elif mq_utili > 95.0:
        tipologia = "da_96_a_110"
    elif mq_utili > 70.0:
        tipologia = "da_71_a_95"
    elif mq_utili > 50.0:
        tipologia = "da_51_a_70"
    else:
        tipologia = "fino_a_50"

    if dati.stufe == True and dati.elementi_b[4] == True:
        raise HTTPException(
            status_code=400,
            detail="Opzioni incompatibili: il riscaldamento con stufe nei singoli locali esclude "
                   "l'elemento B5 (riscaldamento centralizzato o autonomo). Correggere per ottenere "
                   "la stima."
        )

    tutti_a = dati.elementi_a[0] == True and dati.elementi_a[1] == True
    conta_b = sum(el for el in dati.elementi_b if el == True)
    conta_c = sum(el for el in dati.elementi_c if el == True)

    if tutti_a == False or dati.categoria_catastale == "A/5":
        sub_fascia = 1
        motivo_sub_fascia = "manca almeno un elemento di tipo A oppure tipologia catastale A/5"
    elif dati.stufe == True and conta_b < 4:
        sub_fascia = 1
        motivo_sub_fascia = "riscaldamento con stufe nei singoli locali e meno di quattro elementi di tipo B"
    elif conta_b < 3:
        sub_fascia = 1
        motivo_sub_fascia = "meno di tre elementi di tipo B"
    elif conta_c < 3:
        sub_fascia = 2
        motivo_sub_fascia = ("tutti gli elementi di tipo A, almeno tre elementi di tipo B e meno di "
                             "tre elementi di tipo C")
    elif dati.categoria_catastale in ["A/3 classe 1", "A/4", "A/6"]:
        sub_fascia = 2
        motivo_sub_fascia = ("requisiti per la sub-fascia 3 presenti, ma collocazione preclusa alle "
                             "tipologie catastali A/3 classe 1, A/4 e A/6")
    else:
        sub_fascia = 3
        motivo_sub_fascia = ("tutti gli elementi di tipo A, almeno tre elementi di tipo B e tre "
                             "elementi di tipo C")

    conta_d = sum(el for el in dati.elementi_d if el == True)
    quinti = conta_d
    if quinti > 5:
        quinti = 5

    can_min, can_max = TABELLA_CANONI[zona][tipologia][sub_fascia]
    can_mq = can_min + (can_max - can_min) * quinti / 5.0

    canone_base = mq_utili * can_mq
    nota_riga_inferiore = ""
    if tipologia in ORDINE_RIGHE:
        riferimento = 0.0
        indice_riga = ORDINE_RIGHE.index(tipologia)
        for riga in ORDINE_RIGHE[:indice_riga]:
            rif_min, rif_max = TABELLA_CANONI[zona][riga][sub_fascia]
            rif_mq = rif_min + (rif_max - rif_min) * quinti / 5.0
            if rif_mq * TETTO_RIGHE[riga] > riferimento:
                riferimento = rif_mq * TETTO_RIGHE[riga]
        if riferimento > canone_base:
            canone_base = riferimento
            nota_riga_inferiore = (f"Applicata la regola della riga immediatamente inferiore (pag. 5 "
                                   f"dell'accordo): il canone annuo di base e' allineato a "
                                   f"{riferimento:.2f} euro, risultato della riga di superficie "
                                   f"inferiore, in quanto superiore a quello della riga di appartenenza.")
    else:
        rif_min, rif_max = TABELLA_CANONI[zona]["oltre_111"][sub_fascia]
        rif_mq = rif_min + (rif_max - rif_min) * quinti / 5.0
        if rif_mq * mq_utili > canone_base:
            canone_base = rif_mq * mq_utili
            nota_riga_inferiore = "Applicata la regola della riga immediatamente inferiore (pag. 5 dell'accordo)."

    if nota_riga_inferiore != "":
        note.append(nota_riga_inferiore)

    perc_totale = 0.0

    if dati.contratto == "Agevolato 3 anni + 2 (art. 2, comma 3, L. 431/98)":
        if dati.durata == "4 anni (+5%)":
            perc_totale = perc_totale + 0.05
        elif dati.durata == "5 anni (+6%)":
            perc_totale = perc_totale + 0.06
        elif dati.durata == "6 o piu' anni (+7%)":
            perc_totale = perc_totale + 0.07
    elif dati.contratto == "Transitorio, durata massima 18 mesi (art. 5, comma 1, L. 431/98)":
        perc_totale = perc_totale + dati.perc_transitorio / 100.0
    else:
        perc_totale = perc_totale + dati.perc_studenti / 100.0

    if dati.ammobiliato:
        perc_totale = perc_totale + dati.perc_arredo / 100.0

    if dati.classe_energetica == "A":
        perc_totale = perc_totale + dati.perc_energia / 100.0
    elif dati.classe_energetica == "B":
        if dati.perc_energia > 4:
            raise HTTPException(
                status_code=400,
                detail="Per la classe energetica B l'aumento concordato non puo' superare il 4%"
            )
        perc_totale = perc_totale + dati.perc_energia / 100.0
    elif dati.classe_energetica == "E":
        perc_totale = perc_totale - 0.02
        note.append("Classe E: decremento del 2%")
    elif dati.classe_energetica == "F":
        perc_totale = perc_totale - 0.04
        note.append("Classe F: decremento del 4%")
    elif dati.classe_energetica == "G":
        perc_totale = perc_totale - 0.06
        note.append("Classe G: decremento del 6%")

    frazione_parziale = 1.0
    if dati.locazione_parziale:
        if dati.mq_porzione <= 0.0:
            raise HTTPException(
                status_code=400,
                detail="Inserire la superficie della porzione locata per ottenere la stima"
            )
        elif dati.mq_porzione > mq_utili:
            raise HTTPException(
                status_code=400,
                detail="La superficie della porzione locata supera i mq utili complessivi: "
                       "correggere per ottenere la stima"
            )
        else:
            frazione_parziale = dati.mq_porzione / mq_utili
            note.append(f"Il canone dell'intero appartamento, calcolato in base ai criteri "
                        f"dell'accordo, e' frazionato in proporzione alla superficie della porzione "
                        f"locata: quota del {frazione_parziale * 100.0:.2f}%")

    if dati.grande_proprietario:
        avvertenze.append(
            "Grandi proprieta' (Capo III): i canoni sono definiti, all'interno dei valori minimi e "
            "massimi delle fasce di oscillazione, in base ad appositi accordi integrativi fra la "
            "proprieta' e le organizzazioni sindacali. La stima ha valore soltanto indicativo."
        )

    canone_annuo = canone_base * (1.0 + perc_totale) * frazione_parziale
    canone_mensile = canone_annuo / 12.0

    avvertenze.append("I mq utili dell'unita' immobiliare e delle relative pertinenze sono calcolati "
                      "con una tolleranza del 5% in piu' o in meno (art. 7).")
    avvertenze.append("E' consentito alle parti concordare anche un canone inferiore alla sub-fascia "
                      "di appartenenza (pag. 6 dell'accordo).")

    return {
        "citta": "Pescara",
        "foglio": dati.foglio,
        "zona": zona,
        "nome_zona": NOMI_ZONE[zona],
        "mq_utili": round(mq_utili, 2),
        "tipologia": tipologia,
        "descrizione_tipologia": DESCRIZIONI_TIPOLOGIE[tipologia],
        "sub_fascia": sub_fascia,
        "motivo_sub_fascia": motivo_sub_fascia,
        "fascia_mq_annuo_min": round(can_min, 2),
        "fascia_mq_annuo_max": round(can_max, 2),
        "elementi_d_presenti": conta_d,
        "canone_unitario_mq_annuo": round(can_mq, 2),
        "percentuale_maggiorazioni": round(perc_totale * 100, 2),
        "frazione_parziale": round(frazione_parziale, 4),
        "canone_annuo": round(canone_annuo, 2),
        "canone_mensile": round(canone_mensile, 2),
        "note": note,
        "avvertenze": avvertenze
    }
