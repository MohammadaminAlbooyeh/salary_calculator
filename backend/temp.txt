import sys

# Monthly net salary calculation 2025 - IRPEF reform 2025
# Law 207/2024 + Legislative Decree 216/2023
# Author: ChatGPT (2025)

def calcola_netto_2025(ral, regione_aliquota=0.0173, comunale_aliquota=0.008):
    """
    Calculate monthly net salary, IRPEF (income tax) and contributions for 2025
    according to the new Italian tax rules.
    """

    # --- PARAMETERS ---
    inps_perc = 0.0919  # employee contributions (contributi INPS dipendente)
    # IRPEF brackets 2025 (scaglioni IRPEF)
    scaglioni = [(28000, 0.23), (50000, 0.35), (float('inf'), 0.43)]

    # --- STEP 1: Total income (IRPEF taxable base - imponibile IRPEF) ---
    imponibile = ral * (1 - inps_perc)

    # --- STEP 2: Gross IRPEF (IRPEF lorda) ---
    irpef_lorda = 0
    residuo = imponibile
    limite_prec = 0
    for limite, aliquota in scaglioni:
        imponibile_scaglione = min(residuo, limite - limite_prec)
        if imponibile_scaglione <= 0:
            break
        irpef_lorda += imponibile_scaglione * aliquota
        residuo -= imponibile_scaglione
        limite_prec = limite

    # --- STEP 3: Standard employee deduction (detrazione lavoro dipendente) ---
    if imponibile <= 15000:
        detrazione_ord = 1955
    elif imponibile <= 28000:
        detrazione_ord = 1910 + 1190 * (28000 - imponibile) / 13000
    elif imponibile <= 50000:
        detrazione_ord = 1910 * (50000 - imponibile) / 22000
    else:
        detrazione_ord = 0

    # --- STEP 4: Additional deduction (ulteriore detrazione - Law 207/2024) ---
    if 20000 < imponibile <= 32000:
        detrazione_extra = 1000
    elif 32000 < imponibile <= 40000:
        detrazione_extra = 1000 * (40000 - imponibile) / 8000
    else:
        detrazione_extra = 0

    # --- STEP 5: Total deductions (totale detrazioni) ---
    detrazioni_tot = detrazione_ord + detrazione_extra

    # --- STEP 6: Net IRPEF (IRPEF netta) ---
    irpef_netta = max(irpef_lorda - detrazioni_tot, 0)

    # --- STEP 7: Regional and municipal surcharges (addizionali regionali e comunali) ---
    addizionali = imponibile * (regione_aliquota + comunale_aliquota)

    # --- STEP 8: Total taxes and contributions (totale imposte e contributi) ---
    contributi = ral * inps_perc
    imposte_tot = irpef_netta + addizionali
    trattenute_tot = contributi + imposte_tot

    # --- STEP 9: Net amounts (netto) ---
    netto_annuo = ral - trattenute_tot
    netto_mensile_12 = netto_annuo / 12
    netto_mensile_13 = netto_annuo / 13

    # --- OUTPUT ---
    risultati = {
        "Gross Annual Salary (RAL)": round(ral, 2),
        "IRPEF Taxable Base (imponibile IRPEF)": round(imponibile, 2),
        "INPS Contributions (contributi INPS)": round(contributi, 2),
        "Gross IRPEF (IRPEF lorda)": round(irpef_lorda, 2),
        "Standard Deduction (detrazione ordinaria)": round(detrazione_ord, 2),
        "Additional Deduction (ulteriore detrazione)": round(detrazione_extra, 2),
        "Total Deductions (totale detrazioni)": round(detrazioni_tot, 2),
        "Net IRPEF (IRPEF netta)": round(irpef_netta, 2),
        "Surcharges (addizionali reg+com)": round(addizionali, 2),
        "Total Taxes (tasse totali IRPEF+addiz)": round(imposte_tot, 2),
        "Total Withholdings (totale trattenute)": round(trattenute_tot, 2),
        "Annual Net Salary (netto annuo)": round(netto_annuo, 2),
        "Monthly Net (12 months - 12 mensilità)": round(netto_mensile_12, 2),
        "Monthly Net (13 months - 13 mensilità)": round(netto_mensile_13, 2)
    }

    return risultati


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python salary_calculation.py <RAL> [regional_rate] [municipal_rate]")
        sys.exit(1)

    ral = float(sys.argv[1])
    regione_aliquota = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0173 # default regional rate (Turin)
    comunale_aliquota = float(sys.argv[3]) if len(sys.argv) > 3 else 0.008 # default municipal rate (Turin)

    dati = calcola_netto_2025(ral, regione_aliquota=regione_aliquota, comunale_aliquota=comunale_aliquota)
    for k, v in dati.items():
        print(f"{k:50}: {v} €")
