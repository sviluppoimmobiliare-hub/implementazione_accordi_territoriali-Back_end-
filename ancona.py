

from typing import Literal, Optional
from pydantic import BaseModel, Field
from fastapi import HTTPException


# ZONE DEL TERRITORIO COMUNALE 
ZONE = {
    "CENTRO e PREGIO": "Passetto - Rione Adriatico - C.so Garibaldi - C.so Matteotti - S. Margherita - "
                       "V.le Vittoria (B1) - Rione San Pietro - Cardeto - Capodimonte (B2) - "
                       "Santo Stefano - Borgo Rodi (B3) - Pietralacroce (D4)",
    "SEMICENTRO (C3-D1-D2-C4)": "Palombare - Pinocchio - Posatora (C3) - B. Bianche - Monte Dago - "
                                "Ponterosso - Passo Varano - Q1 - Q2 (D1) - Torrette - Palombina - "
                                "Collemarino (D2) - Grazie - Tavernelle (C4)",
    "SEMICENTRO (C1-C2-B7)": "Piano S. Lazzaro - M. d. Resistenza - Rione Archi (C1-C2) - "
                             "Rione Monte Marino - Rione Montirozzo (B7)",
    "PERIFERICA-SUBURBANA": "Loc. Candia - Baraccola (D5-E5)",
    "AGRICOLA EST": "Frazioni del Parco Conero - Varano - Montacuto - Poggio - Massignano (R1)",
    "AGRICOLA OVEST": "Altre frazioni - Aspio - Montesicuro - Sappanico - Paterno - Gallignano (R2)"
}

FASCE = {
    "CENTRO e PREGIO":          {"Inferiore": 80.0, "Media": 90.0, "Superiore": 100.0},
    "SEMICENTRO (C3-D1-D2-C4)": {"Inferiore": 70.0, "Media": 80.0, "Superiore": 90.0},
    "SEMICENTRO (C1-C2-B7)":    {"Inferiore": 65.0, "Media": 75.0, "Superiore": 85.0},
    "PERIFERICA-SUBURBANA":     {"Inferiore": 60.0, "Media": 70.0, "Superiore": 80.0},
    "AGRICOLA EST":             {"Inferiore": 50.0, "Media": 60.0, "Superiore": 70.0},
    "AGRICOLA OVEST":           {"Inferiore": 40.0, "Media": 50.0, "Superiore": 60.0}
}

ETICHETTE_SUPERFICIE = {
    "sup_calp": "a - Superficie calpestabile dei vani principali e degli accessori a servizio diretto, "
                "al netto dei muri perimetrali ed interni (mq)",
    "sup_acc_com": "b - Vani accessori a servizio indiretto (soffitte, cantine e simili) COMUNICANTI "
                   "con i vani principali e di caratteristiche omogenee (conteggiati al 30%)",
    "sup_acc_non": "b - Vani accessori a servizio indiretto NON comunicanti (conteggiati al 25%)",
    "sup_balc_com": "c - Balconi, terrazze e simili di pertinenza esclusiva COMUNICANTI (conteggiati al 25%)",
    "sup_balc_non": "c - Balconi, terrazze e simili di pertinenza esclusiva NON comunicanti (conteggiati al 10%)",
    "sup_verde": "d - Aree scoperte a verde in godimento esclusivo (10% fino alla superficie "
                 "convenzionale di cui al punto a, 2% oltre)",
    "sup_garage": "e - Posto auto coperto o garage ad uso esclusivo (conteggiato al 50%)",
    "sup_posto_scop": "f - Posto auto scoperto condominiale assegnato (conteggiato al 20%)"
}

PERTINENZE = [
    ("Garage in uso esclusivo", 5),
    ("Posto auto coperto riservato", 3),
    ("Posto auto scoperto riservato", 2),
    ("Cantina di superficie di almeno 4 mq", 3),
    ("Soffitta praticabile di superficie di almeno 4 mq", 2),
    ("Ripostiglio esterno, sottoscala, soffitta o cantina di superficie inferiore a 4 mq", 1),
    ("Area a verde in godimento esclusivo", 2),
    ("Lavatoio o stenditoio in godimento esclusivo", 1)
]

