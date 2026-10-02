import math
from typing import Literal, Optional
from pydantic import BaseModel, Field
from fastapi import HTTPException

OPZIONI_CATEGORIA_CATASTALE = [
    "A/1", "A/2", "A/3", "A/4", "A/5", "A/7", "A/8", "A/9",
    "A/6 - non ammessa", "A/10 - non ammessa", "A/11 - non ammessa",
]

QUARTIERI_ZONA2 = [
    "San Prospero", "Saragino", "Cappuccini", "Marciano", "Uncinello",
    "Stazione Ferroviaria", "Vico Alto", "Viale Bracci", "Scacciapensieri",
    "Malizia", "Ravacciano", "Madonnina Rossa", "Due Ponti", "Str. Di Busseto",
    "Derna", "Valli", "Coroncina", "Massetana Romana", "Colonna San Marco",
    "Pescaia", "Via Ricasoli", "Via Vittorio Emanuele", "Viale Cavour",
    "Palazzo dei Diavoli", "Via Celso Cittadini", "Via Quinto Settano",
    "Via Sansedoni", "Via Bernardo Tolomei", "Petriccio", "Acquacalda",
    "Policlinico", "San Miniato", "Stellino", "Montarioso",
]

QUARTIERI_ZONA3 = [
    "Bottega Nuova", "Malafrasca", "Ponte a Bozzone", "Vico d'Arbia",
    "Pieve al Bozzone", "Presciano", "Taverne d'Arbia", "Ruffolo", "l'Abbadia",
    "Isola d'Arbia", "Costafabbri", "Costalpino", "Volte Basse", "S. Andrea",
    "S. Rocco a Pilli", "Terrenzano", "Montalbuccio", "Casciano delle Masse",
]

ZONE = {
    "ZONA 1 - CENTRO STORICO": "Tutta l'area entro la cinta muraria della citta'.",
    "ZONA 2 - SEMICENTRALE": ", ".join(QUARTIERI_ZONA2) + ".",
    "ZONA 3 - PERIFERICA": ", ".join(QUARTIERI_ZONA3) + ".",
}

MAPPA_QUARTIERI = {"Centro storico (entro la cinta muraria)": "ZONA 1 - CENTRO STORICO"}
for q in QUARTIERI_ZONA2:
    MAPPA_QUARTIERI[q] = "ZONA 2 - SEMICENTRALE"
for q in QUARTIERI_ZONA3:
    MAPPA_QUARTIERI[q] = "ZONA 3 - PERIFERICA"

OPZIONI_QUARTIERI = (["Centro storico (entro la cinta muraria)"] +
                     sorted(QUARTIERI_ZONA2 + QUARTIERI_ZONA3, key=str.lower) +
                     ["Altro (selezione manuale della zona)"])

FASCE = {
    "ZONA 1 - CENTRO STORICO": {"A": (2.50, 10.84), "B": (2.50, 9.22), "C": (2.50, 8.13)},
    "ZONA 2 - SEMICENTRALE":   {"A": (2.50, 9.76),  "B": (2.50, 8.29), "C": (2.50, 7.32)},
    "ZONA 3 - PERIFERICA":     {"A": (2.50, 8.68),  "B": (2.50, 5.71), "C": (2.50, 5.04)},
}

ETICHETTE_SUPERFICIE = {
    "sup_a": "Superficie interna utile abitativa in mq (area calpestabile, esclusi muri e palchi morti)",
    "sup_b": "Autorimessa singola o box auto in mq (conteggiata al 50%)",
    "sup_c": "Lastrici solari di uso esclusivo al piano attico in mq (25% fino ai mq utili, 5% sull'eccedenza)",
    "sup_d": "Posto auto coperto in comune in mq (conteggiato al 30%)",
    "sup_e": "Posto auto scoperto in comune in mq (conteggiato al 20%)",
    "sup_f": "Balconi, terrazze, lastrici solari non all'attico, cantine, soffitte in mq (conteggiati al 30%)",
    "sup_g": "Superficie scoperta di pertinenza in godimento esclusivo in mq (20%, con risultanza fino alla superficie utile)",
    "sup_h": "Superficie scoperta in uso condominiale in mq (conteggiata al 2%)",
    "sup_vani_bassi": "Superficie interna dei vani con altezza utile inferiore a 1,70 m in mq (detratta al 30%)"
}

