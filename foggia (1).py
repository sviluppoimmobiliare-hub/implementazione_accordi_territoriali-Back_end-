

from typing import Literal, Optional
from pydantic import BaseModel, Field
from fastapi import HTTPException



valori_zone = {
    "Zona 1": {"A+": (1.61, 5.35), "A": (1.34, 4.46), "B": (1.24, 4.18), "C": (0.83, 3.07)},
    "Zona 2": {"A+": (1.49, 5.02), "A": (1.24, 4.18), "B": (1.14, 3.91), "C": (0.72, 2.79)},
    "Zona 3": {"A+": (1.37, 4.69), "A": (1.14, 3.91), "B": (1.03, 3.36), "C": (0.62, 2.51)},
    "Zona 4": {"A+": (0.86, 3.35), "A": (0.72, 2.79), "B": (0.62, 2.51), "C": (0.31, 1.95)}
}


confini_zone = {
    "Zona 1": "Area interna delimitata da: piazza Cavour, via Scillitani sino all'incrocio con via "
              "Montegrappa, via del Carso, via Re di Puglia, piazza Vittorio Veneto, via Manfredi, "
              "via Sant'Antonio, via Sant'Alfonso Maria de' Liguori sino all'incrocio con viale "
              "Candelaro, viale Candelaro, viale Ofanto sino all'incrocio con via Guglielmi, via "
              "Guglielmi, via Caggese sino all'incrocio con via Galliani, via Galliani verso piazza "
              "Cavour.",
    "Zona 2": "Dalla perimetrazione di viale Candelaro, viale Giotto sino all'incrocio con via "
              "Altamura, via Altamura, via Rovelli, via L. Perosi, via Martiri di via Fani, via P. "
              "Telesforo, via Natola, viale I Maggio, via degli Aviatori sino all'incrocio con via "
              "Einaudi, via Einaudi, via D'Addedda sino all'incrocio con via Lenotti, via Lenotti, "
              "via Smaldone sino all'incrocio con corso del Mezzogiorno, corso del Mezzogiorno "
              "verso viale Ofanto.",
    "Zona 3": "Tutte le vie restanti non ricomprese nella zona 1 e nella zona 2.",
    "Zona 4": "Zona agricola e frazioni."
}

LISTA_ZONE = list(valori_zone.keys())

ELEMENTI_ESSENZIALI = [
    "Appartamento dal primo piano in poi o piano rialzato con giardino",
    "Impianto di riscaldamento autonomo o centralizzato, ovvero impianto termico come definito "
    "dalla L. 90/2013 e successive modificazioni",
    "Presenza di ascensore"
]

ELEMENTI_NON_ESSENZIALI = [
    "1. Piano intermedio o piano rialzato con giardino",
    "2. Presenza di condizionamento su almeno il 50% dei vani",
    "3. Doppio servizio",
    "4. Posto auto scoperto assegnato da delibera condominiale o box",
    "5. Doppia esposizione",
    "6. Cortile comune",
    "7. Cantina o soffitta",
    "8. Assenza totale di barriere architettoniche nell'edificio (L. 13/1989)",
    "9. Doppi vetri, vetri termici o doppi infissi su almeno il 50% dell'abitazione",
    "10. Sbarre anti-intrusione agli infissi su almeno il 50% dell'abitazione",
    "11. Porta blindata",
    "12. Sistema di allarme singolo e/o videocamera e/o impianti di sicurezza e/o "
    "automazione (domotica)",
    "13. Impianto di videocitofono",
    "14. Copertura in fibra ottica",
    "15. Presenza di autoclave e/o riserva idrica condominiale o autonoma",
    "16. Dotazioni di fonti energetiche rinnovabili",
    "17. Terrazzo o giardino ad uso esclusivo di superficie non inferiore al 20% "
    "dell'unita' immobiliare"
]

ETICHETTE_SUPERFICIE = {
    "mq_calpestabili": "Superficie netta calpestabile dell'immobile in mq",
    "mq_garage": "Garage, box e posti auto accatastati - mq (calcolati al 50%)",
    "mq_accessori": "Terrazzi, balconi, lavanderie, cantine, porticati, verande, ripostigli, "
                    "tavernette e mansarde - mq (calcolati al 25%)",
    "mq_posti_auto": "Posti auto non accatastati ma assegnati da regolamento o delibera "
                     "condominiale - mq (calcolati al 20%)",
    "mq_verde": "Verde e cortile in condominio, quota millesimale - mq (calcolati al 10%)"
}