OPZIONI_BALCONI = [
    "Assenti",
    "Balconi/terrazzi/lastrico solare di superficie complessiva inferiore a 10 mq (+1)",
    "Terrazza o lastrico solare, o piu' balconi per una superficie totale maggiore di 10 mq (+2)"
]

ELEMENTI_CONSERVAZIONE = ["Pavimenti",
                          "Pareti, soffitti e tinteggiatura",
                          "Infissi",
                          "Impianto idrico e servizi igienici e sanitari",
                          "Accessi, scale, ascensore",
                          "Facciate, coperture e parti comuni in genere"]

OPZIONI_CONSERVAZIONE = ["Buone o nuove (2)", "Normali o discrete (1)", "Mediocri o scadenti (0)"]

SERVIZI = [
    ("Ascensore", 2),
    ("Assenza di barriere architettoniche nell'edificio (L. 13/1989)", 2),
    ("Assenza di barriere architettoniche nell'abitazione (L. 13/1989)", 1),
    ("Riscaldamento autonomo o contabilizzato", 1),
    ("Doppi vetri, vetri termici o doppie finestre su almeno il 50% degli infissi", 1),
    ("Cucina abitabile (superficie minima 9 mq piu' finestra)", 2),
    ("Doppi servizi", 3),
    ("Porta blindata e/o barre anti-intrusione a infissi", 1),
    ("Sistema di allarme singolo e/o videocamera e/o impianti di sicurezza/domotica", 2),
    ("Sistema di allarme condominiale e/o videocamera e/o impianti di sicurezza/domotica", 1),
    ("Portiere", 1),
    ("Condizionamento aria su almeno il 50% dei vani", 1),
    ("Impianto TV autonomo o centralizzato", 1),
    ("Impianto antenna parabolica e/o collegamento in rete", 1),
    ("Dotazione di fonti energetiche rinnovabili", 2)
]

OPZIONI_CITOFONO = ["Assente", "Impianto di citofono (+1)", "Impianto di video-citofono (+2)"]
OPZIONI_APE = ["A - B (+4)", "C - D - E (+2)", "F - G (+0)"]

SPAZI_COMUNI = [
    ("Cortili con eventuale piantumazione e/o parcheggio in uso comune (+1%)", 1),
    ("Aree verdi (giardino, orto) in uso comune (+2%)", 2),
    ("Stenditoi/lavatoi comuni (+1%)", 1),
    ("Lastrici solari agibili in uso comune (+1%)", 1),
    ("Aree condominiali comuni, androni o ripostigli (+1%)", 1),
    ("Abitazione AUTONOMA: alloggio singolo o con ingresso indipendente, anche a schiera (+5%)", 5)
]

OPZIONI_CATEGORIA = [
    "A/2 (+0%)",
    "A/7 villini, oppure A/1, A/8, A/9 di cui all'art. 1 c. 2 L. 431/98 (+10%)",
    "A/3 (-2%)",
    "A/4, A/5, A/6 (-4%)"
]

OPZIONI_VETUSTA = [
    "Dal 2000 in poi (0%)",
    "Dal 1975 al 1999 (-4%)",
    "Dal 1955 al 1974 (-8%)",
    "Fino al 1955 (-10%)",
    "Prima del 1935 con stato di conservazione in condizioni di degrado (-20%)"
]

RIDUZIONI_VETUSTA = {
    "Dal 2000 in poi (0%)": 0.0,
    "Dal 1975 al 1999 (-4%)": -4.0,
    "Dal 1955 al 1974 (-8%)": -8.0,
    "Fino al 1955 (-10%)": -10.0,
    "Prima del 1935 con stato di conservazione in condizioni di degrado (-20%)": -20.0
}

OPZIONI_PIANO = [
    "Piano terra, 1 o 2 piano senza ascensore (0%)",
    "Piano intermedio o ultimo con ascensore (+2%)",
    "Piano seminterrato (-4%)",
    "3 piano senza ascensore (-4%)",
    "Oltre il 3 piano senza ascensore (-6%)"
]

PERCENTUALI_PIANO = {
    "Piano terra, 1 o 2 piano senza ascensore (0%)": 0.0,
    "Piano intermedio o ultimo con ascensore (+2%)": 2.0,
    "Piano seminterrato (-4%)": -4.0,
    "3 piano senza ascensore (-4%)": -4.0,
    "Oltre il 3 piano senza ascensore (-6%)": -6.0
}

