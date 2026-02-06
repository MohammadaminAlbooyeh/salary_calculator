"""
Italian tax helper functions (simple model for 2025):
- progressive IRPEF brackets (assumed)
- employee social security (INPS) as a percentage of gross
- regional and municipal surcharges

This module provides a transparent, configurable calculation used by the
Streamlit UI. Rates and brackets are approximate and configurable from the UI.
"""

from typing import Dict, List, Tuple


def italian_brackets_2025() -> List[Tuple[float, float]]:
    """Return list of (threshold, rate) for progressive IRPEF.

    Thresholds are upper bounds for each bracket. Example:
    [(15000, 0.23), (28000, 0.25), (50000, 0.35), (float('inf'), 0.43)]
    """
    return [
        (15000, 0.23),
        (28000, 0.25),
        (50000, 0.35),
        (float("inf"), 0.43),
    ]


def compute_progressive_tax(taxable: float, brackets: List[Tuple[float, float]] = None) -> float:
    """Compute progressive tax (IRPEF) on `taxable` income.

    `brackets` should be list of (upper_bound, rate) sorted ascending.
    """
    if taxable <= 0:
        return 0.0
    # If no brackets provided, use a simplified 2025 scheme matching the
    # rules supplied by the user: 23% up to 28k, 35% 28k-50k, 43% above 50k.
    if brackets is None:
        brackets = [
            (28000, 0.23),
            (50000, 0.35),
            (float("inf"), 0.43),
        ]

    tax = 0.0
    remaining = taxable
    lower = 0.0

    for upper, rate in brackets:
        band_amount = min(remaining, upper - lower)
        if band_amount <= 0:
            lower = upper
            continue
        tax += band_amount * rate
        remaining -= band_amount
        lower = upper
        if remaining <= 0:
            break

    return round(tax, 2)


def compute_social_security(gross: float, rate: float = 0.0919) -> float:
    """Compute employee social security contributions (INPS-like).

    Default rate set to 9.19% as a commonly-used employee share approximation.
    """
    return round(max(0.0, gross * rate), 2)


def compute_regional_municipal(taxable: float, regional_rate: float = 0.01, municipal_rate: float = 0.0023) -> float:
    """Compute small regional and municipal surtaxes on taxable income.

    Defaults combine to 1.23% (configurable).
    """
    return round(taxable * (regional_rate + municipal_rate), 2)


def compute_net_from_gross(
    gross: float,
    social_rate: float = 0.0919,
    regional_rate: float = 0.01,
    municipal_rate: float = 0.0023,
    brackets: List[Tuple[float, float]] = None,
) -> Dict[str, float]:
    """Return a breakdown dict given gross salary.

    - social: employee social contributions
    - taxable: taxable income after social contributions
    - irpef: progressive income tax
    - local: regional + municipal
    - total_tax: irpef + local
    - net: take-home pay (gross - social - total_tax)
    """
    # Employee social contributions
    social = compute_social_security(gross, social_rate)

    # Taxable base (imponibile IRPEF) per the supplied logic
    taxable = round(max(0.0, gross - social), 2)

    # Gross IRPEF using the progressive brackets above
    irpef_lorda = compute_progressive_tax(taxable, brackets)

    # Standard employee deduction (detrazione lavoro dipendente)
    if taxable <= 15000:
        detrazione_ord = 1955.0
    elif taxable <= 28000:
        detrazione_ord = 1910.0 + 1190.0 * (28000 - taxable) / 13000.0
    elif taxable <= 50000:
        detrazione_ord = 1910.0 * (50000 - taxable) / 22000.0
    else:
        detrazione_ord = 0.0

    # Additional deduction introduced by Law 207/2024 (ulteriore detrazione)
    if 20000 < taxable <= 32000:
        detrazione_extra = 1000.0
    elif 32000 < taxable <= 40000:
        detrazione_extra = 1000.0 * (40000 - taxable) / 8000.0
    else:
        detrazione_extra = 0.0

    detrazioni_tot = detrazione_ord + detrazione_extra

    # Net IRPEF after detractions
    irpef_net = max(irpef_lorda - detrazioni_tot, 0.0)

    # Regional and municipal surtaxes
    local = compute_regional_municipal(taxable, regional_rate, municipal_rate)

    total_tax = round(irpef_net + local, 2)

    # Net take-home pay
    net = round(gross - social - total_tax, 2)

    return {
        "gross": round(gross, 2),
        "social": round(social, 2),
        "taxable": round(taxable, 2),
        "irpef": round(irpef_net, 2),
        "local": round(local, 2),
        "total_tax": round(total_tax, 2),
        "net": round(net, 2),
    }


if __name__ == "__main__":
    # quick smoke test
    print(compute_net_from_gross(50000))