ETICHETTE_PORZIONE = {
    "porzione": "Viene locata solo una porzione dell'immobile",
    "mq_vani_locati": "Superficie convenzionale dei vani ad uso esclusivo concessi in locazione - mq",
    "mq_condivisi_totali": "Superficie convenzionale totale delle parti e dei servizi condivisi - mq",
    "vani_locati": "Numero di vani ad uso esclusivo concessi in locazione",
    "vani_totali": "Numero totale di vani disponibili"
}

OPZIONI_CONTRATTO = [
    "Contratto agevolato (art. 2, comma 3)",
    "Contratto transitorio ordinario (art. 5, comma 1)",
    "Contratto transitorio per studenti universitari (art. 5, commi 2 e 3)"
]

OPZIONI_DURATA = [
    "Tre anni piu' due",
    "Quattro anni (aumento fino al 2%)",
    "Cinque anni (aumento fino al 4%)",
    "Sei anni o piu' (aumento fino al 6%)"
]

OPZIONI_ARREDO = [
    "Non ammobiliato",
    "Parzialmente ammobiliato con blocco cucina (aumento fino al 10%)",
    "Completamente ammobiliato (aumento fino al 20%)"
]

OPZIONI_CLASSE = [
    "E o inferiore (nessun aumento)",
    "D (+3%)",
    "C (+4%)",
    "B (+6%)",
    "A1, A2, A3 o A4 (+8%)"
]

DESCRIZIONE_AMMOBILIATO = ("Si intende completamente ammobiliato l'immobile il cui arredo comprende i "
                           "vani letto, il soggiorno, il bagno e la cucina, quest'ultima comprensiva "
                           "di piano cottura, forno, frigorifero e lavatrice. Gli elettrodomestici "
                           "devono essere efficienti e funzionali, televisore compreso.") #messaggio info

NOTA_DURATA = ("La maggiorazione per la durata non si applica: i contratti transitori ordinari durano "
               "al massimo diciotto mesi e quelli per studenti al massimo tre anni.")



# MODELLO DI INPUT
# I campi "magg_durata" e "magg_arredo" erano slider: se non vengono inviati (None)
# si usa il valore che lo slider aveva di default, cioe' il tetto massimo.


