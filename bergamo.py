

from typing import Literal, Optional
from pydantic import BaseModel, Field

AREE = {
    "AREA 1 (arancione)": "Papa Giovanni, Stazione, Quarenghi (in parte), Scotti, Tasso, Ghislandi",
    "AREA 2 (verde)": "Citta' Alta e colli, XXIV Maggio, Vittorio Emanuele, Verdi, Pignolo (interamente)",
    "AREA 3 (rosa)": "Stadio, Baioni-Valtesse, Monterosso, parte di Corridoni e S. Caterina",
    "AREA 4 (giallo)": "Longuelo, Loreto, Broseta (in parte), S. Bernardino, Moroni, S. Giovanni Bosco, "
                       "Promessi Sposi, Borgo Palazzo (in parte), Redona",
    "AREA 5 (azzurro)": "Sud della citta' limitrofa a Treviolo, Lallio, Azzano S. Paolo, Orio al Serio"
}

FASCE = {
    "AREA 1 (arancione)": {1: (48.00, 68.00), 2: (68.01, 110.00), 3: (110.01, 135.00)},
    "AREA 2 (verde)":     {1: (48.00, 68.00), 2: (68.01, 120.00), 3: (120.01, 150.00)},
    "AREA 3 (rosa)":      {1: (43.00, 60.00), 2: (60.01, 100.00), 3: (100.01, 120.00)},
    "AREA 4 (giallo)":    {1: (43.00, 60.00), 2: (60.01, 90.00),  3: (90.01, 115.00)},
    "AREA 5 (azzurro)":   {1: (37.00, 52.00), 2: (52.01, 85.00),  3: (85.01, 105.00)}
}

DOTAZIONI = [
    "Autorimessa singola o posto auto coperto o scoperto",                                 # 0
    "Cortile comune",                                                                      # 1
    "Cantina o sottotetto o soffitta",                                                     # 2
    "Impianto di acqua corrente, allacciamento gas ed impianti elettrici efficienti",      # 3
    "Impianto di riscaldamento autonomo o centralizzato",                                  # 4
    "Impianto di riscaldamento autonomo con termoregolazione o di condizionamento",        # 5
    "Ascensore (fabbricato con almeno 3 piani f.t., per unita' oltre il 3 livello)",       # 6
    "Area verde di pertinenza o condominiale, oppure aree attrezzate",                     # 7
    "Impianti o strutture per accesso ai disabili",                                        # 8
    "Ulteriore posto auto o box",                                                          # 9
    "Impianti sportivi di pertinenza dell'immobile",                                       # 10
    "Dotazione di mobilio",                                                                # 11
    "Bagno completo",                                                                      # 12
    "Doppi servizi",                                                                       # 13
    "Porta blindata",                                                                      # 14
    "Doppi vetri",                                                                         # 15
    "Servizio di portineria o impianto di videocitofono",                                  # 16
    "Balconi e/o terrazze di almeno 8 mq",                                                 # 17
    "Unita' ultimata o completamente ristrutturata negli ultimi 10 anni",                  # 18
    "Antenna centralizzata o altro idoneo impianto di rice-trasmissione",                  # 19
    "Vicinanza ai servizi essenziali"                                                      # 20
]


OBBLIGATORI_SF2 = [2, 3, 6, 12]        

ETICHETTE_SUPERFICIE = {
    "sup_a": "a - Locali abitativi, intera superficie (100%) - incl. taverne, mansarde e sottotetti "
             "abitabili comunicanti, esclusi i muri perimetrali esterni e in comune",
    "sup_b": "b - Box e autorimesse / locali per rimesse di veicoli (conteggiati al 70%)",
    "sup_c": "c - Posti auto coperti o scoperti (conteggiati al 50%)",
    "sup_d": "d - Soffitte, cantine e simili (compresi taverne e mansarde soppalchi sprovvisti di "
             "abitabilita') COMUNICANTI con i locali abitativi (conteggiati al 50%)",
    "sup_d_bis": "d bis - Soffitte, cantine e simili NON comunicanti con i locali abitativi "
                 "(conteggiati al 25%)",
    "sup_e": "e - Balconi, terrazze e simili di pertinenza esclusiva COMUNICANTI (30% fino a mq 25, "
             "10% sulla quota eccedente)",
    "sup_e_bis": "e bis - Balconi, terrazze e simili di pertinenza esclusiva NON comunicanti "
                 "(15% fino a mq 25, 5% sulla quota eccedente)",
    "sup_f": "f - Area scoperta di pertinenza esclusiva (10% fino alla superficie dei locali abitativi "
             "di cui al punto a, 2% sulle superfici eccedenti)"
}

