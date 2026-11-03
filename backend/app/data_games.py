"""Dati dei Gratta e Vinci attivi con le probabilità ufficiali pubblicate da ADM.

Ogni gioco riporta:
- name / price: nome e prezzo del biglietto in euro
- odds_win: denominatore della probabilità di vincita per premi SUPERIORI al costo
  della giocata (es. 7.84 = "1 biglietto ogni 7,84"), come pubblicato da ADM
- odds_top: denominatore della probabilità di vincere il premio massimo
- top_prize: importo del premio massimo in euro (None se non disponibile)
- source_url / source_label: fonte ufficiale (pagina ADM o portale del concessionario)

NOTA: i giochi attivi cambiano nel tempo. Questi dati sono indicativi e vanno
sempre verificati sulla scheda ufficiale di ciascun gioco su adm.gov.it.
"""

ADM_LOTTERIE_ISTANTANEE = (
    "https://www.adm.gov.it/portale/monopoli/giochi/lotterie/lotterie_istantanee"
)
ADM_NOTE_PROBABILITA = (
    "https://www.adm.gov.it/portale/monopoli/giochi/lotterie/"
    "lotterie_istantanee/lot_ist_note"
)
CONCESSIONARIO_PROBABILITA = "https://www.grattaevinci.com/probabilita-di-vincita"

# Probabilità media complessiva di tutte le lotterie istantanee (fonte: ADM)
PROBABILITA_MEDIA_ADM = 3.60  # "1 su 3,60"
PAYOUT_MASSIMO_PERCENT = 75   # "fino al 75% dell'incasso" (fonte: ADM)

GAMES = [
    {
        "name": "Ping Pong",
        "price": 0.50,
        "odds_win": 9.06,
        "odds_top": None,
        "top_prize": 1_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Disponibile online. Premi superiori al costo: 1 biglietto ogni 9,06.",
    },
    {
        "name": "Winning Star",
        "price": 1.00,
        "odds_win": 7.28,
        "odds_top": None,
        "top_prize": 10_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Premio massimo 10.000 euro (10.000 volte il costo del biglietto).",
    },
    {
        "name": "Viva l'Estate Mini",
        "price": 2.00,
        "odds_win": 7.47,
        "odds_top": None,
        "top_prize": 100_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Tra i biglietti da 2 euro con la probabilità di vincita più alta.",
    },
    {
        "name": "Un'Estate al Mare Mini",
        "price": 2.00,
        "odds_win": 7.48,
        "odds_top": None,
        "top_prize": 100_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": None,
    },
    {
        "name": "Mini Doppia Sfida",
        "price": 2.00,
        "odds_win": 9.59,
        "odds_top": 9_600_000,
        "top_prize": None,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Probabilità di vincita massima: 1 biglietto ogni 9.600.000.",
    },
    {
        "name": "Il Tris Vincente",
        "price": 2.00,
        "odds_win": 9.32,
        "odds_top": None,
        "top_prize": 100_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": None,
    },
    {
        "name": "Turista per 10 anni",
        "price": 2.00,
        "odds_win": 8.52,
        "odds_top": None,
        "top_prize": 100_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Tra i biglietti da 2 euro più vincenti secondo le schede ufficiali.",
    },
    {
        "name": "2026 (biglietto natalizio)",
        "price": 3.00,
        "odds_win": None,
        "odds_top": None,
        "top_prize": 200_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Biglietto delle festività natalizie da 3 euro.",
    },
    {
        "name": "Il Miliardario",
        "price": 5.00,
        "odds_win": 7.84,
        "odds_top": 6_000_000,
        "top_prize": 500_000,
        "source_url": "https://www.adm.gov.it/portale/-/il-miliardario",
        "source_label": "Scheda ADM - Il Miliardario",
        "notes": "Vincita (premi > costo): 1 su 7,84. Premio max 500.000 euro: 1 su 6.000.000.",
    },
    {
        "name": "Miliardario New",
        "price": 5.00,
        "odds_win": 7.59,
        "odds_top": 8_880_000,
        "top_prize": 500_000,
        "source_url": "https://www.adm.gov.it/portale/-/miliardario-new-1",
        "source_label": "Scheda ADM - Miliardario New",
        "notes": "Vincita (premi > costo): 1 su 7,59. Premio max: 1 su 8.880.000.",
    },
    {
        "name": "Dual Play",
        "price": 5.00,
        "odds_win": 6.17,
        "odds_top": None,
        "top_prize": 500_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Tra i biglietti da 5 euro quello con la probabilità ufficiale più alta (1 su 6,17).",
    },
    {
        "name": "Turista per Sempre",
        "price": 5.00,
        "odds_win": 7.10,
        "odds_top": 4_560_000,
        "top_prize": 300_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Premio max: 300.000 euro + 6.000 euro/mese per 20 anni + 100.000 euro di bonus finale (1 su 4.560.000).",
    },
    {
        "name": "Giochi di Natale",
        "price": 5.00,
        "odds_win": 6.45,
        "odds_top": None,
        "top_prize": 500_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Edizione natalizia da 5 euro.",
    },
    {
        "name": "Testa o Croce",
        "price": 5.00,
        "odds_win": 8.41,
        "odds_top": 240_000,
        "top_prize": None,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Probabilità di vincita massima: 1 biglietto ogni 240.000.",
    },
    {
        "name": "Colpo Ricco",
        "price": 10.00,
        "odds_win": 7.77,
        "odds_top": 9_120_000,
        "top_prize": None,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Probabilità di vincita massima: 1 biglietto ogni 9.120.000.",
    },
    {
        "name": "Giochi di Natale Super",
        "price": 10.00,
        "odds_win": 5.34,
        "odds_top": None,
        "top_prize": 2_000_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Migliore probabilità tra i biglietti da 10 euro (1 su 5,34; 1 su 2,99 contando anche i premi pari al costo).",
    },
    {
        "name": "Miliardario Mega",
        "price": 10.00,
        "odds_win": 7.21,
        "odds_top": None,
        "top_prize": 2_000_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": None,
    },
    {
        "name": "La Grande Occasione",
        "price": 15.00,
        "odds_win": 4.24,
        "odds_top": None,
        "top_prize": 3_000_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Probabilità di vincita 23,6% (1 su 4,24 circa) per premi superiori al costo.",
    },
    {
        "name": "Il Miliardario Maxi",
        "price": 20.00,
        "odds_win": 7.45,
        "odds_top": 9_360_000,
        "top_prize": 5_000_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Premio max 5.000.000 euro: 1 su 9.360.000. Payout medio tra i più alti del catalogo.",
    },
    {
        "name": "Giochi di Natale Extra",
        "price": 20.00,
        "odds_win": 6.34,
        "odds_top": None,
        "top_prize": 5_000_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "1 su 6,34 per premi > costo; 1 su 2,88 contando anche i premi pari al costo (migliore del catalogo).",
    },
    {
        "name": "Ultra Numerissimi",
        "price": 20.00,
        "odds_win": 2.94,
        "odds_top": None,
        "top_prize": 5_000_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Probabilità di vincita 34% (1 su 2,94 circa) per premi superiori al costo.",
    },
    {
        "name": "Super Gold",
        "price": 25.00,
        "odds_win": None,
        "odds_top": 10_080_000,
        "top_prize": 6_000_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Premio max 6.000.000 euro: 1 su 10.080.000 (primo lotto).",
    },
    {
        "name": "Milioni di Diamanti",
        "price": 30.00,
        "odds_win": 3.22,
        "odds_top": 9_120_000,
        "top_prize": 6_000_000,
        "source_url": ADM_LOTTERIE_ISTANTANEE,
        "source_label": "Elenco lotterie istantanee attive - ADM",
        "notes": "Biglietto più caro in vendita. Primo lotto: 18.240.000 biglietti, di cui 5.663.636 con premi > 30 euro. Premio max: 1 su 9.120.000.",
    },
]

