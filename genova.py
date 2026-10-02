

from typing import Literal
from pydantic import BaseModel, Field
from fastapi import HTTPException



# valori ANNUI in euro al mq (minimo, massimo) per zona: i codici sono quelli della
# zonizzazione del Geoportale del Comune di Genova (nessuno stradario via -> zona)

valori_zone = {
    "B01": (34.56, 143.61), "B02": (34.56, 143.61), "B03": (26.78, 101.94),
    "B04": (35.19, 146.22), "B05": (26.78, 101.94), "B06": (30.98, 124.07),
    "C01": (43.95, 100.07), "C02": (37.20, 117.15), "C03": (37.31, 105.90),
    "C04": (37.20, 121.36), "C05": (34.46, 131.76), "C05A": (40.63, 162.21),
    "C06": (42.15, 168.65), "C09": (37.20, 105.90), "C11": (32.74, 133.08),
    "C12": (32.74, 133.08), "C13": (30.87, 100.62), "C13A": (36.80, 136.83),
    "C14": (43.88, 100.07), "C15": (37.90, 92.77), "C16": (37.90, 92.77),
    "C17": (37.90, 92.77), "C18": (36.01, 92.77), "C19": (37.82, 98.39),
    "C20": (37.20, 98.97), "C20A": (36.69, 117.15), "C21": (36.01, 92.77),
    "C22": (39.62, 103.99), "C23": (36.01, 92.77), "C24": (39.62, 103.99),
    "D01": (41.20, 97.95), "D02": (33.29, 82.75), "D03": (37.00, 93.45),
    "D04": (37.00, 93.45), "D05": (37.00, 93.45), "D06": (37.00, 93.45),
    "D07": (37.00, 93.45), "D08": (37.00, 93.45), "D09": (37.00, 83.17),
    "D10": (37.00, 83.17), "D11": (37.00, 83.17), "D12": (37.00, 93.45),
    "D13": (37.20, 116.68), "D14": (37.31, 97.95), "D15": (41.20, 97.95),
    "D16": (37.20, 116.68), "D17": (37.20, 116.68), "D18": (34.46, 131.76),
    "D20": (34.46, 162.21), "D21": (34.46, 137.02), "D22": (42.16, 176.44),
    "D23": (36.01, 92.77), "D24": (42.16, 176.44), "D25": (37.90, 88.25),
    "D26": (37.90, 88.25), "D27": (36.00, 75.71), "D28": (37.90, 88.25),
    "D29": (37.90, 88.25), "D30": (36.00, 75.71), "D31": (37.90, 88.25),
    "D32": (37.90, 88.25), "D33": (41.20, 91.64), "D34": (41.20, 91.64),
    "D35": (41.20, 91.64), "D36": (41.20, 91.64), "D37": (41.20, 91.64),
    "D38": (41.20, 91.64), "D39": (41.20, 91.64), "D40": (39.14, 109.61),
    "D41": (39.14, 89.06), "D41A": (39.14, 109.61), "D42": (39.14, 109.61),
    "D43": (39.14, 99.54), "D44": (31.32, 85.20), "D45": (39.14, 95.60),
    "D46": (31.32, 85.20), "D47": (36.41, 89.28), "D48": (37.90, 88.35),
    "D49": (39.14, 95.60), "E1": (37.90, 88.25), "R1": (33.29, 82.75),
    "R2": (31.32, 92.23), "R3": (39.00, 82.49), "R5": (34.95, 79.33),
    "R6": (39.00, 82.49)
}

zone_da_verificare = ["D41", "D41A", "D47", "D48", "D49"]


LISTA_ZONE = list(valori_zone.keys())

NOTA_ZONA_DA_VERIFICARE = ("Il valore massimo di questa zona e' parzialmente coperto da un timbro "
                           "nella scansione dell'Allegato 2: da verificare sull'originale.")