OPZIONI_MOBILIO = [
    "Non ammobiliato",
    "Parzialmente ammobiliato, es. solo cucina, bagno ed elettrodomestici essenziali (+10/20%)",
    "Ammobiliato (fino a +25%)"
]

OPZIONI_CONTRATTO = [
    "Abitativo 3 anni + 2",
    "Abitativo 4 anni + 2 (+3%)",
    "Abitativo 5 anni + 2 (+5%)",
    "Abitativo 6 anni + 2 (+7%)",
    "Transitorio (1-18 mesi)",
    "Studenti universitari fuori sede, fino a 9 mesi",
    "Studenti universitari fuori sede, da 10 a 12 mesi (+5%)",
    "Studenti universitari fuori sede, da 13 a 24 mesi (+8%)",
    "Studenti universitari fuori sede, da 25 a 36 mesi (+10%)"
]

PERCENTUALI_DURATA = {
    "Abitativo 3 anni + 2": 0.0,
    "Abitativo 4 anni + 2 (+3%)": 3.0,
    "Abitativo 5 anni + 2 (+5%)": 5.0,
    "Abitativo 6 anni + 2 (+7%)": 7.0,
    "Transitorio (1-18 mesi)": 0.0,
    "Studenti universitari fuori sede, fino a 9 mesi": 0.0,
    "Studenti universitari fuori sede, da 10 a 12 mesi (+5%)": 5.0,
    "Studenti universitari fuori sede, da 13 a 24 mesi (+8%)": 8.0,
    "Studenti universitari fuori sede, da 25 a 36 mesi (+10%)": 10.0
}


# MODELLO DI INPUT