CRITERI_TIPOLOGIA = (
    "- Tipologia A: lavori ultimati entro 30 anni con ammodernamento degli impianti "
    "elettrico/idrico/sanitario; servizio igienico completo con almeno 4 apparecchi e "
    "finestra/areazione; cantina e/o garage e/o posto auto. Gli immobili nei centri storici si "
    "considerano di tipologia A anche senza cantina/garage/posto auto se in presenza di tutti gli "
    "altri requisiti.\n"
    "- Tipologia B: lavori ultimati oltre il 30 anno con ammodernamento degli impianti; servizio "
    "igienico completo (almeno 4 apparecchi) oppure incompleto/con meno di 4 apparecchi.\n"
    "- Tipologia C: lavori ultimati oltre il 50 anno e almeno due tra: assenza di riscaldamento; "
    "assenza contemporanea di garage, posto auto e cantina (tutti e tre); assenza del servizio "
    "igienico o non interno all'immobile; assenza di infissi efficienti."
)

OPZIONI_CONTRATTO = [
    "Abitativo agevolato 3+2 (durata minima)",
    "Abitativo agevolato 4+2 (+4%)",
    "Abitativo agevolato 5+2 (+5%)",
    "Abitativo agevolato 6+2 e oltre (+10%)",
    "Transitorio (max 18 mesi)",
    "Studenti universitari (6 mesi - 3 anni)",
]

OPZIONI_ARREDO = ["Non arredato", "Parzialmente arredato", "Completamente arredato"]


def arrotonda_euro(x):
    return int(math.floor(x + 0.5))


class InputSiena(BaseModel):
    categoria_catastale: Literal[
        "A/1", "A/2", "A/3", "A/4", "A/5", "A/7", "A/8", "A/9",
        "A/6 - non ammessa", "A/10 - non ammessa", "A/11 - non ammessa"
    ] = "A/1"

    quartiere: str = Field(
        "Centro storico (entro la cinta muraria)",
        description="Quartiere / localita' di ubicazione dell'immobile. I valori ammessi sono "
                    "nell'elenco 'quartieri' di GET /citta/siena/info; per le localita' non in "
                    "elenco usare 'Altro (selezione manuale della zona)' e compilare zona_manuale."
    )
    zona_manuale: Literal[
        "ZONA 1 - CENTRO STORICO",
        "ZONA 2 - SEMICENTRALE",
        "ZONA 3 - PERIFERICA"
    ] = Field(
        "ZONA 1 - CENTRO STORICO",
        description="Zona di ubicazione dell'immobile: considerata solo se quartiere = "
                    "'Altro (selezione manuale della zona)'."
    )

    sup_a: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_a"])
    sup_b: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_b"])
    sup_c: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_c"])
    sup_d: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_d"])
    sup_e: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_e"])
    sup_f: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_f"])
    sup_g: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_g"])
    sup_h: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_h"])
    sup_vani_bassi: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_vani_bassi"])

    incremento_25: bool = Field(
        True,
        description="Applica l'incremento del 25% per immobili con superficie fino a 60 mq "
                    "(facolta', art. 6). La superficie aumentata non puo' superare i 60 mq. "
                    "Considerato solo se la superficie base e' compresa tra 0 e 60 mq."
    )

    tipologia: Literal["A", "B", "C"] = "A"

    grande_proprieta: bool = Field(
        False,
        description="Locatore rientrante tra le grandi proprieta' o gli enti dell'art. 17 c.1 "
                    "(soggetti detentori di piu' di 100 unita' immobiliari ad uso abitativo, enti "
                    "previdenziali, istituti di credito, compagnie assicurative, fondi immobiliari, "
                    "enti locali, cooperative...). La stima ha in tal caso valore solo indicativo."
    )
    alloggio_sociale: bool = Field(
        False,
        description="Alloggio sociale (art. 17 c.2 - art. 2 c.3 D.M. 22/04/2008): il canone base "
                    "massimo e' limitato al valore della tipologia B della zona."
    )

    tipo_contratto: Literal[
        "Abitativo agevolato 3+2 (durata minima)",
        "Abitativo agevolato 4+2 (+4%)",
        "Abitativo agevolato 5+2 (+5%)",
        "Abitativo agevolato 6+2 e oltre (+10%)",
        "Transitorio (max 18 mesi)",
        "Studenti universitari (6 mesi - 3 anni)"
    ] = "Abitativo agevolato 3+2 (durata minima)"

    arredo: Literal["Non arredato", "Parzialmente arredato", "Completamente arredato"] = "Non arredato"

    art9c2: bool = Field(
        False,
        description="Immobile con TUTTE le caratteristiche dell'art. 9 c.2 (+15%): a) nuovo entro 10 "
                    "anni oppure ristrutturato/risanato con lavori ultimati entro 10 anni e "
                    "ammodernamento impianti; b) APE in classe da A a E; c) ascensore per unita' dal "
                    "terzo piano in poi (non pertinente sotto il terzo piano)."
    )
    storico: bool = Field(
        False,
        description="Immobile di interesse storico-artistico (+15%): ex L. 364/1909, L. 1089/1939, "
                    "D.Lgs. 490/1999, D.Lgs. 42/2004. Stessa maggiorazione dell'art. 9 c.2, applicata "
                    "una sola volta anche se ricorrono entrambe le condizioni."
    )

    porzione: bool = Field(
        False,
        description="Locazione di porzioni di immobile (calcolo del canone per singole camere)"
    )
    superfici_camere: list[float] = Field(
        default_factory=list,
        max_length=10,
        description="Superfici ad uso esclusivo delle camere in mq (comprese le eventuali pertinenze "
                    "esclusive; comprese le camere non locate o riservate al locatore). "
                    "Considerate solo se porzione = true. Massimo 10 camere."
    )