ELEMENTI = [
    "1. Impianto di ascensore",
    "2. Impianto di riscaldamento centralizzato, autonomo, a piastre radianti o a pompa "
    "di calore (obbligatorio per le sottofasce superiori alla prima)",
    "3. Impianto di raffrescamento",
    "4. Servizio igienico con doccia o vasca da bagno (obbligatorio per le sottofasce "
    "superiori alla prima)",
    "5. Balcone con profondita' minima di 0,80 m, oppure terrazzo o giardino "
    "pertinenziale di superficie almeno pari a 10 mq",
    "6. Doppi servizi igienici",
    "7. Doppi vetri ad almeno il 90% delle finestre e/o porta blindata",
    "8. Cantina e/o soffitta",
    "9. Servizio di portineria",
    "10. Area verde di uso comune di superficie almeno pari al triplo della superficie "
    "coperta dell'immobile, oppure impianto sportivo",
    "11. Strutture o interventi atti al superamento delle barriere architettoniche nel "
    "condominio",
    "12. Spazio scoperto condominiale per posteggio di uso comune, in numero pari ad "
    "almeno il 50% delle unita' immobiliari del condominio",
    "13. Box pertinenziale e/o posto auto esclusivo",
    "14. Classe energetica da certificazione APE da A sino a D comprese",
    "15. Edificio ultimato da non oltre 10 anni",
    "16. Edificio oggetto di integrale ristrutturazione (L. 457/78, art. 31 lett. c), "
    "ultimato da non oltre 10 anni",
    "17. Intervento di manutenzione straordinaria del fabbricato (L. 457/78, art. 31 "
    "lett. b), ultimato da non oltre 10 anni",
    "18. Ristrutturazione interna (L. 457/78, art. 31 lett. b) o rifacimento integrale "
    "di bagno e cucina, esclusi gli impianti, ultimati da non oltre 10 anni",
    "19. Esposizione a levante/mezzogiorno o mezzogiorno/ponente di almeno la meta' dei "
    "vani, esclusi i servizi e i cavedi",
    "20. Vista mare da almeno due finestre",
    "21. Distanza dal mare inferiore a 300 m"
]

NOTA_ASCENSORE = ("1. Impianto di ascensore: caratteristica considerata presente per gli alloggi "
                  "ubicati non oltre il primo piano")

ETICHETTE_SUPERFICIE = {
    "mq_catastale": "Superficie catastale da visura - mq",
    "mq_principali": "Vani principali e vani accessori a servizio diretto: bagni, ripostigli, "
                     "ingressi, corridoi e simili - mq (calcolati al 100%)",
    "da_ape": "La superficie deriva dall'Attestato di Prestazione Energetica e va maggiorata del 20%",
    "mq_cantine": "Vani accessori a servizio indiretto: soffitte, cantine e simili - mq",
    "cantine_comunicanti": "Le cantine e le soffitte sono comunicanti con i vani principali (50% "
                           "invece del 25%)",
    "mq_balconi": "Balconi, terrazze e simili di pertinenza esclusiva - mq",
    "balconi_comunicanti": "I balconi e le terrazze sono comunicanti con i vani principali (30% e "
                           "10% invece del 15% e 5%)",
    "mq_scoperta": "Area scoperta o assimilabile di pertinenza esclusiva, compreso il posto auto "
                   "scoperto - mq",
    "mq_autorimessa": "Box o autorimessa di pertinenza esclusiva - mq (calcolati al 50%)"
}

ETICHETTE_PORZIONE = {
    "porzione": "Viene locata solo una porzione dell'immobile",
    "mq_porzione": "Mq della porzione locata",
    "mq_parti_comuni": "Mq della quota di parti, accessori e servizi condivisi"
}

DESCRIZIONE_VANI_PRINCIPALI = ("Non entrano nel computo i locali con altezza utile inferiore a 1,50 m. "
                               "Le scale e le rampe interne si computano in misura pari alla loro "
                               "proiezione orizzontale.") #messaggio info

DESCRIZIONE_ARREDO = ("Per completamente arredato si intende l'alloggio fornito in tutti i vani di "
                      "mobilio efficiente e funzionante: cucina o angolo cottura con mobili "
                      "contenitori, tavolo, sedie, frigorifero e piano cottura; camere con armadio e "
                      "letti completi di materassi; adeguati apparati di illuminazione in tutti gli "
                      "ambienti; lavabiancheria. Per parzialmente arredato devono risultare arredati "
                      "almeno la cucina o angolo cottura e la meta' dei restanti vani utili.") #messaggio info

