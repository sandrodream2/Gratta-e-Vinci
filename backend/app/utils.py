"""Funzioni di formattazione numeri in formato italiano."""


def format_number_it(value: float | None) -> str | None:
    """Formatta un numero con separatore delle migliaia '.' e decimali ','.

    7.84 -> "7,84"; 6000000 -> "6.000.000"; 500000.0 -> "500.000".
    """
    if value is None:
        return None
    if float(value).is_integer():
        return f"{int(value):,}".replace(",", ".")
    int_part, dec_part = f"{value:,.2f}".split(".")
    return int_part.replace(",", ".") + "," + dec_part


def format_odds(denominator: float | None) -> str | None:
    """Restituisce l'etichetta '1 su N' da un denominatore (es. 7.84 -> '1 su 7,84')."""
    if denominator is None:
        return None
    return f"1 su {format_number_it(denominator)}"


def format_eur(value: float | None) -> str | None:
    """Formatta un importo in euro (es. 500000 -> '500.000 €')."""
    if value is None:
        return None
    return f"{format_number_it(value)} €"