class InputAncona(BaseModel):
    zona: Literal[
        "CENTRO e PREGIO",
        "SEMICENTRO (C3-D1-D2-C4)",
        "SEMICENTRO (C1-C2-B7)",
        "PERIFERICA-SUBURBANA",
        "AGRICOLA EST",
        "AGRICOLA OVEST"
    ] = "CENTRO e PREGIO"

   
    sup_calp: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_calp"])
    sup_acc_com: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_acc_com"])
    sup_acc_non: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_acc_non"])
    sup_balc_com: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_balc_com"])
    sup_balc_non: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_balc_non"])
    sup_verde: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_verde"])
    sup_garage: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_garage"])
    sup_posto_scop: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["sup_posto_scop"])

    pertinenze: list[bool] = Field(
        default_factory=lambda: [False] * len(PERTINENZE),
        min_length=len(PERTINENZE), max_length=len(PERTINENZE),
        description="8 caselle true/false, nello stesso ordine della lista PERTINENZE "
                    "(vedi GET /citta/ancona/info)"
    )
    balconi: Literal[
        "Assenti",
        "Balconi/terrazzi/lastrico solare di superficie complessiva inferiore a 10 mq (+1)",
        "Terrazza o lastrico solare, o piu' balconi per una superficie totale maggiore di 10 mq (+2)"
    ] = "Assenti"

   
    conservazione: list[Literal[
        "Buone o nuove (2)", "Normali o discrete (1)", "Mediocri o scadenti (0)"
    ]] = Field(
        default_factory=lambda: ["Normali o discrete (1)"] * len(ELEMENTI_CONSERVAZIONE),
        min_length=len(ELEMENTI_CONSERVAZIONE), max_length=len(ELEMENTI_CONSERVAZIONE),
        description="Una scelta per ciascuno dei 6 elementi, nello stesso ordine della lista "
                    "ELEMENTI_CONSERVAZIONE (vedi GET /citta/ancona/info)"
    )

    servizi: list[bool] = Field(
        default_factory=lambda: [False] * len(SERVIZI),
        min_length=len(SERVIZI), max_length=len(SERVIZI),
        description="15 caselle true/false, nello stesso ordine della lista SERVIZI "
                    "(vedi GET /citta/ancona/info)"
    )
    citofono: Literal["Assente", "Impianto di citofono (+1)", "Impianto di video-citofono (+2)"] = "Assente"
    ape: Literal["A - B (+4)", "C - D - E (+2)", "F - G (+0)"] = "A - B (+4)"

    intensivo: bool = Field(False, description="Alloggio in immobile intensivo, oltre 8 alloggi nello "
                                               "stesso fabbricato (-10%)")
    spazi_comuni: list[bool] = Field(
        default_factory=lambda: [False] * len(SPAZI_COMUNI),
        min_length=len(SPAZI_COMUNI), max_length=len(SPAZI_COMUNI),
        description="6 caselle true/false, nello stesso ordine della lista SPAZI_COMUNI "
                    "(vedi GET /citta/ancona/info)"
    )
    categoria: Literal[
        "A/2 (+0%)",
        "A/7 villini, oppure A/1, A/8, A/9 di cui all'art. 1 c. 2 L. 431/98 (+10%)",
        "A/3 (-2%)",
        "A/4, A/5, A/6 (-4%)"
    ] = "A/2 (+0%)"
    vetusta: Literal[
        "Dal 2000 in poi (0%)",
        "Dal 1975 al 1999 (-4%)",
        "Dal 1955 al 1974 (-8%)",
        "Fino al 1955 (-10%)",
        "Prima del 1935 con stato di conservazione in condizioni di degrado (-20%)"
    ] = "Dal 2000 in poi (0%)"
    manutenzione_post_2000: bool = Field(
        False,
        description="Interventi di manutenzione straordinaria effettuati dopo il 2000 "
                    "(la riduzione per vetusta' si riduce del 50%). Considerato solo se la "
                    "riduzione per vetusta' e' negativa."
    )
    assenza_servizi_igienici: bool = Field(False, description="Assenza di servizi igienici interni "
                                                              "all'abitazione (-15%)")
    assenza_riscaldamento: bool = Field(False, description="Assenza di impianto di riscaldamento esteso "
                                                           "a tutti i vani (-12%)")
    assenza_fognaria: bool = Field(False, description="Assenza di allacciamento alla rete fognaria (-4%)")
    piano: Literal[
        "Piano terra, 1 o 2 piano senza ascensore (0%)",
        "Piano intermedio o ultimo con ascensore (+2%)",
        "Piano seminterrato (-4%)",
        "3 piano senza ascensore (-4%)",
        "Oltre il 3 piano senza ascensore (-6%)"
    ] = "Piano terra, 1 o 2 piano senza ascensore (0%)"

    
    mobilio: Literal[
        "Non ammobiliato",
        "Parzialmente ammobiliato, es. solo cucina, bagno ed elettrodomestici essenziali (+10/20%)",
        "Ammobiliato (fino a +25%)"
    ] = "Non ammobiliato"
    perc_mobilio: Optional[float] = Field(
        None, ge=0, le=25,
        description="Percentuale di incremento per il mobilio. Se omessa si usa il valore di default "
                    "dello slider Streamlit (15 per il parzialmente ammobiliato, 25 per l'ammobiliato). "
                    "Per il parzialmente ammobiliato deve essere compresa tra 10 e 20."
    )
    mobilio_scadente: bool = Field(False, description="Mobilio scadente (la percentuale viene ridotta "
                                                      "del 20%). Considerato solo se la percentuale "
                                                      "mobilio e' maggiore di zero.")

    tipo_contratto: Literal[
        "Abitativo 3 anni + 2",
        "Abitativo 4 anni + 2 (+3%)",
        "Abitativo 5 anni + 2 (+5%)",
        "Abitativo 6 anni + 2 (+7%)",
        "Transitorio (1-18 mesi)",
        "Studenti universitari fuori sede, fino a 9 mesi",
        "Studenti universitari fuori sede, da 10 a 12 mesi (+5%)",
        "Studenti universitari fuori sede, da 13 a 24 mesi (+8%)",
        "Studenti universitari fuori sede, da 25 a 36 mesi (+10%)"
    ] = "Abitativo 3 anni + 2"
    zona_universitaria: bool = Field(
        False,
        description="Alloggio situato in zona universitaria o limitrofa alle sedi universitarie (+5%). "
                    "Considerato solo per i contratti per studenti universitari."
    )


# INFO PER IL FRONTEND