DESCRIZIONE_VINCOLO = ("Riguarda gli immobili di cui all'art. 1 comma 2 lettera a) della L. 431/98, "
                       "soggetti ai vincoli della L. 1089/1939 o inclusi nelle categorie catastali "
                       "A/1, A/8 e A/9. Queste maggiorazioni si sommano a quelle per maggior durata e "
                       "arredo.") #messaggio info

OPZIONI_CONTRATTO = [
    "Contratto agevolato 3 + 2",
    "Contratto transitorio ordinario",
    "Contratto transitorio per studenti universitari"
]

OPZIONI_METODO = [
    "Superficie catastale risultante dalla visura aggiornata",
    "Calcolo secondo i criteri dell'Allegato 3"
]

OPZIONI_ARREDO = [
    "Non arredato",
    "Parzialmente arredato (+6%)",
    "Completamente arredato (+12%)"
]

OPZIONI_DURATA = [
    "Tre anni piu' due",
    "Quattro anni piu' due (+2%)",
    "Cinque anni piu' due (+4%)",
    "Sei anni piu' due (+6%)"
]

OPZIONI_VINCOLO = [
    "Nessun vincolo",
    "Il vincolo riguarda solo il fabbricato (+15%)",
    "Il vincolo riguarda specificamente l'appartamento locato (+30%)"
]

NOTA_PORZIONE = ("In caso di locazione di porzione di immobile gli incrementi di superficie non si "
                 "applicano. La somma dei canoni delle diverse porzioni non puo' superare il canone "
                 "calcolato per l'intero immobile.")

NOTA_DURATA = ("La maggiorazione per la durata non si applica: il punto 4 e' escluso per i contratti "
               "transitori ordinari e per quelli per studenti universitari.")

NOTA_MINIMO_ASSOLUTO = ("Il canone non puo' eccedere il valore massimo della sottofascia, mentre e' "
                        "consentito concordare un valore inferiore al minimo della sottofascia "
                        "purche' non inferiore al limite minimo assoluto della zona.")



# MODELLO DI INPUT


class InputGenova(BaseModel):
    tipo_contratto: Literal[
        "Contratto agevolato 3 + 2",
        "Contratto transitorio ordinario",
        "Contratto transitorio per studenti universitari"
    ] = "Contratto agevolato 3 + 2"

    zona: str = Field(
        ...,
        description="Codice della zona (zonizzazione del Geoportale del Comune di Genova), scritto "
                    "come nell'elenco lista_zone di GET /citta/genova/info (esempio: 'C05A')"
    )

    piano: int = Field(1, ge=0, le=40, description="Piano dell'appartamento (0 per il piano terra)")

    # superficie
    metodo: Literal[
        "Superficie catastale risultante dalla visura aggiornata",
        "Calcolo secondo i criteri dell'Allegato 3"
    ] = Field("Superficie catastale risultante dalla visura aggiornata",
              description="Come viene determinata la superficie")

    mq_catastale: float = Field(
        0.0, ge=0,
        description=ETICHETTE_SUPERFICIE["mq_catastale"] + ". Considerato solo con il metodo "
                    "'Superficie catastale risultante dalla visura aggiornata'."
    )

    # campi considerati solo con il metodo "Calcolo secondo i criteri dell'Allegato 3"
    mq_principali: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_principali"] + ". " +
                                                        DESCRIZIONE_VANI_PRINCIPALI)
    da_ape: bool = Field(False, description=ETICHETTE_SUPERFICIE["da_ape"])
    mq_cantine: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_cantine"])
    cantine_comunicanti: bool = Field(False, description=ETICHETTE_SUPERFICIE["cantine_comunicanti"])
    mq_balconi: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_balconi"])
    balconi_comunicanti: bool = Field(False, description=ETICHETTE_SUPERFICIE["balconi_comunicanti"])
    mq_scoperta: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_scoperta"])
    mq_autorimessa: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_autorimessa"])

    # locazione di porzione di immobile
    porzione: bool = Field(False, description=ETICHETTE_PORZIONE["porzione"])
    mq_porzione: float = Field(0.0, ge=0, description=ETICHETTE_PORZIONE["mq_porzione"] +
                                                      ". Considerato solo se porzione = true.")
    mq_parti_comuni: float = Field(0.0, ge=0, description=ETICHETTE_PORZIONE["mq_parti_comuni"] +
                                                          ". Considerato solo se porzione = true.")

    elementi: list[bool] = Field(
        default_factory=lambda: [False] * len(ELEMENTI),
        min_length=len(ELEMENTI), max_length=len(ELEMENTI),
        description="21 caselle true/false, nello stesso ordine della lista ELEMENTI (vedi "
                    "GET /citta/genova/info). La prima (ascensore) e' considerata solo oltre il "
                    "primo piano: fino al primo piano l'elemento e' dato per presente."
    )

    # maggiorazioni
    arredo: Literal[
        "Non arredato",
        "Parzialmente arredato (+6%)",
        "Completamente arredato (+12%)"
    ] = Field("Non arredato", description="Arredamento. " + DESCRIZIONE_ARREDO)

    durata: Literal[
        "Tre anni piu' due",
        "Quattro anni piu' due (+2%)",
        "Cinque anni piu' due (+4%)",
        "Sei anni piu' due (+6%)"
    ] = Field("Tre anni piu' due", description="Durata contrattuale. Considerata solo per il "
                                               "contratto agevolato.")

    vincolo: Literal[
        "Nessun vincolo",
        "Il vincolo riguarda solo il fabbricato (+15%)",
        "Il vincolo riguarda specificamente l'appartamento locato (+30%)"
    ] = Field("Nessun vincolo", description="Immobili vincolati. " + DESCRIZIONE_VINCOLO)