OPZIONI_ARREDAMENTO = [
    "Non arredato",
    "Parzialmente arredato",
    "Completamente arredato (+15%)"
]

OPZIONI_CONTRATTO = [
    "A - Uso abitativo ordinario, durata 3 anni",
    "A - Uso abitativo ordinario, durata 4 anni",
    "A - Uso abitativo ordinario, durata 5 anni",
    "A - Uso abitativo ordinario, durata 6 anni e oltre",
    "B - Transitorio ad uso abitativo, max 18 mesi (+5%)",
    "C - Studenti universitari fuori sede, 6 mesi - 3 anni (+5%)",
    "D - Alloggio sociale (D.M. 22/04/2008)"
]

CLASSI_ENERGETICHE = ["A4", "A3", "A2", "A1", "B", "C", "D", "E", "F", "G"]


# MODELLO DI INPUT


class InputBergamo(BaseModel):
    
    area: Literal[
        "AREA 1 (arancione)",
        "AREA 2 (verde)",
        "AREA 3 (rosa)",
        "AREA 4 (giallo)",
        "AREA 5 (azzurro)"
    ] = "AREA 1 (arancione)"

    sup_a: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_a"])
    sup_b: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_b"])
    sup_c: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_c"])
    sup_d: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_d"])
    sup_d_bis: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_d_bis"])
    sup_e: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_e"])
    sup_e_bis: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_e_bis"])
    sup_f: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_f"])

    dotazioni: list[bool] = Field(
        default_factory=lambda: [False] * len(DOTAZIONI),
        min_length=len(DOTAZIONI),
        max_length=len(DOTAZIONI),
        description="21 caselle true/false, nello stesso ordine della lista DOTAZIONI "
                    "(vedi GET /citta/bergamo/info)"
    )

    piano_entro_secondo: bool = Field(
        False,
        description="Unita' posta ad un piano entro il secondo (escluso piano terra e rialzato): "
                    "l'ascensore non viene conteggiato"
    )
    restaurata_borghi: bool = Field(
        False,
        description="Unita' restaurata in borgo storico, Citta' Alta o Parco dei Colli "
                    "(o ricondotta a condizioni simili)"
    )

    # maggiorazioni
    arredamento: Literal[
        "Non arredato",
        "Parzialmente arredato",
        "Completamente arredato (+15%)"
    ] = "Non arredato"

    # usato solo se arredamento = "Parzialmente arredato" (era uno slider 0-14, default 7)
    perc_arredo_parziale: int = Field(
        7, ge=0, le=14,
        description="Percentuale di maggiorazione per arredo parziale (deve essere inferiore al 15%). "
                    "Considerata solo se arredamento = 'Parzialmente arredato'."
    )

    tipo_contratto: Literal[
        "A - Uso abitativo ordinario, durata 3 anni",
        "A - Uso abitativo ordinario, durata 4 anni",
        "A - Uso abitativo ordinario, durata 5 anni",
        "A - Uso abitativo ordinario, durata 6 anni e oltre",
        "B - Transitorio ad uso abitativo, max 18 mesi (+5%)",
        "C - Studenti universitari fuori sede, 6 mesi - 3 anni (+5%)",
        "D - Alloggio sociale (D.M. 22/04/2008)"
    ] = "A - Uso abitativo ordinario, durata 3 anni"

    classe_energetica: Literal["A4", "A3", "A2", "A1", "B", "C", "D", "E", "F", "G"] = "A4"

    locatore_pubblico: bool = Field(
        False,
        description="Locatore Comune o Ente pubblico (anche partecipato o fondazione a prevalenza "
                    "pubblica) (-30% sulle fasce, con limite minimo invalicabile = minimo sub-fascia 1)"
    )


