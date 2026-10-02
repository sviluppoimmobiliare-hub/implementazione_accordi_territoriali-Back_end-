
from typing import Literal
from pydantic import BaseModel, Field
from fastapi import HTTPException



ZONE = {
    "ZONA 1": "CITTA' VECCHIA",
    "ZONA 2": "MURAT",
    "ZONA 3": "LIBERTA'",
    "ZONA 4": "MADONNELLA",
    "ZONA 5": "JAPIGIA E SANT'ANNA",
    "ZONA 6": "SAN PAOLO",
    "ZONA 7": "STANIC",
    "ZONA 8": "SAN GIROLAMO - FESCA",
    "ZONA 9": "TORRE A MARE SAN GIORGIO",
    "ZONA 10": "CARRASSI - SAN PASQUALE",
    "ZONA 11": "POGGIOFRANCO - PICONE",
    "ZONA 12": "CARBONARA - CEGLIE - LOSETO",
    "ZONA 13": "SANTO SPIRITO - PALESE"
}

CARATTERISTICHE = [
    "Appartamenti dal 1º piano fuori terra",
    "Ingresso alloggio da piazza o da mare",
    "Balcone con vista su piazza o mare",
    "Allacciamento gas metano",
    "Impianto di condizionamento",
    "Secondo servizio igienico",
    "Spazi esterni ad uso esclusivo e/o condominiale",
    "Porta blindata",
    "Cantina o soffitta o giardino privato o terrazza a livello",
    "Posto auto di pertinenza e/o condominiale assegnato",
    "Box auto",
    "Ascensore",
    "Portierato",
    "Videosorveglianza condominiale o individuale",
    "Impianto fotovoltaico o pannelli solari produzione acqua calda",
    "Impianto citofono",
    "Impianto di videocitofono",
    "Impianto di autoclave",
    "Impianto elettrico interno adeguato ai sensi del D.M. 37/2008",
    "Attico",
    "Ripostiglio",
    "Parquet",
    "Postazione di ricarica veicoli elettrici nel box/posto auto o antenna satellitare",
    "Cucina abitabile di almeno 9 mq. con finestra",
    "Sistemi di sicurezza allarme",
    "Sistemi di domotica in almeno il 50% dell'unità immobiliare",
    "Riscaldamento autonomo o centralizzato o pompa di calore",
    "Infissi interni ed esterni in buono stato",
    "Cassaforte",
    "Doppio ingresso o cortile/giardino recintato"
]

# indici delle caratteristiche usate nelle regole (stesso ordine della lista)
IDX_ASCENSORE = CARATTERISTICHE.index("Ascensore")                                                   # 11
IDX_AUTOCLAVE = CARATTERISTICHE.index("Impianto di autoclave")                                       # 17
IDX_ELETTRICO = CARATTERISTICHE.index("Impianto elettrico interno adeguato ai sensi del D.M. 37/2008")  # 18
IDX_RISCALDAMENTO = CARATTERISTICHE.index("Riscaldamento autonomo o centralizzato o pompa di calore")   # 26
IDX_INFISSI = CARATTERISTICHE.index("Infissi interni ed esterni in buono stato")                     # 27

LISTA_ZONE = list(ZONE.values())

ETICHETTE_SUPERFICIE = {
    "superficie_utile": "Superficie utile calpestabile in mq (non catastale)",
    "superficie_vani_bassi": "Di cui vani con altezza inferiore a 170 cm (conteggiati al 50%)",
    "superficie_autorimessa": "Autorimessa singola ad uso esclusivo in mq (conteggiata al 50%)",
    "superficie_posto_auto": "Posto auto ad uso esclusivo in mq (conteggiato al 25%)",
    "superficie_accessori": "Balconi, terrazze, cortili, cantine, soffitte e accessori simili in mq (conteggiati al 25%)",
    "superficie_scoperta": "Superficie scoperta ad uso esclusivo del conduttore in mq (conteggiata al 15%)",
    "superficie_verde": "Superficie a verde per quota millesimale in mq (conteggiata al 10%)"
}

