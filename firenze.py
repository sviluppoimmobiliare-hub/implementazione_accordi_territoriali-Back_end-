

from typing import Literal, Optional
from pydantic import BaseModel, Field
from fastapi import HTTPException

DETTAGLIO_ZONE = {
    "Centro Storico": "CENTRO",
    "Lungarno": "CENTRO",
    "Piazza Ferrucci": "CENTRO",
    "Bobolino": "DI PREGIO",
    "Due Strade": "DI PREGIO",
    "Marignolle": "DI PREGIO",
    "La Pietra": "DI PREGIO",
    "Careggi": "DI PREGIO",
    "Settignano": "DI PREGIO",
    "Poggetto": "INTERMEDIA A",
    "Cure": "INTERMEDIA A",
    "Campo di Marte": "INTERMEDIA A",
    "Madonnone/Bellariva": "INTERMEDIA A",
    "Bandino": "INTERMEDIA A",
    "Nave a Rovezzano": "INTERMEDIA A",
    "Novoli": "INTERMEDIA A",
    "Coverciano": "INTERMEDIA A",
    "Varlungo": "INTERMEDIA A",
    "San Jacopino": "INTERMEDIA B",
    "Dalmazia": "INTERMEDIA B",
    "Cascine del Riccio": "INTERMEDIA B",
    "Galluzzo": "INTERMEDIA B",
    "Legnaia": "PERIFERICA A",
    "Isolotto": "PERIFERICA A",
    "Argingrosso": "PERIFERICA A",
    "Castello": "PERIFERICA A",
    "Piagge": "PERIFERICA B",
    "Peretola": "PERIFERICA B",
    "Mantignano": "PERIFERICA B",
    "Cupolina": "PERIFERICA B"
}

MICROZONE_MAP = {
    "CENTRO": "1-2-3",
    "DI PREGIO": "4-5-6-12-25-30",
    "INTERMEDIA A": "11-13-14-15-16-17-23-26-27",
    "INTERMEDIA B": "9-10-18-19",
    "PERIFERICA A": "7-8-20-24",
    "PERIFERICA B": "21-22-28-29"
}

FASCE = {
    "CENTRO":       {"A": (2.00, 13.00), "B": (2.00, 11.00), "C": (2.00, 7.00)},
    "DI PREGIO":    {"A": (2.00, 13.50), "B": (2.00, 12.00), "C": (2.00, 7.50)},
    "INTERMEDIA A": {"A": (2.00, 10.20), "B": (2.00, 9.00),  "C": (2.00, 5.50)},
    "INTERMEDIA B": {"A": (2.00, 9.70),  "B": (2.00, 8.70),  "C": (2.00, 5.50)},
    "PERIFERICA A": {"A": (2.00, 9.20),  "B": (2.00, 8.30),  "C": (2.00, 5.50)},
    "PERIFERICA B": {"A": (2.00, 8.75),  "B": (2.00, 8.10),  "C": (2.00, 5.00)}
}


CARATTERISTICHE_TIPOLOGIA_B = [
    "a - Riscaldamento completo di elementi radianti e/o sistemi alternativi, efficiente ed a norma",
    "b - Servizio igienico principale con almeno quattro apparecchi, fornito di finestra o areazione forzata",
    "c - Impianto idrico idoneo ed efficiente",
    "d - Impianto elettrico a norma, consentito dalle vigenti norme",
    "e - Ascensore per unità immobiliari poste oltre il terzo piano fuori terra",
    "f - Infissi ed affissi efficienti con chiusura atta a garantire la tenuta agli agenti atmosferici",
    "g - Citofono con apri porta efficiente"
]


INDICI_NON_DETERMINANTI = [4, 6]

ELEMENTI_TIPOLOGIA_A = [
    "1 - Apparecchi di condizionamento d'aria nell'unità immobiliare (non richiesto se immobile vincolato o cat. A/8, A/9)",
    "2 - Rifiniture di particolare pregio",
    "3 - Doppi servizi igienici (secondo servizio con almeno 3 apparecchi se sup. > 80 mq; servizio finestrato se sup. < 80 mq)",
    "4 - Spazi per uso parcheggio con effettiva disponibilità, assegnati catastalmente o da regolamento condominiale",
    "5 - Spazi esterni ad uso esclusivo di metratura pari almeno ad 1/3 della superficie calpestabile",
    "6 - Sistema di allarme e/o sistemi di anti effrazione quali inferriate",
    "7 - Servizio di portierato o impianto di videosorveglianza",
    "8 - Sistema di connessione internet in fibra ottica di tipo FTTH",
    "9 - Portone o portoncino blindato",
    "10 - Ascensore per unità immobiliari poste oltre il secondo piano",
    "11 - Spazi verdi condominiali",
    "12 - Impianto fotovoltaico e/o solare termico"
]