INFO = {
    "id": "siena",
    "nome": "Siena",
    "titolo": "Calcolatore Canone Concordato - Comune di Siena",
    "accordo": "Accordo Territoriale per il Comune di Siena sottoscritto il 07/04/2026, con validita' "
               "dal 01/05/2026 (art. 2, comma 3, L. 431/98 e D.M. 16/01/2017)",
    "unita_fasce": "euro/mq mensili",
    "zone": ZONE,
    "quartieri": OPZIONI_QUARTIERI,
    "nota_quartieri": "L'elenco dei quartieri della zona semicentrale e' esemplificativo (art. 4: "
                      "'ad esempio'): per le localita' non in elenco selezionare 'Altro (selezione "
                      "manuale della zona)' e indicare la zona di appartenenza.",
    "etichette_superficie": ETICHETTE_SUPERFICIE,
    "criteri_tipologia": CRITERI_TIPOLOGIA,
    "opzioni": {
        "categoria_catastale": OPZIONI_CATEGORIA_CATASTALE,
        "zona_manuale": list(ZONE.keys()),
        "tipologia": ["A", "B", "C"],
        "tipo_contratto": OPZIONI_CONTRATTO,
        "arredo": OPZIONI_ARREDO
    },
    "note": [
        "Arredo (art. 9 c.1 - art. 16 c.4): contratti ordinari/transitori completo +15%, parziale "
        "+10%; contratti per studenti universitari completo +25%, parziale +15%. Per i contratti "
        "studenti l'alloggio 'completamente ammobiliato' richiede la dotazione dell'art. 16 c.4.",
        "Superficie lett. F: l'elenco letterale dell'art. 6 comprende anche i 'garage'; per evitare "
        "il doppio conteggio con la lett. B inserire qui solo eventuali garage NON conteggiati come "
        "autorimessa singola o box auto (punto da verificare con le organizzazioni firmatarie).",
        "Vani bassi: la superficie interna utile abitativa considera gia' come non calpestabili le "
        "aree con altezza inferiore a 170 cm; compilare il campo solo se la superficie e' stata "
        "misurata al lordo di tali vani.",
        "Art. 11: le maggiorazioni si applicano SEMPRE sul solo canone base come somma aritmetica "
        "delle singole percentuali (non in modo progressivo).",
        "Art. 12: il canone di riparto per porzioni e' calcolato senza la maggiorazione arredo; le "
        "eventuali pertinenze esclusive di una camera vanno sommate alla sua superficie (bagno "
        "privato per intero; balcone, posto auto ecc. secondo le percentuali dell'art. 6). Vanno "
        "conteggiate anche le camere che il locatore riserva per se' o che non vengono locate.",
        "Art. 20: il canone finale e' arrotondato all'unita' di euro (per eccesso se la frazione "
        "decimale e' >= 0,50, per difetto se inferiore)."
    ]
}