OPZIONI_CONTRATTO = ["Agevolato (3+2)", "Transitorio ordinario", "Transitorio per studenti universitari"]
OPZIONI_DURATA = ["3 anni", "4 anni (+5%)", "5 anni (+7%)", "6 anni o superiore (+12%)"]
OPZIONI_CLASSE_ENERGETICA = ["G o non dichiarata", "A (A4-A3-A2-A1) (+5%)", "B (+3%)", "C (+3%)",
                             "D (+3%)", "E (+3%)", "F (+3%)"]

DESCRIZIONI_PREGIO = {
    "CITTA' VECCHIA": "Zona di Pregio: gli immobili con balcone su mare o su Piazza Mercantile - "
                      "Piazza Ferrarese - Piazza Massari - Via Venezia",
    "MURAT": "Zona di Pregio: immobili con balcone e ingresso su via Sparano, C.so V. Emanuele, "
             "C.so Cavour, piazza Garibaldi, Piazza Umberto, piazza Moro",
    "LIBERTA'": "Zona di Pregio: Zona Executive - zona contrada Barone"
}




class InputBari(BaseModel):
    zona: Literal[
        "CITTA' VECCHIA",
        "MURAT",
        "LIBERTA'",
        "MADONNELLA",
        "JAPIGIA E SANT'ANNA",
        "SAN PAOLO",
        "STANIC",
        "SAN GIROLAMO - FESCA",
        "TORRE A MARE SAN GIORGIO",
        "CARRASSI - SAN PASQUALE",
        "POGGIOFRANCO - PICONE",
        "CARBONARA - CEGLIE - LOSETO",
        "SANTO SPIRITO - PALESE"
    ] = "CITTA' VECCHIA"


    superficie_utile: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["superficie_utile"])
    superficie_vani_bassi: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["superficie_vani_bassi"])
    superficie_autorimessa: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["superficie_autorimessa"])
    superficie_posto_auto: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["superficie_posto_auto"])
    superficie_accessori: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["superficie_accessori"])
    superficie_scoperta: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["superficie_scoperta"])
    superficie_verde: float = Field(0.0, ge=0, description=ETICHETTE_SUPERFICIE["superficie_verde"])

    tipo_contratto: Literal[
        "Agevolato (3+2)", "Transitorio ordinario", "Transitorio per studenti universitari"
    ] = "Agevolato (3+2)"
    durata_contratto: Literal[
        "3 anni", "4 anni (+5%)", "5 anni (+7%)", "6 anni o superiore (+12%)"
    ] = Field("3 anni", description="Durata del contratto. Considerata solo per il contratto "
                                    "Agevolato (3+2).")
    classe_energetica: Literal[
        "G o non dichiarata", "A (A4-A3-A2-A1) (+5%)", "B (+3%)", "C (+3%)",
        "D (+3%)", "E (+3%)", "F (+3%)"
    ] = "G o non dichiarata"


    caratteristiche: list[bool] = Field(
        default_factory=lambda: [False] * len(CARATTERISTICHE),
        min_length=len(CARATTERISTICHE), max_length=len(CARATTERISTICHE),
        description="30 caselle true/false, nello stesso ordine della lista CARATTERISTICHE "
                    "(vedi GET /citta/bari/info)"
    )


    zona_pregio: bool = Field(
        False,
        description="Zona di Pregio. Considerata solo per CITTA' VECCHIA, MURAT e LIBERTA' "
                    "(vedi descrizioni_pregio in GET /citta/bari/info)."
    )
    piano_oltre_secondo: bool = Field(
        False,
        description="L'immobile e' situato oltre il 2° piano? Rilevante per la Zona di Pregio di "
                    "MURAT: l'ascensore e' richiesto solo dopo il 2° piano."
    )
    buone_condizioni: bool = Field(
        False,
        description="Condizioni generali dell'appartamento e dello stabile buone. Rilevante per la "
                    "Zona di Pregio di MURAT."
    )
    parzialmente_ammobiliato: bool = Field(False, description="L'immobile è parzialmente ammobiliato?")
    totalmente_ammobiliato: bool = Field(False, description="L'immobile è totalmente ammobiliato?")