ETICHETTE_SUPERFICIE = {
    "sup_a": "A - Superficie interna utile abitativa calpestabile in mq (escluse mura e aree con altezza inferiore a 240 cm)",
    "sup_a1": "A1 - Superficie delle aree interne con altezza compresa fra 180 e 240 cm (conteggiata al 30%)",
    "sup_b": "B - Superficie utile delle autorimesse singole o box auto (conteggiata al 50%)",
    "sup_c": "C - Superficie dei lastrici solari di uso esclusivo al piano attico (25% fino ai mq calpestabili, 5% sull'eccedenza)",
    "sup_d": "D - Superficie dei posti auto coperti o scoperti in area di proprietà esclusiva del locatore (conteggiata al 30%)",
    "sup_e": "E - Superficie del posto auto in autorimesse comuni coperte, delimitato ed assegnato senza identificativo catastale (conteggiata al 25%)",
    "sup_f": "F - Superficie utile del posto auto in spazi comuni scoperti, delimitato ed assegnato senza identificativo catastale (conteggiata al 20%)",
    "sup_g": "G - Superficie utile del posto auto in spazi comuni scoperti con rotazione turnaria (conteggiata al 5%)",
    "sup_h": "H - Superficie utile di balconi, terrazze, lastrici solari non all'attico, cantine (conteggiata al 25%)",
    "sup_i": "I - Superficie scoperta (corti, giardini ecc.) di pertinenza in godimento esclusivo (10% fino ai mq calpestabili, 2% sull'eccedenza)"
}

OPZIONI_ARREDAMENTO = [
    "Non arredato",
    "Arredato per 1/2 dei vani locati (max +7%)",
    "Arredato per 3/4 dei vani locati (max +10%)",
    "Completamente arredato (max +15%)"
]

TETTI_ARREDO = {
    "Non arredato": 0.0,
    "Arredato per 1/2 dei vani locati (max +7%)": 7.0,
    "Arredato per 3/4 dei vani locati (max +10%)": 10.0,
    "Completamente arredato (max +15%)": 15.0
}

OPZIONI_CLASSE_ENERGETICA = [
    "G / F / Non disponibile",
    "E (+2%)",
    "D (+4%)",
    "C (+6%)",
    "B (+8%)",
    "A1 (+10%)",
    "A2 (+12%)",
    "A3 (+14%)",
    "A4 (+15%)"
]

INCREMENTI_ENERGETICI = {
    "G / F / Non disponibile": 1.00,
    "E (+2%)": 1.02,
    "D (+4%)": 1.04,
    "C (+6%)": 1.06,
    "B (+8%)": 1.08,
    "A1 (+10%)": 1.10,
    "A2 (+12%)": 1.12,
    "A3 (+14%)": 1.14,
    "A4 (+15%)": 1.15
}

OPZIONI_CONTRATTO = [
    "Agevolato 3+2 anni",
    "Agevolato 4 anni +2 (+4,50%)",
    "Agevolato 5 anni +2 (+6%)",
    "Agevolato 6 o più anni (+7,5%)",
    "Transitorio ordinario (1-18 mesi)",
    "Transitorio per studenti universitari (max +15%)"
]

# MODELLO DI INPUT