class InputFoggia(BaseModel):
    tipo_contratto: Literal[
        "Contratto agevolato (art. 2, comma 3)",
        "Contratto transitorio ordinario (art. 5, comma 1)",
        "Contratto transitorio per studenti universitari (art. 5, commi 2 e 3)"
    ] = "Contratto agevolato (art. 2, comma 3)"

    zona: Literal["Zona 1", "Zona 2", "Zona 3", "Zona 4"] = Field(
        "Zona 1",
        description="Zona (Allegato 1). Se l'immobile ricade sulla linea di confine tra due zone si "
                    "prende in considerazione quella di maggior valore (vedi confini_zone in "
                    "GET /citta/foggia/info)"
    )

    piano: int = Field(1, ge=0, le=30, description="Piano dell'appartamento (0 per il piano terra)")
    rialzato_giardino: bool = Field(False, description="Piano rialzato con giardino")

    # superficie convenzionale
    mq_calpestabili: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_calpestabili"])
    mq_garage: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_garage"])
    mq_accessori: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_accessori"])
    mq_posti_auto: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_posti_auto"])
    mq_verde: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["mq_verde"])

    # elementi essenziali (il primo e' ricavato in automatico da piano e rialzato_giardino)
    riscaldamento: bool = Field(False, description=ELEMENTI_ESSENZIALI[1])
    ascensore: bool = Field(
        False,
        description="Presenza di ascensore. Considerato solo oltre il secondo piano: fino al secondo "
                    "piano l'ascensore non e' richiesto."
    )

    elementi_non_essenziali: list[bool] = Field(
        default_factory=lambda: [False] * len(ELEMENTI_NON_ESSENZIALI),
        min_length=len(ELEMENTI_NON_ESSENZIALI), max_length=len(ELEMENTI_NON_ESSENZIALI),
        description="17 caselle true/false, nello stesso ordine della lista ELEMENTI_NON_ESSENZIALI "
                    "(vedi GET /citta/foggia/info)"
    )

    immobile_vincolato: bool = Field(
        False,
        description="Immobile di cui all'art. 1, comma 2, lettera a) della L. 431/98: i valori minimo "
                    "e massimo aumentano del 5%. Considerato solo per il contratto transitorio per "
                    "studenti universitari."
    )

    # maggiorazioni
    durata: Literal[
        "Tre anni piu' due",
        "Quattro anni (aumento fino al 2%)",
        "Cinque anni (aumento fino al 4%)",
        "Sei anni o piu' (aumento fino al 6%)"
    ] = Field("Tre anni piu' due", description="Durata contrattuale. Considerata solo per il "
                                               "contratto agevolato.")
    magg_durata: Optional[float] = Field(
        None, ge=0, le=6,
        description="Aumento per la durata effettivamente concordato (%). Se omesso si usa il tetto "
                    "massimo della durata scelta. Non puo' superare il tetto della durata (2 / 4 / 6)."
    )

    arredo: Literal[
        "Non ammobiliato",
        "Parzialmente ammobiliato con blocco cucina (aumento fino al 10%)",
        "Completamente ammobiliato (aumento fino al 20%)"
    ] = Field("Non ammobiliato", description="Arredamento. " + DESCRIZIONE_AMMOBILIATO)
    magg_arredo: Optional[float] = Field(
        None, ge=0, le=20,
        description="Aumento per l'arredo effettivamente concordato (%). Se omesso si usa il tetto "
                    "massimo dell'opzione di arredo scelta. Non puo' superare il tetto dell'opzione "
                    "(10 / 20)."
    )

    classe: Literal[
        "E o inferiore (nessun aumento)",
        "D (+3%)",
        "C (+4%)",
        "B (+6%)",
        "A1, A2, A3 o A4 (+8%)"
    ] = Field("E o inferiore (nessun aumento)", description="Classe energetica")

    # locazione di porzione di immobile (punto 7)
    porzione: bool = Field(False, description=ETICHETTE_PORZIONE["porzione"])
    mq_vani_locati: float = Field(0.0, ge=0, description=ETICHETTE_PORZIONE["mq_vani_locati"] +
                                                         ". Considerato solo se porzione = true.")
    mq_condivisi_totali: float = Field(0.0, ge=0, description=ETICHETTE_PORZIONE["mq_condivisi_totali"] +
                                                              ". Considerato solo se porzione = true.")
    vani_locati: int = Field(1, ge=0, le=30, description=ETICHETTE_PORZIONE["vani_locati"] +
                                                         ". Considerato solo se porzione = true.")
    vani_totali: int = Field(1, ge=1, le=30, description=ETICHETTE_PORZIONE["vani_totali"] +
                                                         ". Considerato solo se porzione = true.")



# INFO PER IL FRONTEND


INFO = {
    "id": "foggia",
    "nome": "Foggia",
    "titolo": "Calcolatore canone concordato - Comune di Foggia",
    "unita_fasce": "euro/mq mensili",
    "valori_zone": valori_zone,
    "lista_zone": LISTA_ZONE,
    "confini_zone": confini_zone,
    "elementi_essenziali": ELEMENTI_ESSENZIALI,
    "elementi_non_essenziali": ELEMENTI_NON_ESSENZIALI,
    "etichette_superficie": ETICHETTE_SUPERFICIE,
    "etichette_porzione": ETICHETTE_PORZIONE,
    "etichette": {
        "ammobiliato": DESCRIZIONE_AMMOBILIATO
    },
    "opzioni": {
        "tipo_contratto": OPZIONI_CONTRATTO,
        "durata": OPZIONI_DURATA,
        "arredo": OPZIONI_ARREDO,
        "classe": OPZIONI_CLASSE
    },
    "note": [
        "Se l'immobile ricade sulla linea di confine tra due zone si prende in considerazione "
        "quella di maggior valore.",
        "Superficie di calcolo: fino a 38 mq la superficie convenzionale e' aumentata del 20% (con "
        "il limite di 38 mq); fino a 55 mq del 15% (con il limite di 55 mq); fino a 70 mq del 10% "
        "(con il limite di 70 mq).",
        "Elementi essenziali: il primo (appartamento dal primo piano in poi o piano rialzato con "
        "giardino) e' ricavato in automatico dai campi piano e rialzato_giardino; l'ascensore e' "
        "richiesto solo oltre il secondo piano.",
        "Piano intermedio: l'accordo non definisce cosa si intenda per piano intermedio, la voce e' "
        "lasciata alla valutazione delle parti.",
        "Fasce: manca un elemento essenziale = C; da 10 a 17 elementi non essenziali = A+; da 5 a 9 "
        "= A; da 1 a 4 = B; nessuno = C.",
        "Le maggiorazioni (durata, arredo, classe energetica) sono progressive: si applicano una "
        "sull'altra con un moltiplicatore (punto 9).",
        NOTA_DURATA
    ]
}