# INFO PER IL FRONTEND


INFO = {
    "id": "bari",
    "nome": "Bari",
    "titolo": "Calcolatore Canone Concordato - Comune di Bari",
    "unita_fasce": "euro/mq mensili",
    "zone": ZONE,
    "lista_zone": LISTA_ZONE,
    "caratteristiche": CARATTERISTICHE,
    "descrizioni_pregio": DESCRIZIONI_PREGIO,
    "etichette_superficie": ETICHETTE_SUPERFICIE,
    "opzioni": {
        "tipo_contratto": OPZIONI_CONTRATTO,
        "durata_contratto": OPZIONI_DURATA,
        "classe_energetica": OPZIONI_CLASSE_ENERGETICA
    },
    "note": [
        "La parte di superficie convenzionale eccedente i 130 mq e' computata al 50%.",
        "Coefficiente moltiplicatore 1,20 per le superfici piccole: fino a 45 mq la superficie di "
        "calcolo e' aumentata del 20% (con il limite di 45 mq); da 45 a 70 mq e' aumentata del 20% "
        "(con il limite di 70 mq).",
        "È ammessa una tolleranza del 4% in più o in meno sulla superficie convenzionale.",
        "Incremento energetico e maggiorazione di durata sono applicati in cascata sul canone gia' "
        "comprensivo delle regole di arredamento ('si applica progressivamente', punto 4 delle "
        "norme comuni)."
    ]
}

# CALCOLO (stessi passaggi, nello stesso ordine, del file Streamlit;
# i 13 blocchi di zona sono riportati uno per uno come nell'originale)