INFO = {
    "id": "ancona",
    "nome": "Ancona",
    "titolo": "Calcolatore Canone Concordato - Comune di Ancona",
    "accordo": "Accordo Territoriale per il Comune di Ancona depositato il 23/04/2019, in vigore dal "
               "01/06/2019 (art. 2 c. 3 e art. 5 L. 431/98, D.M. 16/01/2017)",
    "unita_fasce": "euro/mq annui",
    "zone": ZONE,
    "etichette_superficie": ETICHETTE_SUPERFICIE,
    "pertinenze": [etichetta for etichetta, punti in PERTINENZE],
    "punti_pertinenze": [punti for etichetta, punti in PERTINENZE],
    "elementi_conservazione": ELEMENTI_CONSERVAZIONE,
    "servizi": [etichetta for etichetta, punti in SERVIZI],
    "punti_servizi": [punti for etichetta, punti in SERVIZI],
    "spazi_comuni": [etichetta for etichetta, perc in SPAZI_COMUNI],
    "opzioni": {
        "balconi": OPZIONI_BALCONI,
        "conservazione": OPZIONI_CONSERVAZIONE,
        "citofono": OPZIONI_CITOFONO,
        "ape": OPZIONI_APE,
        "categoria": OPZIONI_CATEGORIA,
        "vetusta": OPZIONI_VETUSTA,
        "piano": OPZIONI_PIANO,
        "mobilio": OPZIONI_MOBILIO,
        "tipo_contratto": OPZIONI_CONTRATTO
    },
    "note": [
        "Conservazione: 2 = buone o nuove; 1 = normali o discrete, in ogni caso funzionanti; "
        "0 = mediocri o scadenti, difettose o deteriorate.",
        "Vani accessori: la parte con altezza inferiore a m 1,70 va prima computata al 30%.",
        "Le percentuali dei correttivi (punto B4) si sommano algebricamente tra loro e si applicano "
        "una sola volta ai valori minimo e massimo ricavati.",
        "Il canone effettivo e' concordato tra le parti entro la forbice minimo-massimo."
    ]
}


# CALCOLO 