def calcola(dati: InputSiena) -> dict:
    avvertenze = []

    if "non ammessa" in dati.categoria_catastale:
        avvertenze.append(
            "L'art. 7 ammette ai contratti del presente accordo solo le unita' immobiliari destinate "
            "a civile abitazione delle categorie catastali A/1, A/2, A/3, A/4, A/5, A/7, A/8, A/9: "
            "la categoria selezionata e' esclusa."
        )

    if dati.quartiere == "Altro (selezione manuale della zona)":
        zona = dati.zona_manuale
    elif dati.quartiere in MAPPA_QUARTIERI:
        zona = MAPPA_QUARTIERI[dati.quartiere]
    else:
        raise HTTPException(
            status_code=400,
            detail="Quartiere non riconosciuto: usare uno dei valori dell'elenco 'quartieri' di "
                   "GET /citta/siena/info oppure 'Altro (selezione manuale della zona)' con il "
                   "campo zona_manuale"
        )

    if dati.sup_c <= dati.sup_a:
        quota_c = dati.sup_c * 0.25
    else:
        quota_c = dati.sup_a * 0.25 + (dati.sup_c - dati.sup_a) * 0.05

    quota_g = min(dati.sup_g * 0.20, dati.sup_a)

    superficie_base = (dati.sup_a + dati.sup_b * 0.50 + quota_c + dati.sup_d * 0.30 +
                       dati.sup_e * 0.20 + dati.sup_f * 0.30 + quota_g + dati.sup_h * 0.02)

    incremento_25 = False
    if 0 < superficie_base <= 60:
        incremento_25 = dati.incremento_25

    if incremento_25:
        superficie_convenzionale = min(superficie_base * 1.25, 60.0)
    else:
        superficie_convenzionale = superficie_base

    superficie_convenzionale = max(superficie_convenzionale - dati.sup_vani_bassi * 0.30, 0.0)

    if dati.grande_proprieta:
        avvertenze.append(
            "Art. 17 c.1: per le grandi proprieta' i canoni sono definiti in base ad appositi e "
            "specifici Accordi integrativi tra la proprieta' interessata e le organizzazioni "
            "firmatarie dell'accordo. I valori di questo calcolatore hanno quindi valore solo "
            "indicativo."
        )

    base_min, base_max = FASCE[zona][dati.tipologia]

    if dati.alloggio_sociale:
        base_b_max = FASCE[zona]["B"][1]
        if base_max > base_b_max:
            base_max = base_b_max
            avvertenze.append(
                f"Alloggio sociale (art. 17 c.2): canone base massimo limitato al valore della "
                f"tipologia B della zona ({base_b_max:.2f} euro/mq mensile)."
            )
        avvertenze.append(
            "Le agevolazioni pubbliche spettanti al locatore costituiscono elemento oggettivo di "
            "ulteriore riduzione del canone massimo (art. 17 c.2 e art. 1 c.7 D.M. 16/01/2017), non "
            "quantificata dall'accordo: in loro presenza il massimale indicato va ridotto di "
            "conseguenza."
        )

    studenti = "Studenti" in dati.tipo_contratto

    if dati.art9c2 and dati.storico:
        avvertenze.append(
            "L'art. 9 c.2 prevede un'unica maggiorazione del 15%: il vincolo storico-artistico e' "
            "una via alternativa di accesso alla stessa maggiorazione, che pertanto NON si cumula e "
            "viene applicata una sola volta."
        )

    perc_arredo = 0.0
    perc_altre = 0.0

    if dati.arredo == "Completamente arredato":
        perc_arredo = 0.25 if studenti else 0.15
    elif dati.arredo == "Parzialmente arredato":
        perc_arredo = 0.15 if studenti else 0.10

    if dati.art9c2 or dati.storico:
        perc_altre += 0.15

    if "4+2" in dati.tipo_contratto:
        perc_altre += 0.04
    elif "5+2" in dati.tipo_contratto:
        perc_altre += 0.05
    elif "6+2" in dati.tipo_contratto:
        perc_altre += 0.10

    perc = perc_arredo + perc_altre

    magg_mq = base_max * perc
    canone_mq_min = base_min + magg_mq
    canone_mq_max = base_max + magg_mq

    can_mensile_min = canone_mq_min * superficie_convenzionale
    can_mensile_max = canone_mq_max * superficie_convenzionale
    arr_min = arrotonda_euro(can_mensile_min)
    arr_max = arrotonda_euro(can_mensile_max)

    risultato = {
        "citta": "Siena",
        "quartiere": dati.quartiere,
        "zona": zona,
        "superficie_convenzionale": round(superficie_convenzionale, 2),
        "tipologia": dati.tipologia,
        "canone_base_mq_min": round(base_min, 2),
        "canone_base_mq_max": round(base_max, 2),
        "maggiorazioni_percentuale": round(perc * 100, 2),
        "canone_mq_mensile_min": round(canone_mq_min, 2),
        "canone_mq_mensile_max": round(canone_mq_max, 2),
        "canone_mensile_min": arr_min,
        "canone_mensile_max": arr_max,
        "canone_annuo_min": arr_min * 12,
        "canone_annuo_max": arr_max * 12,
        "canone_mensile_min_non_arrotondato": round(can_mensile_min, 2),
        "canone_mensile_max_non_arrotondato": round(can_mensile_max, 2),
        "canone_annuo_min_non_arrotondato": round(can_mensile_min * 12, 2),
        "canone_annuo_max_non_arrotondato": round(can_mensile_max * 12, 2),
        "porzioni": None,
        "avvertenze": avvertenze
    }

    if dati.porzione:
        superfici_camere = dati.superfici_camere
        tot_camere = sum(superfici_camere)
        if tot_camere > 0:
            magg_riparto_mq = base_max * perc_altre
            can_riparto_min = (base_min + magg_riparto_mq) * superficie_convenzionale
            can_riparto_max = (base_max + magg_riparto_mq) * superficie_convenzionale
            val_mq_min = math.floor(can_riparto_min / tot_camere * 100) / 100.0
            val_mq_max = math.floor(can_riparto_max / tot_camere * 100) / 100.0

            camere = []
            for i in range(len(superfici_camere)):
                cam_min = arrotonda_euro(val_mq_min * superfici_camere[i])
                cam_max = arrotonda_euro(val_mq_max * superfici_camere[i])
                camere.append({
                    "camera": i + 1,
                    "superficie": round(superfici_camere[i], 2),
                    "canone_mensile_min": cam_min,
                    "canone_mensile_max": cam_max
                })

            risultato["porzioni"] = {
                "canone_riparto_mensile_min": round(can_riparto_min, 2),
                "canone_riparto_mensile_max": round(can_riparto_max, 2),
                "totale_superfici_camere": round(tot_camere, 2),
                "valore_mq_mese_min": val_mq_min,
                "valore_mq_mese_max": val_mq_max,
                "camere": camere
            }
            risultato["avvertenze"].append(
                "La somma dei canoni delle porzioni effettivamente locate non puo' in ogni caso "
                "superare il canone dell'intero appartamento (art. 12 c.2); le camere riservate al "
                "locatore o non locate sono conteggiate nel riparto e poi scorporate (art. 12 c.3). "
                "E' ammesso locare le singole camere con tipologie contrattuali diverse (art. 12 "
                "c.4): in tal caso ripetere il calcolo selezionando il tipo di contratto "
                "corrispondente. Per le porzioni autonome dotate di ingresso esclusivo e prive di "
                "parti comuni (art. 12 c.6) il canone si calcola direttamente sulla sola parte "
                "locata con i criteri ordinari."
            )
        else:
            risultato["avvertenze"].append(
                "Inserire le superfici delle camere per calcolare il canone delle singole porzioni."
            )

    return risultato
