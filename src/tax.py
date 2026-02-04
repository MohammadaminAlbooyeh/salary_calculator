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
    if brackets is None:
        brackets = italian_brackets_2025()

    tax = 0.0
    lower = 0.0
    remaining = taxable

    for upper, rate in brackets:
        band = min(upper - lower, remaining)
        if band <= 0:
            lower = upper
            continue
        tax += band * rate
        remaining -= band
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
    social = compute_social_security(gross, social_rate)
    taxable = max(0.0, gross - social)
    irpef = compute_progressive_tax(taxable, brackets)
    local = compute_regional_municipal(taxable, regional_rate, municipal_rate)
    total_tax = round(irpef + local, 2)
    net = round(gross - social - total_tax, 2)

    return {
        "gross": round(gross, 2),
        "social": social,
        "taxable": round(taxable, 2),
        "irpef": irpef,
        "local": local,
        "total_tax": total_tax,
        "net": net,
    }


if __name__ == "__main__":
    # quick smoke test
    print(compute_net_from_gross(50000))