# INFO PER IL FRONTEND


INFO = {
    "id": "genova",
    "nome": "Genova",
    "titolo": "Calcolatore canone concordato - Comune di Genova",
    "unita_fasce": "euro/mq annui",
    "valori_zone": valori_zone,
    "lista_zone": LISTA_ZONE,
    "zone_da_verificare": zone_da_verificare,
    "elementi": ELEMENTI,
    "etichette_superficie": ETICHETTE_SUPERFICIE,
    "etichette_porzione": ETICHETTE_PORZIONE,
    "etichette": {
        "vani_principali": DESCRIZIONE_VANI_PRINCIPALI,
        "arredo": DESCRIZIONE_ARREDO,
        "vincolo": DESCRIZIONE_VINCOLO
    },
    "opzioni": {
        "tipo_contratto": OPZIONI_CONTRATTO,
        "metodo": OPZIONI_METODO,
        "arredo": OPZIONI_ARREDO,
        "durata": OPZIONI_DURATA,
        "vincolo": OPZIONI_VINCOLO
    },
    "note": [
        "La zona va indicata con il codice della zonizzazione del Geoportale del Comune di Genova "
        "(B01, C05A, D13, ...): nel modulo non c'e' uno stradario che associ la via al codice.",
        "I valori delle tabelle sono ANNUI in euro al mq: il canone mensile e' il canone annuo "
        "diviso 12.",
        "L'Allegato 2 da' un solo minimo e un solo massimo per zona: le tre sottofasce sono "
        "ricavate dividendo l'intervallo in tre parti uguali.",
        "Sottofasce: da 9 elementi la terza, da 3 a 8 la seconda, fino a 2 la prima. Senza "
        "l'elemento 2 o l'elemento 4 l'alloggio resta in prima sottofascia.",
        NOTA_ASCENSORE,
        "Superficie di calcolo: sotto 45 mq +30% (con il limite di 54 mq); fino a 60 mq +20% (con "
        "il limite di 67 mq); da 61 a 69 mq +10% (con il limite di 70 mq); oltre 100 mq "
        "l'eccedenza e' ridotta del 30%.",
        "Le maggiorazioni sono sommate tra loro. Contratto transitorio ordinario: +10%, con il "
        "limite del 16% complessivo insieme all'arredo.",
        "Zone " + ", ".join(zone_da_verificare) + ": " + NOTA_ZONA_DA_VERIFICARE,
        NOTA_PORZIONE,
        NOTA_DURATA,
        NOTA_MINIMO_ASSOLUTO
    ]
}