class InputFirenze(BaseModel):
    
    quartiere: Literal[
        "Centro Storico", "Lungarno", "Piazza Ferrucci",
        "Bobolino", "Due Strade", "Marignolle", "La Pietra", "Careggi", "Settignano",
        "Poggetto", "Cure", "Campo di Marte", "Madonnone/Bellariva", "Bandino",
        "Nave a Rovezzano", "Novoli", "Coverciano", "Varlungo",
        "San Jacopino", "Dalmazia", "Cascine del Riccio", "Galluzzo",
        "Legnaia", "Isolotto", "Argingrosso", "Castello",
        "Piagge", "Peretola", "Mantignano", "Cupolina"
    ] = "Centro Storico"

    
    sup_a: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_a"])
    sup_a1: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_a1"])
    sup_b: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_b"])
    sup_c: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_c"])
    sup_d: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_d"])
    sup_e: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_e"])
    sup_f: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_f"])
    sup_g: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_g"])
    sup_h: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_h"])
    sup_i: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_i"])

    
    applica_incremento_piccole: bool = Field(
        True,
        description="Applicare l'incremento per piccole superfici (Art. 6). Considerato solo se "
                    "la superficie calpestabile A e' compresa tra 0 e 65 mq. "
                    "+20% fino a 63 mq se il calpestabile e' fino a 60 mq, "
                    "+5% fino a 65 mq se il calpestabile e' tra 60 e 65 mq."
    )

    
    caratteristiche_b: list[bool] = Field(
        default_factory=lambda: [False] * len(CARATTERISTICHE_TIPOLOGIA_B),
        min_length=len(CARATTERISTICHE_TIPOLOGIA_B),
        max_length=len(CARATTERISTICHE_TIPOLOGIA_B),
        description="7 caselle true/false, nello stesso ordine della lista "
                    "CARATTERISTICHE_TIPOLOGIA_B (vedi GET /citta/firenze/info)"
    )

    
    nuovo_o_ristrutturato: bool = Field(
        False,
        description="Immobile costruito o oggetto di ristrutturazione e/o risanamento ultimati entro "
                    "gli ultimi 10 anni, con i requisiti dell'Art. 8 lett. a)"
    )

    
    elementi_a: list[bool] = Field(
        default_factory=lambda: [False] * len(ELEMENTI_TIPOLOGIA_A),
        min_length=len(ELEMENTI_TIPOLOGIA_A),
        max_length=len(ELEMENTI_TIPOLOGIA_A),
        description="12 caselle true/false, nello stesso ordine della lista "
                    "ELEMENTI_TIPOLOGIA_A (vedi GET /citta/firenze/info)"
    )

    immobile_vincolato: bool = Field(
        False,
        description="Immobile vincolato o di categoria catastale A/8 o A/9: il condizionamento d'aria "
                    "(elemento 1) non e' richiesto e viene considerato automaticamente presente ai "
                    "fini del conteggio dei 6 elementi (Art. 8, lett. a, punto 1)"
    )

    
    arredamento: Literal[
        "Non arredato",
        "Arredato per 1/2 dei vani locati (max +7%)",
        "Arredato per 3/4 dei vani locati (max +10%)",
        "Completamente arredato (max +15%)"
    ] = "Non arredato"

    
    perc_arredo: Optional[float] = Field(
        None, ge=0, le=15,
        description="Percentuale di maggiorazione per arredo concordata tra le parti. "
                    "Se omessa si usa il tetto massimo dell'opzione di arredo scelta. "
                    "Non puo' superare il tetto dell'opzione (7 / 10 / 15)."
    )

    pregio_431: bool = Field(
        False,
        description="Immobile di particolare pregio ex art. 1, comma 2, lett. a) L. 431/98 "
                    "(+15% sulle fasce): immobili vincolati o di categoria catastale A/1, A/8, A/9 "
                    "(Art. 9, punto 2)"
    )
    categoria_a7: bool = Field(
        False,
        description="Immobile di categoria catastale A/7 (+10% sulle fasce) (Art. 9, punto 2)"
    )

    classe_energetica: Literal[
        "G / F / Non disponibile",
        "E (+2%)",
        "D (+4%)",
        "C (+6%)",
        "B (+8%)",
        "A1 (+10%)",
        "A2 (+12%)",
        "A3 (+14%)",
        "A4 (+15%)"
    ] = "G / F / Non disponibile"

    tipo_contratto: Literal[
        "Agevolato 3+2 anni",
        "Agevolato 4 anni +2 (+4,50%)",
        "Agevolato 5 anni +2 (+6%)",
        "Agevolato 6 o più anni (+7,5%)",
        "Transitorio ordinario (1-18 mesi)",
        "Transitorio per studenti universitari (max +15%)"
    ] = "Agevolato 3+2 anni"

    
    perc_studenti: Optional[float] = Field(
        None, ge=0, le=15,
        description="Percentuale di maggiorazione per contratto studenti concordata tra le parti. "
                    "Se omessa si usa il massimo (15%). Considerata solo per il contratto "
                    "'Transitorio per studenti universitari'."
    )

    
    transitorio_studio: bool = Field(
        False,
        description="Contratto transitorio ordinario sottoscritto con la motivazione di cui "
                    "all'Art. 12, comma 2, lett. a) (motivi di studio, apprendistato, formazione e "
                    "aggiornamento professionale; sussistenza da verificare tramite Attestazione "
                    "Bilaterale obbligatoria). Max +5% nei valori minimi e massimi."
    )
    perc_transitorio_studio: Optional[float] = Field(
        None, ge=0, le=5,
        description="Percentuale di maggiorazione per motivazione di studio concordata tra le parti. "
                    "Se omessa si usa il massimo (5%). Considerata solo se tipo_contratto = "
                    "'Transitorio ordinario (1-18 mesi)' e transitorio_studio = true."
    )