# INFO PER IL FRONTEND (etichette, opzioni, note dell'accordo)


INFO = {
    "id": "bergamo",
    "nome": "Bergamo",
    "titolo": "Calcolatore Canone Concordato - Comune di Bergamo",
    "accordo": "Accordo Territoriale per il Comune di Bergamo sottoscritto il 06/11/2025, "
               "con validita' dal 01/02/2026 (art. 2, comma 3, L. 431/98 e D.M. 16/01/2017)",
    "unita_fasce": "euro/mq annui",
    "aree": AREE,
    "nota_aree": "Deroghe: via Pignolo e via T. Tasso sono assegnate interamente all'AREA 2.",
    "etichette_superficie": ETICHETTE_SUPERFICIE,
    "dotazioni": DOTAZIONI,
    "casi_particolari": {
        "piano_entro_secondo": "Unita' posta ad un piano entro il secondo (escluso piano terra e "
                               "rialzato): l'ascensore non viene conteggiato. La sub-fascia 3 richiede "
                               "10 elementi (6 obbligatori) e la sub-fascia 2 richiede 6 elementi "
                               "(4 obbligatori).",
        "restaurata_borghi": "Unita' restaurata in borgo storico, Citta' Alta o Parco dei Colli: gli "
                             "elementi indispensabili autorimessa/posto auto, ascensore e verde possono "
                             "essere sostituiti da altrettanti elementi opzionali."
    },
    "opzioni": {
        "arredamento": OPZIONI_ARREDAMENTO,
        "tipo_contratto": OPZIONI_CONTRATTO,
        "classe_energetica": CLASSI_ENERGETICHE
    },
    "note": [
        "L'individuazione della sub-fascia e' indicativa: la collocazione definitiva e il canone vanno "
        "verificati con le Organizzazioni firmatarie tramite l'attestazione di rispondenza, in "
        "particolare in prossimita' del valore massimo di fascia.",
        "Le maggiorazioni per durata, arredo e superficie ridotta sono cumulabili e si applicano al "
        "canone base in maniera progressiva: ogni aumento percentuale si applica sul canone gia' "
        "aumentato dal precedente.",
        "Per l'arredo parziale la maggiorazione deve essere inferiore al 15% e proporzionale all'arredo "
        "presente; e' comunque indispensabile una cucina o angolo cottura totalmente attrezzata di "
        "elettrodomestici e mobili.",
        "Per le sub-fasce 2 e 3, gli immobili in classe E, F o G non possono utilizzare il valore "
        "massimo di fascia: il canone massimo e' ridotto del 4% (riduzione applicata prima delle "
        "maggiorazioni)."
    ]
}


# CALCOLO 