# CALCOLO (stessi passaggi, nello stesso ordine, del file Streamlit)


def calcola(dati: InputFoggia) -> dict:
    note = []
    avvertenze = []

    tipo_contratto = dati.tipo_contratto
    zona = dati.zona
    piano = dati.piano
    rialzato_giardino = dati.rialzato_giardino
    mq_calpestabili = dati.mq_calpestabili

    if mq_calpestabili <= 0.0:
        raise HTTPException(
            status_code=400,
            detail="Inserire la superficie netta calpestabile per ottenere la stima"
        )

    porzione = dati.porzione
    if porzione == True and dati.mq_vani_locati <= 0.0:
        raise HTTPException(
            status_code=400,
            detail="Inserire la superficie dei vani locati per ottenere la stima"
        )

    # SUPERFICIE CONVENZIONALE

    mq_convenzionali = (mq_calpestabili
                        + dati.mq_garage * 0.50
                        + dati.mq_accessori * 0.25
                        + dati.mq_posti_auto * 0.20
                        + dati.mq_verde * 0.10)

    mq_finali = mq_convenzionali
    if mq_convenzionali <= 38.0:
        mq_finali = mq_convenzionali * 1.20
        if mq_finali > 38.0:
            mq_finali = 38.0
    elif mq_convenzionali <= 55.0:
        mq_finali = mq_convenzionali * 1.15
        if mq_finali > 55.0:
            mq_finali = 55.0
    elif mq_convenzionali <= 70.0:
        mq_finali = mq_convenzionali * 1.10
        if mq_finali > 70.0:
            mq_finali = 70.0

    # ELEMENTI ESSENZIALI

    ess1 = False
    if piano >= 1 or rialzato_giardino == True:
        ess1 = True

    ess2 = dati.riscaldamento

    ess3 = True
    if piano > 2:
        ess3 = dati.ascensore
    else:
        note.append("Ascensore: non richiesto per gli appartamenti fino al secondo piano")

    elementi_essenziali = [ess1, ess2, ess3]
    n_essenziali = sum(e for e in elementi_essenziali if e == True)

    # ELEMENTI NON ESSENZIALI

    elementi_non_essenziali = dati.elementi_non_essenziali
    n_non_essenziali = sum(n for n in elementi_non_essenziali if n == True)

    if n_essenziali < 3:
        fascia = "C"
    elif n_non_essenziali >= 10:
        fascia = "A+"
    elif n_non_essenziali >= 5:
        fascia = "A"
    elif n_non_essenziali >= 1:
        fascia = "B"
    else:
        fascia = "C"

    val_min, val_max = valori_zone[zona][fascia]

    if tipo_contratto.startswith("Contratto transitorio per studenti"):
        immobile_vincolato = dati.immobile_vincolato
        if immobile_vincolato == True:
            val_min = val_min + val_min * 0.05
            val_max = val_max + val_max * 0.05
            note.append("Immobile di cui all'art. 1, comma 2, lettera a) della L. 431/98: valori "
                        "minimo e massimo aumentati del 5%")

    # MAGGIORAZIONI (progressive: si moltiplicano una sull'altra)

    moltiplicatore = 1.0

    if tipo_contratto.startswith("Contratto agevolato"):
        durata = dati.durata
        tetto_durata = 0
        if durata.startswith("Quattro"):
            tetto_durata = 2
        elif durata.startswith("Cinque"):
            tetto_durata = 4
        elif durata.startswith("Sei"):
            tetto_durata = 6

        if tetto_durata > 0:
            # lo slider aveva come default il tetto massimo
            if dati.magg_durata is None:
                magg_durata = tetto_durata
            else:
                magg_durata = dati.magg_durata
            if magg_durata > tetto_durata:
                raise HTTPException(
                    status_code=400,
                    detail=f"L'aumento per la durata ({magg_durata}%) supera il tetto massimo "
                           f"({tetto_durata}%) previsto per l'opzione '{durata}'"
                )
            moltiplicatore = moltiplicatore * (1.0 + magg_durata / 100.0)
    else:
        note.append(NOTA_DURATA)

    arredo = dati.arredo
    tetto_arredo = 0
    if arredo.startswith("Parzialmente"):
        tetto_arredo = 10
    elif arredo.startswith("Completamente"):
        tetto_arredo = 20

    if tetto_arredo > 0:
        if dati.magg_arredo is None:
            magg_arredo = tetto_arredo
        else:
            magg_arredo = dati.magg_arredo
        if magg_arredo > tetto_arredo:
            raise HTTPException(
                status_code=400,
                detail=f"L'aumento per l'arredo ({magg_arredo}%) supera il tetto massimo "
                       f"({tetto_arredo}%) previsto per l'opzione '{arredo}'"
            )
        moltiplicatore = moltiplicatore * (1.0 + magg_arredo / 100.0)

    classe = dati.classe
    if classe.startswith("D "):
        moltiplicatore = moltiplicatore * 1.03
    elif classe.startswith("C "):
        moltiplicatore = moltiplicatore * 1.04
    elif classe.startswith("B "):
        moltiplicatore = moltiplicatore * 1.06
    elif classe.startswith("A1"):
        moltiplicatore = moltiplicatore * 1.08

    # LOCAZIONE DI PORZIONE DI IMMOBILE (punto 7)

    quota_porzione = 1.0
    if porzione == True:
        mq_vani_locati = dati.mq_vani_locati
        mq_condivisi_totali = dati.mq_condivisi_totali
        vani_locati = dati.vani_locati
        vani_totali = dati.vani_totali
        mq_condivisi = mq_condivisi_totali * vani_locati / vani_totali
        if mq_convenzionali > 0.0:
            quota_porzione = (mq_vani_locati + mq_condivisi) / mq_convenzionali
        if quota_porzione > 1.0:
            quota_porzione = 1.0

    canone_base_min = mq_finali * val_min * quota_porzione
    canone_base_max = mq_finali * val_max * quota_porzione
    canone_min = canone_base_min * moltiplicatore
    canone_max = canone_base_max * moltiplicatore

    avvertenze.append("Se l'immobile ricade sulla linea di confine tra due zone si prende in "
                      "considerazione quella di maggior valore.")

    return {
        "citta": "Foggia",
        "zona": zona,
        "fascia": fascia,
        "elementi_essenziali": n_essenziali,
        "elementi_non_essenziali": n_non_essenziali,
        "superficie_convenzionale": round(mq_convenzionali, 2),
        "superficie_calcolo": round(mq_finali, 2),
        "canone_mq_base_min": round(val_min, 4),
        "canone_mq_base_max": round(val_max, 4),
        "moltiplicatore_maggiorazioni": round(moltiplicatore, 4),
        "percentuale_maggiorazioni": round((moltiplicatore - 1.0) * 100, 2),
        "quota_porzione": round(quota_porzione, 4),
        "canone_mq_min": round(val_min * moltiplicatore, 4),
        "canone_mq_max": round(val_max * moltiplicatore, 4),
        "canone_base_min": round(canone_base_min, 2),
        "canone_base_max": round(canone_base_max, 2),
        "canone_mensile_min": round(canone_min, 2),
        "canone_mensile_max": round(canone_max, 2),
        "canone_annuo_min": round(canone_min * 12, 2),
        "canone_annuo_max": round(canone_max * 12, 2),
        "note": note,
        "avvertenze": avvertenze
    }