# CALCOLO (stessi passaggi, nello stesso ordine, del file Streamlit)


def calcola(dati: InputGenova) -> dict:
    note = []
    avvertenze = []

    tipo_contratto = dati.tipo_contratto
    zona = dati.zona.strip().upper()

    if zona not in valori_zone:
        raise HTTPException(
            status_code=400,
            detail="La zona non e' stata trovata: usare uno dei codici dell'elenco lista_zone di "
                   "GET /citta/genova/info"
        )

    if zona in zone_da_verificare:
        avvertenze.append(NOTA_ZONA_DA_VERIFICARE)

    piano = dati.piano

    # SUPERFICIE

    metodo = dati.metodo

    if metodo.startswith("Superficie catastale"):
        mq_convenzionali = dati.mq_catastale
    else:
        mq_principali = dati.mq_principali
        da_ape = dati.da_ape
        if da_ape == True:
            mq_principali = mq_principali * 1.20

        mq_cantine = dati.mq_cantine
        cantine_comunicanti = dati.cantine_comunicanti
        if cantine_comunicanti == True:
            mq_cantine_conv = mq_cantine * 0.50
        else:
            mq_cantine_conv = mq_cantine * 0.25

        mq_balconi = dati.mq_balconi
        balconi_comunicanti = dati.balconi_comunicanti
        if balconi_comunicanti == True:
            prima_quota = 0.30
            seconda_quota = 0.10
        else:
            prima_quota = 0.15
            seconda_quota = 0.05
        if mq_balconi <= 25.0:
            mq_balconi_conv = mq_balconi * prima_quota
        else:
            mq_balconi_conv = 25.0 * prima_quota + (mq_balconi - 25.0) * seconda_quota

        mq_scoperta = dati.mq_scoperta
        if mq_scoperta <= mq_principali:
            mq_scoperta_conv = mq_scoperta * 0.10
        else:
            mq_scoperta_conv = mq_principali * 0.10 + (mq_scoperta - mq_principali) * 0.02

        mq_autorimessa = dati.mq_autorimessa

        mq_convenzionali = (mq_principali + mq_cantine_conv + mq_balconi_conv
                            + mq_scoperta_conv + mq_autorimessa * 0.50)

    porzione = dati.porzione

    if porzione == True:
        mq_porzione = dati.mq_porzione
        mq_parti_comuni = dati.mq_parti_comuni
        mq_finali = mq_porzione + mq_parti_comuni
        note.append(NOTA_PORZIONE)
    else:
        mq_porzione = 0.0
        mq_finali = mq_convenzionali
        if mq_convenzionali < 45.0:
            mq_finali = mq_convenzionali * 1.30
            if mq_finali > 54.0:
                mq_finali = 54.0
        elif mq_convenzionali <= 60.0:
            mq_finali = mq_convenzionali * 1.20
            if mq_finali > 67.0:
                mq_finali = 67.0
        elif mq_convenzionali >= 61.0 and mq_convenzionali <= 69.0:
            mq_finali = mq_convenzionali * 1.10
            if mq_finali > 70.0:
                mq_finali = 70.0
        elif mq_convenzionali > 100.0:
            mq_finali = 100.0 + (mq_convenzionali - 100.0) * 0.70

    if porzione == False and mq_convenzionali <= 0.0:
        raise HTTPException(
            status_code=400,
            detail="Inserire la superficie dell'immobile per ottenere la stima"
        )
    elif porzione == True and mq_finali <= 0.0:
        raise HTTPException(
            status_code=400,
            detail="Inserire la superficie della porzione locata per ottenere la stima"
        )

    # ELEMENTI CARATTERISTICI

    el1 = True
    if piano > 1:
        el1 = dati.elementi[0]
    else:
        note.append(NOTA_ASCENSORE)

    el2 = dati.elementi[1]  # Impianto di riscaldamento (obbligatorio oltre la prima sottofascia)
    el4 = dati.elementi[3]  # Servizio igienico con doccia o vasca (obbligatorio oltre la prima)

    # la prima casella viene sostituita da el1, le altre venti restano come inviate
    elementi = [el1] + dati.elementi[1:]
    n_elementi = sum(e for e in elementi if e == True)

    if el2 == False or el4 == False:
        sottofascia = 1
    elif n_elementi >= 9:
        sottofascia = 3
    elif n_elementi >= 3:
        sottofascia = 2
    else:
        sottofascia = 1

    if (el2 == False or el4 == False) and n_elementi >= 3:
        note.append("Prima sottofascia: mancano l'elemento 2 e/o l'elemento 4, obbligatori per "
                    "accedere alle sottofasce superiori")

    zona_min, zona_max = valori_zone[zona]
    ampiezza = (zona_max - zona_min) / 3.0

    if sottofascia == 1:
        val_min = zona_min
        val_max = zona_min + ampiezza
    elif sottofascia == 2:
        val_min = zona_min + ampiezza
        val_max = zona_min + ampiezza * 2.0
    else:
        val_min = zona_min + ampiezza * 2.0
        val_max = zona_max

    canone_mq_base_min = val_min
    canone_mq_base_max = val_max

    # MAGGIORAZIONI (sommate)

    perc_totale = 0.0

    arredo = dati.arredo
    perc_arredo = 0.0
    if arredo.startswith("Parzialmente"):
        perc_arredo = 0.06
    elif arredo.startswith("Completamente"):
        perc_arredo = 0.12

    if tipo_contratto.startswith("Contratto transitorio ordinario"):
        perc_base = 0.10 + perc_arredo
        if perc_base > 0.16:
            perc_base = 0.16
            note.append("L'aumento del 10% previsto per i contratti transitori sommato a quello per "
                        "l'arredo e' stato limitato al 16% complessivo.")
        perc_totale = perc_totale + perc_base
    else:
        perc_totale = perc_totale + perc_arredo

    if tipo_contratto.startswith("Contratto agevolato"):
        durata = dati.durata
        if durata.startswith("Quattro"):
            perc_totale = perc_totale + 0.02
        elif durata.startswith("Cinque"):
            perc_totale = perc_totale + 0.04
        elif durata.startswith("Sei"):
            perc_totale = perc_totale + 0.06
    else:
        note.append(NOTA_DURATA)

    vincolo = dati.vincolo
    if vincolo.startswith("Il vincolo riguarda solo"):
        perc_totale = perc_totale + 0.15
    elif vincolo.startswith("Il vincolo riguarda specificamente"):
        perc_totale = perc_totale + 0.30

    # CANONE

    val_min = val_min + val_min * perc_totale
    val_max = val_max + val_max * perc_totale
    minimo_assoluto = zona_min + zona_min * perc_totale

    canone_annuo_min = mq_finali * val_min
    canone_annuo_max = mq_finali * val_max
    canone_minimo_assoluto = mq_finali * minimo_assoluto

    avvertenze.append(NOTA_MINIMO_ASSOLUTO)

    return {
        "citta": "Genova",
        "zona": zona,
        "sottofascia": sottofascia,
        "numero_elementi": n_elementi,
        "superficie_convenzionale": round(mq_convenzionali, 2),
        "superficie_calcolo": round(mq_finali, 2),
        "canone_mq_base_min": round(canone_mq_base_min, 4),
        "canone_mq_base_max": round(canone_mq_base_max, 4),
        "percentuale_maggiorazioni": round(perc_totale * 100, 2),
        "canone_mq_min": round(val_min, 4),
        "canone_mq_max": round(val_max, 4),
        "minimo_assoluto_mq": round(minimo_assoluto, 4),
        "canone_minimo_assoluto_mensile": round(canone_minimo_assoluto / 12.0, 2),
        "canone_mensile_min": round(canone_annuo_min / 12.0, 2),
        "canone_mensile_max": round(canone_annuo_max / 12.0, 2),
        "canone_annuo_min": round(canone_annuo_min, 2),
        "canone_annuo_max": round(canone_annuo_max, 2),
        "note": note,
        "avvertenze": avvertenze
    }