# INFO PER IL FRONTEND 

INFO = {
    "id": "firenze",
    "nome": "Firenze",
    "titolo": "Calcolatore Canone Concordato - Comune di Firenze",
    "accordo": "Accordo Territoriale sulle locazioni abitative sottoscritto il 03/07/2025 "
               "(art. 2, comma 3, L. 431/98 e D.M. 16/01/2017)",
    "unita_fasce": "euro/mq mensili",
    "quartieri": DETTAGLIO_ZONE,         
    "microzone": MICROZONE_MAP,           
    "etichette_superficie": ETICHETTE_SUPERFICIE,
    "caratteristiche_tipologia_b": CARATTERISTICHE_TIPOLOGIA_B,
    "nota_tipologia_c": "Le caratteristiche e) ascensore e g) citofono NON sono determinanti per la "
                        "tipologia C (Art. 8, lett. c).",
    "elementi_tipologia_a": ELEMENTI_TIPOLOGIA_A,
    "nota_tipologia_a": "Almeno 6 elementi aggiuntivi, uniti ai requisiti della Tipologia B, "
                        "classificano l'alloggio in Tipologia A.",
    "aiuto_nuovo_o_ristrutturato": "Interventi che abbiano coinvolto in toto gli impianti elettrico, "
        "idrico e sanitario, con sostituzione degli infissi esterni e APE migliorativo. L'unita' deve "
        "inoltre possedere: riscaldamento efficiente a norma con caldaia di vetusta' non superiore a "
        "10 anni, servizio igienico principale con almeno 4 apparecchi finestrato o con areazione "
        "forzata, impianto idrico idoneo, impianto elettrico post L. 46/90 certificato, ascensore "
        "oltre il 2 piano, ambienti a norma, infissi efficienti, citofono con apri porta, "
        "condizionamento diffuso in tutti i locali, rifiniture di buona fattura, doppi servizi se "
        "superficie >= 80 mq",
    "opzioni": {
        "arredamento": OPZIONI_ARREDAMENTO,
        "tetti_arredo": TETTI_ARREDO,
        "classe_energetica": OPZIONI_CLASSE_ENERGETICA,
        "tipo_contratto": OPZIONI_CONTRATTO
    },
    "note": [
        "L'arredo deve essere funzionale ed efficiente; per la maggiorazione massima e' indispensabile "
        "arredo idoneo per ogni vano utile locato. Le percentuali sono tetti massimi entro cui le "
        "parti concordano l'incremento effettivo (Art. 9, punto 1).",
        "L'incremento per piccole superfici (Art. 6) e' una facolta' delle parti: +20% fino a 63 mq "
        "se il calpestabile e' fino a 60 mq, +5% fino a 65 mq se il calpestabile e' tra 60 e 65 mq.",
        "Le maggiorazioni si applicano in maniera progressiva (Art. 10)."
    ]
}



# CALCOLO 