def calcola(dati: InputAncona) -> dict:
    
    if 0 < dati.sup_calp < 46:
        quota_a = dati.sup_calp * 1.30                                       
    elif 46 <= dati.sup_calp < 65:
        quota_a = dati.sup_calp * (65 - dati.sup_calp) / 65 + dati.sup_calp  
    elif dati.sup_calp > 95:
        quota_a = 95 + (dati.sup_calp - 95) * 0.50                           
    else:
        quota_a = dati.sup_calp

    if dati.sup_verde <= quota_a:
        quota_verde = dati.sup_verde * 0.10
    else:
        quota_verde = quota_a * 0.10 + (dati.sup_verde - quota_a) * 0.02

    superficie_convenzionale = (quota_a + dati.sup_acc_com * 0.30 + dati.sup_acc_non * 0.25 +
                                dati.sup_balc_com * 0.25 + dati.sup_balc_non * 0.10 +
                                quota_verde + dati.sup_garage * 0.50 + dati.sup_posto_scop * 0.20)

    
    punti_a = 0
    for i in range(len(PERTINENZE)):
        if dati.pertinenze[i]:
            punti_a += PERTINENZE[i][1]

    if "(+1)" in dati.balconi:
        punti_a += 1
    elif "(+2)" in dati.balconi:
        punti_a += 2

    
    punti_b = 0
    for scelta in dati.conservazione:
        if scelta.startswith("Buone"):
            punti_b += 2
        elif scelta.startswith("Normali"):
            punti_b += 1

   
    punti_c = 0
    for i in range(len(SERVIZI)):
        if dati.servizi[i]:
            punti_c += SERVIZI[i][1]

    if "(+1)" in dati.citofono:
        punti_c += 1
    elif "(+2)" in dati.citofono:
        punti_c += 2

    if dati.ape.startswith("A"):
        punti_c += 4
    elif dati.ape.startswith("C"):
        punti_c += 2

    
    def fascia_pertinenze(p):
        if p <= 5:
            return "Inferiore"
        if p <= 10:
            return "Media"
        return "Superiore"

    def fascia_conservazione(p):
        if p <= 5:
            return "Inferiore"
        if p <= 9:
            return "Media"
        return "Superiore"

    def fascia_servizi(p):
        if p <= 7:
            return "Inferiore"
        if p <= 15:
            return "Media"
        return "Superiore"

    fascia_a = fascia_pertinenze(punti_a)
    fascia_b = fascia_conservazione(punti_b)
    fascia_c = fascia_servizi(punti_c)

    vmax_a = FASCE[dati.zona][fascia_a]
    vmax_b = FASCE[dati.zona][fascia_b]
    vmax_c = FASCE[dati.zona][fascia_c]

    
    can_max = (2 * vmax_a + 1 * vmax_b + 2 * vmax_c) / 5
    can_min = can_max * 0.60

    valore_base_min = can_min
    valore_base_max = can_max

    

    correttivi = 0.0

    if dati.intensivo:
        correttivi -= 10

    for i in range(len(SPAZI_COMUNI)):
        if dati.spazi_comuni[i]:
            correttivi += SPAZI_COMUNI[i][1]

    if "+10%" in dati.categoria:
        correttivi += 10
    elif "-2%" in dati.categoria:
        correttivi -= 2
    elif "-4%" in dati.categoria:
        correttivi -= 4

    riduzione_vetusta = RIDUZIONI_VETUSTA[dati.vetusta]
    if riduzione_vetusta < 0:
        if dati.manutenzione_post_2000:
            riduzione_vetusta = riduzione_vetusta / 2
    correttivi += riduzione_vetusta

    if dati.assenza_servizi_igienici:
        correttivi -= 15
    if dati.assenza_riscaldamento:
        correttivi -= 12
    if dati.assenza_fognaria:
        correttivi -= 4

    correttivi += PERCENTUALI_PIANO[dati.piano]

    

    perc_mobilio = 0.0
    if dati.mobilio.startswith("Parzialmente"):
        
        if dati.perc_mobilio is None:
            perc_mobilio = 15.0
        else:
            perc_mobilio = dati.perc_mobilio
        if not (10 <= perc_mobilio <= 20):
            raise HTTPException(
                status_code=400,
                detail="Per l'alloggio parzialmente ammobiliato la percentuale di incremento deve "
                       "essere compresa tra 10 e 20"
            )
    elif dati.mobilio.startswith("Ammobiliato"):
        
        if dati.perc_mobilio is None:
            perc_mobilio = 25.0
        else:
            perc_mobilio = dati.perc_mobilio
    if perc_mobilio > 0:
        if dati.mobilio_scadente:
            perc_mobilio = perc_mobilio * 0.80

    

    perc_durata = PERCENTUALI_DURATA[dati.tipo_contratto]

    perc_zona_univ = 0.0
    if "Studenti" in dati.tipo_contratto:
        if dati.zona_universitaria:
            perc_zona_univ = 5.0

    

    
    mq_min = can_min * (1 + correttivi / 100)
    mq_max = can_max * (1 + correttivi / 100)

    
    mq_min *= (1 + perc_mobilio / 100)
    mq_max *= (1 + perc_mobilio / 100)
    mq_min *= (1 + (perc_durata + perc_zona_univ) / 100)
    mq_max *= (1 + (perc_durata + perc_zona_univ) / 100)

    can_annuo_min = round(mq_min * superficie_convenzionale, 2)
    can_annuo_max = round(mq_max * superficie_convenzionale, 2)
    can_mensile_min = round(can_annuo_min / 12, 2)
    can_mensile_max = round(can_annuo_max / 12, 2)

    return {
        "citta": "Ancona",
        "zona": dati.zona,
        "superficie_convenzionale": round(superficie_convenzionale, 2),
        "punti_pertinenze": punti_a,
        "fascia_pertinenze": fascia_a,
        "punti_conservazione": punti_b,
        "fascia_conservazione": fascia_b,
        "punti_servizi": punti_c,
        "fascia_servizi": fascia_c,
        "valore_base_mq_min": round(valore_base_min, 2),
        "valore_base_mq_max": round(valore_base_max, 2),
        "correttivi_percentuale": round(correttivi, 1),
        "perc_mobilio": round(perc_mobilio, 2),
        "perc_durata": perc_durata,
        "perc_zona_universitaria": perc_zona_univ,
        "canone_mq_annuo_min": round(mq_min, 2),
        "canone_mq_annuo_max": round(mq_max, 2),
        "canone_annuo_min": can_annuo_min,
        "canone_annuo_max": can_annuo_max,
        "canone_mensile_min": can_mensile_min,
        "canone_mensile_max": can_mensile_max,
        "avvertenze": [
            "Il canone effettivo e' concordato tra le parti entro la forbice minimo-massimo."
        ]
    }