# Dati AGGREGATI DI ESEMPIO (simulati) per la sezione "Dove si vince di più?".
# Non sono dati reali: servono a mostrare la correlazione statistica
# "più biglietti venduti = più probabilità che escano premi".
POINTS_OF_SALE_SAMPLE = [
    {"name": "Tabaccheria Centrale", "city": "Milano", "region": "MI", "tickets_sold": 184_200, "wins_recorded": 5_210},
    {"name": "Ricevitoria Roma Nord", "city": "Roma", "region": "LA", "tickets_sold": 156_800, "wins_recorded": 4_380},
    {"name": "Tabaccheria del Corso", "city": "Firenze", "region": "FI", "tickets_sold": 121_500, "wins_recorded": 3_410},
    {"name": "Edicola Piazza Garibaldi", "city": "Napoli", "region": "NA", "tickets_sold": 98_700, "wins_recorded": 2_870},
    {"name": "Tabaccheria Stazione", "city": "Torino", "region": "TO", "tickets_sold": 87_300, "wins_recorded": 2_460},
    {"name": "Ricevitoria Lungomare", "city": "Bari", "region": "BA", "tickets_sold": 76_900, "wins_recorded": 2_210},
    {"name": "Tabaccheria San Pietro", "city": "Bologna", "region": "BO", "tickets_sold": 65_400, "wins_recorded": 1_890},
    {"name": "Edicola Universale", "city": "Padova", "region": "PD", "tickets_sold": 54_100, "wins_recorded": 1_520},
    {"name": "Tabaccheria Duomo", "city": "Genova", "region": "GE", "tickets_sold": 48_700, "wins_recorded": 1_380},
    {"name": "Ricevitoria Libertà", "city": "Palermo", "region": "PA", "tickets_sold": 41_200, "wins_recorded": 1_180},
]