def calcola(dati: InputBari) -> dict:
    note = []



    superficie_convenzionale = (dati.superficie_utile - dati.superficie_vani_bassi * 0.50 +
                                dati.superficie_autorimessa * 0.50 +
                                dati.superficie_posto_auto * 0.25 +
                                dati.superficie_accessori * 0.25 +
                                dati.superficie_scoperta * 0.15 +
                                dati.superficie_verde * 0.10)


    if superficie_convenzionale > 130:
        superficie_convenzionale = 130 + (superficie_convenzionale - 130) * 0.50

    superficie_calcolo = superficie_convenzionale
    if superficie_convenzionale <= 45:
        superficie_calcolo = min(superficie_convenzionale * 1.20, 45.0)
    elif superficie_convenzionale <= 70:
        superficie_calcolo = min(superficie_convenzionale * 1.20, 70.0)

    if superficie_calcolo <= 0:
        raise HTTPException(
            status_code=400,
            detail="Inserire la superficie dell'immobile prima di stimare il canone"
        )

    # CONTRATTO E CLASSE ENERGETICA

    maggiorazione_durata = 0.0
    if dati.tipo_contratto == "Agevolato (3+2)":
        if dati.durata_contratto == "4 anni (+5%)":
            maggiorazione_durata = 0.05
        elif dati.durata_contratto == "5 anni (+7%)":
            maggiorazione_durata = 0.07
        elif dati.durata_contratto == "6 anni o superiore (+12%)":
            maggiorazione_durata = 0.12

    incremento_energetico = 0.0
    if dati.classe_energetica == "A (A4-A3-A2-A1) (+5%)":
        incremento_energetico = 0.05
    elif dati.classe_energetica != "G o non dichiarata":
        incremento_energetico = 0.03

    # CARATTERISTICHE

    valori_checkbox = dati.caratteristiche
    counter = valori_checkbox.count(True)

    # opzioni di arredamento incompatibili: in Streamlit il blocco di zona veniva
    # saltato con un avviso e la stima non era possibile
    if dati.totalmente_ammobiliato and dati.parzialmente_ammobiliato:
        raise HTTPException(
            status_code=400,
            detail="L'immobile non può essere totalmente e parzialmente arredato allo stesso tempo"
        )

    parzialmente_ammobiliato = dati.parzialmente_ammobiliato
    totalmente_ammobiliato = dati.totalmente_ammobiliato

    # requisiti per la promozione di fascia tramite arredo (identici in tutte le zone)
    requisiti_arredo = (
            valori_checkbox[IDX_AUTOCLAVE] and
            valori_checkbox[IDX_RISCALDAMENTO] and
            valori_checkbox[IDX_INFISSI]
    )

    can_min = 0.0
    can_max = 0.0
    fascia_finale = ""

    zona = dati.zona


    if zona == "CITTA' VECCHIA":
        zona_pregio = dati.zona_pregio
        requisiti_pregio = (zona_pregio and valori_checkbox[IDX_AUTOCLAVE] and
                            valori_checkbox[IDX_RISCALDAMENTO] and valori_checkbox[IDX_ELETTRICO])

        fascia_nativa = ""
        if counter > 5 or requisiti_pregio:
            fascia_nativa = "A"
        elif counter > 3:
            fascia_nativa = "B"
        else:
            fascia_nativa = "C"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 5.26, 6.37
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.26, 6.37
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.26, 6.37 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 4.38, 5.25
                else:
                    can_min, can_max = 2.18, 4.37


    if zona == "MURAT":
        zona_pregio = dati.zona_pregio
        piano_oltre_secondo = dati.piano_oltre_secondo
        buone_condizioni = dati.buone_condizioni
        # L'ascensore è richiesto solo per gli immobili oltre il 2° piano
        requisito_ascensore = valori_checkbox[IDX_ASCENSORE] or not piano_oltre_secondo
        requisiti_pregio = (zona_pregio and valori_checkbox[IDX_AUTOCLAVE] and
                            valori_checkbox[IDX_RISCALDAMENTO] and valori_checkbox[IDX_ELETTRICO] and
                            requisito_ascensore and buone_condizioni)

        fascia_nativa = ""
        if requisiti_pregio:
            fascia_nativa = "A"
        elif counter > 7:
            fascia_nativa = "A"
        elif counter >= 6:
            fascia_nativa = "B"
        elif counter >= 5:
            fascia_nativa = "C"
        else:
            fascia_nativa = "D"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 6.63, 8.20
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 6.63, 8.20
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 6.63, 8.20 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 5.38, 6.62
                else:  # Fascia C
                    can_min, can_max = 4.76, 5.37

        elif fascia_nativa == "D":
            can_min, can_max = 2.37, 4.75
            if parzialmente_ammobiliato or totalmente_ammobiliato:
                note.append("Nota: in fascia D l'accordo non prevede variazioni del canone per l'arredamento")


    if zona == "LIBERTA'":
        zona_pregio = dati.zona_pregio

        fascia_nativa = ""
        if zona_pregio:
            fascia_nativa = "A"
        elif counter > 7:
            fascia_nativa = "A"
        elif counter >= 6:
            fascia_nativa = "B"
        elif counter >= 5:
            fascia_nativa = "C"
        else:
            fascia_nativa = "D"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 5.13, 6.06
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.13, 6.06
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.13, 6.06 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 4.51, 5.12
                else:
                    can_min, can_max = 4.11, 4.50

        elif fascia_nativa == "D":
            can_min, can_max = 3.88, 4.10
            if parzialmente_ammobiliato or totalmente_ammobiliato:
                note.append("Nota: in fascia D l'accordo non prevede variazioni del canone per l'arredamento")


    if zona == "MADONNELLA":
        fascia_nativa = ""
        if counter > 7:
            fascia_nativa = "A"
        elif counter >= 6:
            fascia_nativa = "B"
        elif counter >= 5:
            fascia_nativa = "C"
        else:
            fascia_nativa = "D"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 6.01, 6.50
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 6.01, 6.50
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 6.01, 6.50 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 5.31, 6.00
                else:
                    can_min, can_max = 4.41, 5.30

        elif fascia_nativa == "D":
            can_min, can_max = 3.41, 4.40
            if parzialmente_ammobiliato or totalmente_ammobiliato:
                note.append("Nota: in fascia D l'accordo non prevede variazioni del canone per l'arredamento")


    if zona == "JAPIGIA E SANT'ANNA":
        fascia_nativa = ""
        if counter >= 8:
            fascia_nativa = "A"
        elif counter > 6:
            fascia_nativa = "B"
        elif counter >= 6:
            fascia_nativa = "C"
        else:
            fascia_nativa = "D"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 5.26, 6.00
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.26, 6.00
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.26, 6.00 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 4.81, 5.25
                else:
                    can_min, can_max = 3.51, 4.80

        elif fascia_nativa == "D":
            can_min, can_max = 3.00, 3.50
            if parzialmente_ammobiliato or totalmente_ammobiliato:
                note.append("Nota: in fascia D l'accordo non prevede variazioni del canone per l'arredamento")


    if zona == "SAN PAOLO":
        fascia_nativa = ""
        if counter > 7:
            fascia_nativa = "A"
        elif counter > 6:
            fascia_nativa = "B"
        elif counter >= 6:
            fascia_nativa = "C"
        else:
            fascia_nativa = "D"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 4.94, 5.18
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 4.94, 5.18
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 4.94, 5.18 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 4.57, 4.93
                else:
                    can_min, can_max = 4.32, 4.56

        elif fascia_nativa == "D":
            can_min, can_max = 2.16, 4.31
            if parzialmente_ammobiliato or totalmente_ammobiliato:
                note.append("Nota: in fascia D l'accordo non prevede variazioni del canone per l'arredamento")


    if zona == "STANIC":
        fascia_nativa = ""
        if counter > 7:
            fascia_nativa = "A"
        elif counter >= 7:
            fascia_nativa = "B"
        elif counter >= 6:
            fascia_nativa = "C"
        else:
            fascia_nativa = "D"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 5.19, 5.50
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.19, 5.50
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.19, 5.50 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 4.91, 5.18
                else:
                    can_min, can_max = 4.31, 4.90

        elif fascia_nativa == "D":
            can_min, can_max = 2.16, 4.30
            if parzialmente_ammobiliato or totalmente_ammobiliato:
                note.append("Nota: in fascia D l'accordo non prevede variazioni del canone per l'arredamento")


    if zona == "SAN GIROLAMO - FESCA":
        fascia_nativa = ""
        if counter > 7:
            fascia_nativa = "A"
        elif counter >= 7:
            fascia_nativa = "B"
        elif counter >= 6:
            fascia_nativa = "C"
        else:
            fascia_nativa = "D"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 5.13, 6.00
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.13, 6.00
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.13, 6.00 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 4.51, 5.12
                else:
                    can_min, can_max = 3.88, 4.50

        elif fascia_nativa == "D":
            can_min, can_max = 1.93, 3.87
            if parzialmente_ammobiliato or totalmente_ammobiliato:
                note.append("Nota: in fascia D l'accordo non prevede variazioni del canone per l'arredamento")


    if zona == "TORRE A MARE SAN GIORGIO":
        fascia_nativa = ""
        if counter > 7:
            fascia_nativa = "A"
        elif counter >= 7:
            fascia_nativa = "B"
        else:
            fascia_nativa = "C"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 5.51, 5.90
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.51, 5.90
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.51, 5.90 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 4.71, 5.50
                else:  # Fascia C
                    can_min, can_max = 3.70, 4.70


    if zona == "CARRASSI - SAN PASQUALE":
        fascia_nativa = ""
        if counter > 7:
            fascia_nativa = "A"
        elif counter >= 7:
            fascia_nativa = "B"
        else:
            fascia_nativa = "C"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 7.01, 7.50
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 7.01, 7.50
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 7.01, 7.50 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 6.01, 7.00
                else:  # Fascia C
                    can_min, can_max = 5.50, 6.00


    if zona == "POGGIOFRANCO - PICONE":
        fascia_nativa = ""
        if counter > 7:
            fascia_nativa = "A"
        elif counter >= 7:
            fascia_nativa = "B"
        elif counter >= 6:
            fascia_nativa = "C"
        else:
            fascia_nativa = "D"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 6.88, 7.50
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 6.88, 7.50
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 6.88, 7.50 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 6.26, 6.87
                else:
                    can_min, can_max = 5.61, 6.25

        elif fascia_nativa == "D":

            can_min, can_max = 5.00, 5.60
            if parzialmente_ammobiliato or totalmente_ammobiliato:
                note.append("Nota: in fascia D l'accordo non prevede variazioni del canone per l'arredamento")


    if zona == "CARBONARA - CEGLIE - LOSETO":
        fascia_nativa = ""
        if counter > 7:
            fascia_nativa = "A"
        elif counter >= 7:
            fascia_nativa = "B"
        elif counter >= 6:
            fascia_nativa = "C"
        else:
            fascia_nativa = "D"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 5.26, 5.70
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.26, 5.70
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.26, 5.70 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 4.88, 5.25
                else:
                    can_min, can_max = 4.13, 4.87

        elif fascia_nativa == "D":

            can_min, can_max = 2.06, 4.12
            if parzialmente_ammobiliato or totalmente_ammobiliato:
                note.append("Nota: in fascia D l'accordo non prevede variazioni del canone per l'arredamento")


    if zona == "SANTO SPIRITO - PALESE":
        fascia_nativa = ""
        if counter > 7:
            fascia_nativa = "A"
        elif counter >= 7:
            fascia_nativa = "B"
        else:
            fascia_nativa = "C"

        fascia_finale = fascia_nativa

        if fascia_nativa == "A":
            can_min, can_max = 5.69, 6.12
            if parzialmente_ammobiliato:
                can_min *= 1.10
                can_max *= 1.10
            elif totalmente_ammobiliato:
                can_min *= 1.20
                can_max *= 1.20

        elif fascia_nativa in ["B", "C"]:
            if parzialmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.69, 6.12
            elif totalmente_ammobiliato and requisiti_arredo:
                fascia_finale = "A"
                can_min, can_max = 5.69, 6.12 * 1.10
            else:
                if fascia_nativa == "B":
                    can_min, can_max = 5.13, 5.68
                else:
                    can_min, can_max = 2.56, 5.12



    if can_min <= 0:
        raise HTTPException(
            status_code=400,
            detail="Completare correttamente la selezione delle caratteristiche prima di stimare il canone"
        )


    can_mq_minimo = can_min * (1 + incremento_energetico) * (1 + maggiorazione_durata)
    can_mq_massimo = can_max * (1 + incremento_energetico) * (1 + maggiorazione_durata)
    can_finale_minimo = round(can_mq_minimo * superficie_calcolo, 2)
    can_finale_massimo = round(can_mq_massimo * superficie_calcolo, 2)

    return {
        "citta": "Bari",
        "zona": zona,
        "superficie_convenzionale": round(superficie_convenzionale, 2),
        "superficie_calcolo": round(superficie_calcolo, 2),
        "fascia": fascia_finale,
        "canone_mq_base_min": round(can_min, 2),
        "canone_mq_base_max": round(can_max, 2),
        "incremento_energetico": incremento_energetico,
        "maggiorazione_durata": maggiorazione_durata,
        "canone_mq_min": round(can_mq_minimo, 4),
        "canone_mq_max": round(can_mq_massimo, 4),
        "canone_mensile_min": can_finale_minimo,
        "canone_mensile_max": can_finale_massimo,
        "canone_annuo_min": round(can_finale_minimo * 12, 2),
        "canone_annuo_max": round(can_finale_massimo * 12, 2),
        "note": note,
        "avvertenze": [
            "È ammessa una tolleranza del 4% in più o in meno sulla superficie convenzionale."
        ]
    }