def calcola(dati: InputBergamo) -> dict:
    
    if dati.sup_e <= 25:
        quota_e = dati.sup_e * 0.30
    else:
        quota_e = 25 * 0.30 + (dati.sup_e - 25) * 0.10

    if dati.sup_e_bis <= 25:
        quota_e_bis = dati.sup_e_bis * 0.15
    else:
        quota_e_bis = 25 * 0.15 + (dati.sup_e_bis - 25) * 0.05

    if dati.sup_f <= dati.sup_a:
        quota_f = dati.sup_f * 0.10
    else:
        quota_f = dati.sup_a * 0.10 + (dati.sup_f - dati.sup_a) * 0.02

    superficie_computabile = (dati.sup_a + dati.sup_b * 0.70 + dati.sup_c * 0.50 + dati.sup_d * 0.50 +
                              dati.sup_d_bis * 0.25 + quota_e + quota_e_bis + quota_f)

    

    valori_dotazioni = dati.dotazioni

    
    riscaldamento = valori_dotazioni[4] or valori_dotazioni[5]
    n_totale = sum(valori_dotazioni)

    
    obl_sf3 = list(OBBLIGATORI_SF3)
    obl_sf2 = list(OBBLIGATORI_SF2)

    if dati.piano_entro_secondo:
        if valori_dotazioni[6]:
            n_totale -= 1                       
        if 6 in obl_sf3:
            obl_sf3.remove(6)
        if 6 in obl_sf2:
            obl_sf2.remove(6)
        req_sf3_totale, req_sf2_totale = 10, 6
    else:
        req_sf3_totale, req_sf2_totale = 11, 7

    if dati.restaurata_borghi:
        for i in (0, 6, 7):                     
            if i in obl_sf3:
                obl_sf3.remove(i)
        if 6 in obl_sf2:
            obl_sf2.remove(6)

    
    tutti_obbligatori_sf3 = riscaldamento and all(valori_dotazioni[i] for i in obl_sf3)
    tutti_obbligatori_sf2 = riscaldamento and all(valori_dotazioni[i] for i in obl_sf2)

    
    if tutti_obbligatori_sf3 and n_totale >= req_sf3_totale:
        sub_fascia = 3
    elif tutti_obbligatori_sf2 and n_totale >= req_sf2_totale:
        sub_fascia = 2
    else:
        sub_fascia = 1

    #CALCOLO DEL CANONE 

    can_min, can_max = FASCE[dati.area][sub_fascia]

    if dati.classe_energetica in ["E", "F", "G"] and sub_fascia in [2, 3]:
        can_max = can_max * 0.96

    if dati.locatore_pubblico:
        min_sf1_area = FASCE[dati.area][1][0]
        can_min = max(can_min * 0.70, min_sf1_area)
        can_max = can_max * 0.70

    moltiplicatori = []

    if 0 < dati.sup_a < 52:
        moltiplicatori.append(1.20)
    elif 52 <= dati.sup_a <= 64:
        moltiplicatori.append(1.10)

    if dati.arredamento == "Completamente arredato (+15%)":
        moltiplicatori.append(1.15)
    elif dati.arredamento == "Parzialmente arredato" and dati.perc_arredo_parziale > 0:
        moltiplicatori.append(1 + dati.perc_arredo_parziale / 100)

    
    piccolo_64 = 0 < dati.sup_a < 64
    if dati.tipo_contratto == "A - Uso abitativo ordinario, durata 4 anni":
        moltiplicatori.append(1.05 if piccolo_64 else 1.04)
    elif dati.tipo_contratto == "A - Uso abitativo ordinario, durata 5 anni":
        moltiplicatori.append(1.08 if piccolo_64 else 1.06)
    elif dati.tipo_contratto == "A - Uso abitativo ordinario, durata 6 anni e oltre":
        moltiplicatori.append(1.10 if piccolo_64 else 1.08)
    elif dati.tipo_contratto == "B - Transitorio ad uso abitativo, max 18 mesi (+5%)":
        moltiplicatori.append(1.05)
    elif dati.tipo_contratto == "C - Studenti universitari fuori sede, 6 mesi - 3 anni (+5%)":
        moltiplicatori.append(1.05)
    

    for moltiplicatore in moltiplicatori:
        can_min *= moltiplicatore
        can_max *= moltiplicatore

    
    can_annuo_min = round(can_min * superficie_computabile, 2)
    can_annuo_max = round(can_max * superficie_computabile, 2)
    can_mensile_min = round(can_annuo_min / 12, 2)
    can_mensile_max = round(can_annuo_max / 12, 2)

    return {
        "citta": "Bergamo",
        "superficie_computabile": round(superficie_computabile, 2),
        "superficie_tolleranza_min": round(superficie_computabile * 0.93, 2),
        "superficie_tolleranza_max": round(superficie_computabile * 1.07, 2),
        "sub_fascia": sub_fascia,
        "canone_mq_annuo_min": round(can_min, 2),
        "canone_mq_annuo_max": round(can_max, 2),
        "canone_annuo_min": can_annuo_min,
        "canone_annuo_max": can_annuo_max,
        "canone_mensile_min": can_mensile_min,
        "canone_mensile_max": can_mensile_max,
        "avvertenze": [
            "L'individuazione della sub-fascia e' indicativa: la collocazione definitiva e il canone "
            "vanno verificati con le Organizzazioni firmatarie tramite l'attestazione di rispondenza."
        ]
    }