def calcola(dati: InputFirenze) -> dict:
    
    zona = DETTAGLIO_ZONE[dati.quartiere]

    
    if dati.sup_c <= dati.sup_a:
        quota_c = dati.sup_c * 0.25
    else:
        quota_c = dati.sup_a * 0.25 + (dati.sup_c - dati.sup_a) * 0.05

    
    if dati.sup_i <= dati.sup_a:
        quota_i = dati.sup_i * 0.10
    else:
        quota_i = dati.sup_a * 0.10 + (dati.sup_i - dati.sup_a) * 0.02

    superficie_convenzionale = (dati.sup_a + dati.sup_a1 * 0.30 + dati.sup_b * 0.50 + quota_c +
                                dati.sup_d * 0.30 + dati.sup_e * 0.25 + dati.sup_f * 0.20 +
                                dati.sup_g * 0.05 + dati.sup_h * 0.25 + quota_i)

    
    applica_incremento_piccole = False
    if 0 < dati.sup_a <= 65:
        applica_incremento_piccole = dati.applica_incremento_piccole

    if applica_incremento_piccole:
        if 0 < dati.sup_a <= 60:
            superficie_convenzionale = max(superficie_convenzionale,
                                           min(superficie_convenzionale * 1.20, 63.00))
        elif 60 < dati.sup_a <= 65:
            superficie_convenzionale = max(superficie_convenzionale,
                                           min(superficie_convenzionale * 1.05, 65.00))

    

    counter_b = sum(dati.caratteristiche_b)

    counter_a = sum(dati.elementi_a)

    
    if dati.immobile_vincolato and not dati.elementi_a[0]:
        counter_a += 1

    
    mancanti_determinanti = 0
    for i in range(len(CARATTERISTICHE_TIPOLOGIA_B)):
        if i not in INDICI_NON_DETERMINANTI and not dati.caratteristiche_b[i]:
            mancanti_determinanti += 1

    if counter_b >= 6:
        tipologia_base = "B"
    elif mancanti_determinanti < 2:
        tipologia_base = "B"
    else:
        tipologia_base = "C"

    tipologia = tipologia_base
    if dati.nuovo_o_ristrutturato:
        tipologia = "A"
    elif tipologia_base == "B" and counter_a >= 6:
        tipologia = "A"

    
    tetto_arredo = TETTI_ARREDO[dati.arredamento]
    if dati.perc_arredo is None:
        perc_arredo = tetto_arredo
    else:
        perc_arredo = dati.perc_arredo
    if perc_arredo > tetto_arredo:
        raise HTTPException(
            status_code=400,
            detail=f"La percentuale di arredo ({perc_arredo}%) supera il tetto massimo "
                   f"({tetto_arredo}%) previsto per l'opzione '{dati.arredamento}'"
        )

    
    perc_studenti = 0.0
    if dati.tipo_contratto == "Transitorio per studenti universitari (max +15%)":
        if dati.perc_studenti is None:
            perc_studenti = 15.0
        else:
            perc_studenti = dati.perc_studenti

    
    perc_transitorio_studio = 0.0
    if dati.tipo_contratto == "Transitorio ordinario (1-18 mesi)" and dati.transitorio_studio:
        if dati.perc_transitorio_studio is None:
            perc_transitorio_studio = 5.0
        else:
            perc_transitorio_studio = dati.perc_transitorio_studio

    #CALCOLO DEL CANONE

    if dati.pregio_431 and dati.categoria_a7:
        
        raise HTTPException(
            status_code=400,
            detail="L'immobile non può essere di particolare pregio ex L. 431/98 e di categoria A/7 "
                   "allo stesso tempo"
        )

    can_min, can_max = FASCE[zona][tipologia]

    moltiplicatori = []

    if dati.pregio_431:
        moltiplicatori.append(1.15)
    elif dati.categoria_a7:
        moltiplicatori.append(1.10)

    if perc_arredo > 0:
        moltiplicatori.append(1 + perc_arredo / 100)

    moltiplicatori.append(INCREMENTI_ENERGETICI[dati.classe_energetica])

    if dati.tipo_contratto == "Agevolato 4 anni +2 (+4,50%)":
        moltiplicatori.append(1.045)
    elif dati.tipo_contratto == "Agevolato 5 anni +2 (+6%)":
        moltiplicatori.append(1.06)
    elif dati.tipo_contratto == "Agevolato 6 o più anni (+7,5%)":
        moltiplicatori.append(1.075)

    if perc_studenti > 0:
        moltiplicatori.append(1 + perc_studenti / 100)
    if perc_transitorio_studio > 0:
        moltiplicatori.append(1 + perc_transitorio_studio / 100)

   
    for moltiplicatore in moltiplicatori:
        can_min *= moltiplicatore
        can_max *= moltiplicatore

    
    can_mensile_min = round(can_min * superficie_convenzionale, 2)
    can_mensile_max = round(can_max * superficie_convenzionale, 2)

    return {
        "citta": "Firenze",
        "quartiere": dati.quartiere,
        "zona": zona,
        "microzone": MICROZONE_MAP[zona],
        "superficie_convenzionale": round(superficie_convenzionale, 2),
        "tipologia": tipologia,
        "canone_mq_mensile_min": round(can_min, 2),
        "canone_mq_mensile_max": round(can_max, 2),
        "canone_mensile_min": can_mensile_min,
        "canone_mensile_max": can_mensile_max,
        "canone_annuo_min": round(can_mensile_min * 12, 2),
        "canone_annuo_max": round(can_mensile_max * 12, 2),
        "avvertenze": []
    }
