import streamlit as st
import numpy as np
import pandas as pd

st.title("Proračun navojnog vretena")
st.info("Ovaj program služi za izračunavanje prvih 3 tačaka grafičkog rada. I dalje treba pratiti uputstvo radi pravilnog ispisivanja na papiru.")

st.markdown("""
### Navigacija

- [Nulta tačka 0](#nulta_tacka_0)
- [Tačka 1](#tacka1)
- [Tačka 2](#tacka2)
- [Tačka 4](#tacka4)
- [Tačka 5](#tacka5)

""")

st.title("Globalni parametri")
F = st.number_input("Unesite silu F (N):", value=10000.0, format="%f")
h = st.number_input("Unesite hod navojnog vratena h (mm):", value=400.0, format="%f")



def nulta_tacka():
    # ===================================
    # Nulta tačka 0
    # ===================================
    st.markdown('<a id="nulta_tacka_0"></a>', unsafe_allow_html=True)

    st.title("Nulta tačka 0")

    mnv = st.selectbox("Izaberite materijal navojnog vretena (mnv):", ["E335", "E295"], key="mnv_nt")

    # Podesavanje σ_D0 i τ_D0 u zavisnosti od materijala
    if mnv == "E335":
        sigmaD0 = 350
        tauD0 = 215
    else:
        sigmaD0 = 310
        tauD0 = 205

    st.write("**Dozvoljeni napon zatezanja:**")
    st.latex(f'''\\sigma_{{(D0)}} = {sigmaD0} \\, \\text{{N/mm}}^2''')
    st.write("**Dozvoljeni napon smicanja:**")
    st.latex(f'''\\tau_{{(D0)}} = {tauD0} \\, \\text{{N/mm}}^2''')

    # Izračunavanje A₃
    st.write("**Formula za površinu A₃:**")
    st.latex('''A_3 = \\frac{1.3 \\times F \\times 2.5}{\\sigma_{D0}}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''A_3 = \\frac{{1.3 \\times {F:.8g} \\times 2.5}}{{{sigmaD0}}}''')

    A3 = (1.3 * F * 2.5) / sigmaD0
    st.write(f"**Izračunata vrednost A₃:**")
    st.latex(f'''A_3 = {A3:.8g} \\, \\text{{mm}}^2''')

    if A3 <= 104:
        st.success("Odabrani navoj: **Tr 16x4**")
    else:
        st.success("Odaberi prvi veći navoj iz tabele 3.2")

    # ===================================
    # Nulta tačka 1
    # ===================================
    st.header("Nulta tačka 1")

    # Konstante
    E = 206000  # Modul elastičnosti (N/mm²)
    st.write("**Modul elastičnosti E:**")
    st.latex(f'''E = {E} \\, \\text{{N/mm}}^2''')
    S = 7       # Koeficijent sigurnosti
    st.write("**Koeficijent sigurnosti S:**")
    st.latex(f'''S = {S}''')

    # Izračunavanje d₃
    st.write("**Formula za prečnik d₃:**")
    st.latex('''d_3 = \\sqrt[4]{ \\frac{64 \\times F \\times S \\times h^2}{\\pi^3 \\times E} }''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''d_3 = \\sqrt[4]{{ \\frac{{64 \\times {F:.8g} \\times {S} \\times {h:.8g}^2}}{{\\pi^3 \\times {E}}} }}''')

    d3 = ((64 * F * S * h ** 2) / (np.pi ** 3 * E)) ** 0.25
    st.write("**Izračunata vrednost d₃:**")
    st.latex(f'''d_3 = {d3:.8g} \\, \\text{{mm}}''')
    st.write(f"**d₃ ≥ {d3:.8g} mm**")
    st.info("Uzmi prvi veći prečnik iz tabele 3.2")

    # ===================================
    # Nulta tačka 2
    # ===================================
    st.header("Nulta tačka 2")

    d = st.number_input("Unesite prečnik navoja d (mm):", value=24.0, format="%.8g", key="d_nt2")
    P = st.number_input("Unesite korak navoja P (mm):", value=5.0, format="%.8g", key="P_nt2")
    d2 = st.number_input("Unesite srednji prečnik navoja d₂ (mm):", value=21.5, format="%.8g", key="d2_nt2")

    H1 = P / 2
    st.write("**Izračunavanje H₁:**")
    st.latex(f'''H_1 = \\frac{{P}}{{2}} = \\frac{{{P:.8g}}}{{2}} = {H1:.8g} \\, \\text{{mm}}''')

    st.write("**Proračun broja navoja Zₙᵖʳᵉ i dužine navoja Lₙ:**")
    st.latex('''Z_n^{pre} = \\frac{F}{p_{doz} \\times d_2 \\times \\pi \\times H_1}''')
    st.latex(f'''Z_n^{{pre}} = \\frac{{{F:.8g}}}{{p_{{doz}} \\times {d2:.8g} \\times \\pi \\times {H1:.8g}}}''')

    results = []

    for pdoz in range(10, 21):
        Zn_pre = F / (pdoz * d2 * np.pi * H1)
        Zn = max(6, min(Zn_pre, 10))
        if Zn_pre > 10:
            continue
        Ln = P * Zn
        lower_bound = 1.3 * d
        upper_bound = 1.6 * d
        if lower_bound < Ln < upper_bound:
            status = '✅ Odgovara'
        else:
            status = '❌ Ne odgovara'
        results.append({
            'p_dož [N/mm²]': pdoz,
            'Z_n pre': round(Zn_pre, 6),
            'Z_n': Zn,
            'L_n [mm]': round(Ln, 6),
            'Status': status,
            'Donja granica [mm]': round(lower_bound, 6),
            'Gornja granica [mm]': round(upper_bound, 6),
        })

    if not results:
        st.error("Nema tačnih odgovora, izaberite druge parametre")
    else:
        df = pd.DataFrame(results)
        st.write(f"**Rezultati za Tr {d} x {P}:**")
        st.dataframe(df)

    # ===================================
    # Ponovno unošenje parametara
    # ===================================
    st.info("Nove parametre zapisati ispod racuna iz tabel 3.2")
    st.subheader("Unesite nove parametre za dalji proračun")

    P = st.number_input("Ponovo unesite korak navoja P (mm):", value=P, format="%.8g", key="P_nt_repeat")
    d2 = st.number_input("Ponovo unesite srednji prečnik navoja d₂ (mm):", value=d2, format="%.8g", key="d2_nt_repeat")

    # ===================================
    # Nulta tačka 3
    # ===================================
    st.header("Nulta tačka 3")

    # Izračunavanje ugla navoja φ
    st.write("**Izračunavanje ugla navoja φ:**")
    st.latex('''\\varphi = \\arctan\\left( \\frac{P}{\\pi \\times d_2} \\right)''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\varphi = \\arctan\\left( \\frac{{{P:.8g}}}{{\\pi \\times {d2:.8g}}} \\right)''')

    fi = np.arctan(P / (d2 * np.pi))
    fi_deg = np.degrees(fi)
    st.write("**Izračunata vrednost ugla navoja φ:**")
    st.latex(f'''\\varphi = {fi_deg:.8g}^\\circ''')

    # Postavljena vrednost faktora trenja μ
    f = 0.09
    st.write("**Postavljena vrednost faktora trenja μ:**")
    st.latex('''\\mu = 0.09''')

    # Izračunavanje ugla trenja ρ
    st.write("**Izračunavanje ugla trenja ρ:**")
    st.latex('''\\rho = \\arctan\\left( \\frac{\\mu}{\\cos 15^\\circ} \\right)''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\rho = \\arctan\\left( \\frac{{{f}}}{{\\cos 15^\\circ}} \\right)''')

    rho = np.arctan(f / np.cos(np.radians(15)))
    rho_deg = np.degrees(rho)
    st.write("**Izračunata vrednost ugla trenja ρ:**")
    st.latex(f'''\\rho = {rho_deg:.8g}^\\circ''')

    # Izračunavanje momenta na navojnom paru Tₙₚ
    st.write("**Izračunavanje momenta na navojnom paru Tₙₚ:**")
    st.latex('''T_{np} = \\frac{F \\times d_2}{2} \\times \\tan(\\varphi + \\rho)''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''T_{{np}} = \\frac{{{F:.8g} \\times {d2:.8g}}}{{2}} \\times \\tan({fi_deg:.8g}^\\circ + {rho_deg:.8g}^\\circ)''')

    Tnp = (F * d2) / 2 * np.tan(fi + rho)
    st.write("**Izračunata vrednost momenta Tₙₚ:**")
    st.latex(f'''T_{{np}} = {Tnp:.8g} \\text{{ Nmm}}''')

def tacka1():
    # ===================================
    # Tačka 1
    # ===================================
    st.markdown('<a id="tacka1"></a>', unsafe_allow_html=True)
    st.header("Tačka 1")

    # Unos potrebnih vrednosti
    sigmaD0 = st.number_input("Unesite dozvoljeni napon zatezanja σ(D0) (N/mm²):", value=350.0, format="%.8g", key="sigmaD0_t1")
    tauD0 = st.number_input("Unesite dozvoljeni napon smicanja τ(D0) (N/mm²):", value=215.0, format="%.8g", key="tauD0_t1")
    A3 = st.number_input("Unesite površinu A₃ (mm²):", value=150.0, format="%.8g", key="A3_t1")
    d3 = st.number_input("Unesite prečnik d₃ (mm):", value=30.0, format="%.8g", key="d3_t1")
    d2 = st.number_input("Unesite srednji prečnik navoja d₂ (mm):", value=21.5, format="%.8g", key="d2_t1")
    P = st.number_input("Unesite korak navoja P (mm):", value=5.0, format="%.8g", key="P_t1")
    Ln = st.number_input("Unesite dužinu navoja Lₙ (mm):", value=75.0, format="%.8g", key="Ln_t1")
    E = 206000  # Modul elastičnosti (N/mm²)

    # H1 i ostale konstante
    H1 = P / 2
    f = 0.09
    fi = np.arctan(P / (d2 * np.pi))
    fi_deg = np.degrees(fi)
    rho = np.arctan(f / np.cos(np.radians(15)))
    rho_deg = np.degrees(rho)
    Tnp = (F * d2) / 2 * np.tan(fi + rho)
    sigma = F / A3
    S_sigma = sigmaD0 / sigma
    tau = Tnp / (0.2 * d3 ** 3)
    S_tau = tauD0 / tau
    S_total = (S_sigma * S_tau) / np.sqrt(S_sigma ** 2 + S_tau ** 2)

    # Prikaz rezultata tačke 1.1
    st.subheader("Tačka 1.1")

    st.write("**Izračunavanje napona zatezanja σ:**")
    st.latex('''\\sigma = \\frac{F}{A_3}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\sigma = \\frac{{{F:.8g}}}{{{A3:.8g}}}''')
    st.write("**Izračunata vrednost napona σ:**")
    st.latex(f'''\\sigma = {sigma:.8g} \\text{{ N/mm²}}''')
    st.write("**Izracunavanje Sσ**")
    st.latex(f'''S_σ = \\frac{{\\sigma_{{(D0)}}}}{{\\sigma}} = \\frac{{350}}{{{sigma:.8g}}} = {S_sigma:.8g}''') 

    st.write("**Izračunavanje napona smicanja τ:**")
    st.latex('''\\tau = \\frac{T_{np}}{0.2 \\times d_3^3}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\tau = \\frac{{{Tnp:.8g}}}{{0.2 \\times {d3:.8g}^3}}''')
    st.write("**Izračunata vrednost napona τ:**")
    st.latex(f'''\\tau = {tau:.8g} \\text{{ N/mm²}}''')
    st.write("**Izračunavanje Sτ**")
    st.latex(f'''S_τ = \\frac{{\\tau_{{(D0)}}}}{{\\tau}} = \\frac{{215}}{{{tau:.8g}}} = {S_tau:.8g}''')

    st.write("**Ukupni koeficijent sigurnosti S:**")
    st.latex('''S = \\frac{S_\\sigma \\times S_\\tau}{\\sqrt{S_\\sigma^2 + S_\\tau^2}}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''S = \\frac{{{S_sigma:.8g} \\times {S_tau:.8g}}}{{\\sqrt{{{S_sigma:.8g}^2 + {S_tau:.8g}^2}}}}''')
    st.write("**Izračunata vrednost S:**")
    st.latex(f'''S = {S_total:.8g}''')
    st.info("Treba da bude veće od **S_min = 1.5 – 2 (dodati komentar)**")

    # Tačka 1.2
    st.subheader("Tačka 1.2")
    st.info("Vrednost za Bₗ se vadi iz tabele prilozene na sajtu nazvane 'DVOREDI-LEZAJEVI.pdf'")
    Bl = st.number_input("Unesite vrednost Bₗ (mm):", value=19.0, format="%.8g", key="Bl_t1")
    i = d3 / 4
    Lk = (Ln / 2) + h + 10 + (Bl / 2)
    st.write("**Izračunavanje Lk:**")
    st.latex('''L_k = \\frac{L_n}{2} + h + 10 + \\frac{B_l}{2}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''L_k = \\frac{{{Ln:.8g}}}{{2}} + {h:.8g} + 10 + \\frac{{{Bl:.8g}}}{{2}}''')
    st.write("**Izračunata vrednost Lk:**")
    st.latex(f'''L_k = {Lk:.8g} \\text{{ mm}}''')
    st.latex("i = \\frac{d_3}{4} = \\frac{30}{4} = 7.5")
    lamda = Lk / i
    st.write("**Izračunavanje vitkosti λ:**")
    st.latex('''\\lambda = \\frac{L_k}{i}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\lambda = \\frac{{{Lk:.8g}}}{{{i:.8g}}}''')
    st.write("**Izračunata vrednost λ:**")
    st.latex(f'''\\lambda = {lamda:.8g}''')

    if lamda <= 89:
        sigmaK = 335 - 0.62 * lamda
        st.write("**Za λ ≤ 89 dozvoljeni kritični napon σₖ se računa:**")
        st.latex('''\\sigma_{k} = 335 - 0.62 \\times \\lambda''')
        st.write("**Sa unetim vrednostima:**")
        st.latex(f'''\\sigma_{{k}} = 335 - 0.62 \\times {lamda:.8g}''')
    else:
        sigmaK = (E * np.pi ** 2) / (lamda ** 2)
        st.write("**Za λ > 89 dozvoljeni kritični napon σₖ se računa:**")
        st.latex('''\\sigma_{k} = \\frac{E \\times \\pi^2}{\\lambda^2}''')
        st.write("**Sa unetim vrednostima:**")
        st.latex(f'''\\sigma_{{k}} = \\frac{{{E} \\times \\pi^2}}{{{lamda:.8g}^2}}''')

    st.write("**Izračunata vrednost dozvoljenog kritičnog napona σₖ:**")
    st.latex(f'''\\sigma_{{k}} = {sigmaK:.8g} \\text{{ N/mm²}}''')

    sigma_i = np.sqrt(sigma ** 2 + 3 * tau ** 2)
    st.write("**Izračunavanje ekvivalentnog napona σᵢ:**")
    st.latex('''\\sigma_{i} = \\sqrt{ \\sigma^2 + 3 \\times \\tau^2 }''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\sigma_{{i}} = \\sqrt{{ {sigma:.8g}^2 + 3 \\times {tau:.8g}^2 }}''')
    st.write("**Izračunata vrednost σᵢ:**")
    st.latex(f'''\\sigma_{{i}} = {sigma_i:.8g} \\text{{ N/mm²}}''')

    S_i = sigmaK / sigma_i
    st.write("**Koeficijent sigurnosti na izvijanje Sᵢ:**")
    st.latex('''S_{i} = \\frac{\\sigma_{k}}{\\sigma_{i}}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''S_{{i}} = \\frac{{{sigmaK:.8g}}}{{{sigma_i:.8g}}}''')
    st.write("**Izračunata vrednost Sᵢ:**")
    st.latex(f'''S_{{i}} = {S_i:.8g}''')

    # Tačka 1.3
    st.subheader("Tačka 1.3")
    p = (F * P) / (Ln * d2 * np.pi * H1)
    st.write("**Izračunavanje pritiska na bok navoja p:**")
    st.latex('''p = \\frac{F \\times P}{L_n \\times d_2 \\times \\pi \\times H_1}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''p = \\frac{{{F:.8g} \\times {P:.8g}}}{{{Ln:.8g} \\times {d2:.8g} \\times \\pi \\times {H1:.8g}}}''')
    st.write("**Izračunata vrednost p:**")
    st.latex(f'''p = {p:.8g} \\text{{ N/mm²}}''')
    if 10 <= p <= 20:
        st.success("Rezultat zadovoljava uslov (**10 ≤ p ≤ 20**)")
    else:
        st.warning("Rezultat ne zadovoljava uslov (**10 ≤ p ≤ 20**)")
    st.info("Ovo treba staviti samo kao komentar ovo je direktna provera usvojene vrednosti za pdoz iz tacke 0.2")

    # Tačka 1.4
    st.subheader("Tačka 1.4")
    eta_np = np.tan(fi) / np.tan(fi + rho)
    eta_nv = 0.9 * eta_np
    st.write("**Izračunavanje mehaničkog stepena korisnosti ηₙₚ:**")
    st.latex('''\\eta_{np} = \\frac{\\tan(\\varphi)}{\\tan(\\varphi + \\rho)}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\eta_{{np}} = \\frac{{\\tan({fi_deg:.8g}^\\circ)}}{{\\tan({fi_deg:.8g}^\\circ + {rho_deg:.8g}^\\circ)}}''')
    st.write("**Izračunata vrednost ηₙₚ:**")
    st.latex(f'''\\eta_{{np}} = {eta_np:.8g}''')

    st.write("**Izračunavanje ukupnog stepena korisnosti ηₙᵥ:**")
    st.latex('''\\eta_{nv} = 0.9 \\times \\eta_{np}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\eta_{{nv}} = 0.9 \\times {eta_np:.8g}''')
    st.write("**Izračunata vrednost ηₙᵥ:**")
    st.latex(f'''\\eta_{{nv}} = {eta_nv:.8g}''')

    # Tačka 1.5
    st.subheader("Tačka 1.5")
    if fi > rho:
        st.warning("**Navoj nije samokočiv**")
    else:
        st.success("**Navoj je samokočiv**")

def tacka2():
    # ===================================
    # Tačka 2
    # ===================================
    st.markdown('<a id="tacka2"></a>', unsafe_allow_html=True)
    st.header("Tačka 2")

    # Unos vrednosti
    z = st.number_input("Unesite broj z:", value=4.0, format="%.8g", key="z_t2")
    Reh = st.number_input("Unesite vrednost Rₑₕ (N/mm²):", value=300.0, format="%.8g", key="Reh_t2")

# Izračunavanja
    st.write("**Izračunavanje reakcije po jednom vijku Fᵣ:**")
    st.latex('''F_{r} = \\frac{F}{z}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''F_{{r}} = \\frac{{{F:.8g}}}{{{z:.8g}}}''')
    Fr = F / z
    st.write("**Izračunata vrednost Fᵣ:**")
    st.latex(f'''F_{{r}} = {Fr:.8g} \\text{{ N}}''')

    st.write("**Izračunavanje prednaprezanja Fₚ:**")
    y = st.slider("Faktor prednaprezanja y (2-4):", min_value=2.0, max_value=4.0, value=3.0, step=0.1)
    st.info("Ako ima potrebe pomeraj slajder dok ne dobiješ vrednost za odgovrajući stepen sigurnosti u granicama")
    st.latex('''F_{p} = y \\times F_{r}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''F_{{p}} = {y} \\times {Fr:.8g}''')
    Fp_initial = y * Fr
    st.write("**Izračunata vrednost Fₚ:**")
    st.latex(f'''F_{{p}} = {Fp_initial:.8g} \\text{{ N}}''')

    st.write("**Izračunavanje potrebnog preseka Aₛ:**")
    st.latex('''A_{s} = \\frac{F_{p}}{0.6 \\times R_{eH}}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''A_{{s}} = \\frac{{{Fp_initial:.8g}}}{{0.6 \\times {Reh:.8g}}}''')
    As_theoretical = Fp_initial / (0.6 * Reh)
    st.write("**Izračunata vrednost Aₛ:**")
    st.latex(f'''A_{{s}} = {As_theoretical:.8g} \\text{{ mm²}}''')
    st.info("Uzmi prvi veći presek iz tabele 3.1")

    # Unos As iz tabele
    As = st.number_input("Unesite vrednost Aₛ (mm²):", value=58.0, format="%.8g", key="As_t2")
    st.write("**Izračunavanje novog prednaprezanja Fₚ:**")
    st.latex('''F_p = 0.6 \\times A_{s} \\times R_{eH}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''F_p = 0.6 \\times {As:.8g} \\times {Reh:.8g}''')
    Fp = 0.6 * As * Reh
    st.write("**Izračunata vrednost Fₚ_novo:**")
    st.latex(f'''F_p = {Fp:.8g} \\text{{ N}}''')

    if Fp >= Fp_initial:
        st.success("Provera uspešna, nastavi sa proračunom.")
    else:
        st.error("Provera nije uspešna, novo Fₚ nije veće ili jednako početnom Fₚ.")

    # Unos novih parametara
    st.subheader("Unesite nove parametre za dalji proračun iz tabele 3.1")
    d2_new = st.number_input("Unesite srednji prečnik navoja d₂ (mm):", value=21.5, format="%.8g", key="d2_t2")
    d3_new = st.number_input("Unesite prečnik d₃ (mm):", value=30.0, format="%.8g", key="d3_t2")
    phi_deg = st.number_input("Unesite ugao navoja φ (stepeni):", value=7.125, format="%.8g", key="phi_deg_t2")
    fi_new = np.radians(phi_deg)

    # Tačka 2.1
    st.subheader("Tačka 2.1")
    st.info("Sledece parametre uneti iz tabele 3.5 i 3.6")
    tauT = st.number_input("Unesite dozvoljeni napon smicanja τₜ (N/mm²):", value=200.0, format="%.8g", key="tauT_t2")
    SigmaAM = st.number_input("Unesite dozvoljeni amplitudni napon σₐₘ (N/mm²):", value=50.0, format="%.8g", key="SigmaAM_t2")

    # Izračunavanje napona zatezanja σ
    st.write("**Izračunavanje napona zatezanja σ:**")
    st.latex('''\\sigma = \\frac{F_{p}}{A_{s}}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\sigma = \\frac{{{Fp:.8g}}}{{{As:.8g}}}''')
    sigma = Fp / As
    st.write("**Izračunata vrednost σ:**")
    st.latex(f'''\\sigma = {sigma:.8g} \\text{{ N/mm²}}''')
    S_sigma = Reh / sigma
    st.write("**Izračunat koeficijent sigurnosti Sσ:**")
    st.latex(f'''S_σ = \\frac{{R_{{eH}}}}{{\\sigma}} = \\frac{{300}}{{{sigma:.8g}}} = {S_sigma:.8g}''')

    # Izračunavanje Wp
    st.write("**Izračunavanje otpornog momenta Wₚ:**")
    st.latex('''W_{p} = 0.2 \\times \\left( \\frac{d_{2} + d_{3}}{2} \\right)^3''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''W_{{p}} = 0.2 \\times \\left( \\frac{{{d2_new:.8g} + {d3_new:.8g}}}{{2}} \\right)^3''')
    Wp = 0.2 * ((d2_new + d3_new) / 2) ** 3
    st.write("**Izračunata vrednost Wₚ:**")
    st.latex(f'''W_{{p}} = {Wp:.8g} \\text{{ mm³}}''')

    # Izračunavanje momenta zavrtanja Tₜ
    st.write("**Izračunavanje momenta zavrtanja Tₜ:**")
    st.latex('''T_{t} = \\frac{F_{p} \\times d_{2}}{2} \\times \\tan(\\varphi + \\rho)''')
    f_val = st.number_input("Faktor trenja μ:", value=0.15, format="%.8g", key="f_val_t2")
    rho_val = np.arctan(f_val / np.cos(np.radians(30)))
    rho_val_deg = np.degrees(rho_val)
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''T_{{t}} = \\frac{{{Fp:.8g} \\times {d2_new:.8g}}}{{2}} \\times \\tan({phi_deg:.8g}^\\circ + {rho_val_deg:.8g}^\\circ)''')
    Tt = (Fp * d2_new) / 2 * np.tan(fi_new + rho_val)
    st.write("**Izračunata vrednost Tₜ :**")
    st.latex(f'''T_{{t}} = {Tt:.8g} \\text{{ Nmm}}''')

    # Izračunavanje napona smicanja τ
    st.write("**Izračunavanje napona smicanja τ:**")
    st.latex('''\\tau = \\frac{T_{t}}{W_{p}}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\tau = \\frac{{{Tt:.8g}}}{{{Wp:.8g}}}''')
    tau = Tt / Wp
    st.write("**Izračunata vrednost τ:**")
    st.latex(f'''\\tau = {tau:.8g} \\text{{ N/mm²}}''')
    S_tau = tauT / tau
    st.write("**Izračunat koeficijent sigurnosti Sτ:**")
    st.latex(f'''S_τ = \\frac{{\\tau_{{t}}}}{{\\tau}} = \\frac{{200}}{{{tau:.8g}}} = {S_tau:.8g}''')

    # Ukupni koeficijent sigurnosti
    st.write("**Ukupni koeficijent sigurnosti S:**")
    st.latex('''S = \\frac{S_{\\sigma} \\times S_{\\tau}}{\\sqrt{S_{\\sigma}^2 + S_{\\tau}^2}}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''S = \\frac{{{S_sigma:.8g} \\times {S_tau:.8g}}}{{\\sqrt{{{S_sigma:.8g}^2 + {S_tau:.8g}^2}}}}''')
    S_total = (S_sigma * S_tau) / np.sqrt(S_sigma ** 2 + S_tau ** 2)
    st.write("**Izračunata vrednost S:**")
    st.latex(f'''S = {S_total:.8g}''')
    st.info("Veće od **S_min = 1.25 – 2.5** (Dodati komentar)")

    # Tačka 2.2
    st.subheader("Tačka 2.2")
    st.write("**Izračunavanje sile Fz:**")
    st.latex('''F_{z} = F_{p} + \\frac{1}{6} \\times F_{r}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''F_{{z}} = {Fp:.8g} + \\frac{{1}}{{6}} \\times {Fr:.8g}''')
    Fz = Fp + (1 / 6) * Fr
    st.write("**Izračunata vrednost Fz:**")
    st.latex(f'''F_{{z}} = {Fz:.8g} \\text{{ N}}''')

    st.write("**Izračunavanje napona zatezanja σ:**")
    st.latex('''\\sigma = \\frac{F_{z}}{A_{s}}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\sigma = \\frac{{{Fz:.8g}}}{{{As:.8g}}}''')
    sigma = Fz / As
    st.write("**Izračunata vrednost σ:**")
    st.latex(f'''\\sigma = {sigma:.8g} \\text{{ N/mm²}}''')

    S_sigma = Reh / sigma
    st.write("**Izračunat koeficijent sigurnosti Sσ:**")
    st.latex(f'''S_σ = \\frac{{R_{{eH}}}}{{\\sigma}} = \\frac{{300}}{{{sigma:.8g}}} = {S_sigma:.8g}''')
    st.info("Veće od **S_min = 1.25 – 2.5** (dodati komentar)")

    # Tačka 2.3
    st.subheader("Tačka 2.3")
    st.write("**Izračunavanje amplitude sile Fₐ:**")
    st.latex('''F_{a} = \\frac{F_{z} - F_{p}}{2}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''F_{{a}} = \\frac{{{Fz:.8g} - {Fp:.8g}}}{{2}}''')
    Fa = (Fz - Fp) / 2
    st.write("**Izračunata vrednost Fₐ:**")
    st.latex(f'''F_{{a}} = {Fa:.8g} \\text{{ N}}''')

    st.write("**Izračunavanje amplitudnog napona σₐ:**")
    st.latex('''\\sigma_{a} = \\frac{F_{a}}{A_{s}}''')
    st.write("**Sa unetim vrednostima:**")
    st.latex(f'''\\sigma_{{a}} = \\frac{{{Fa:.8g}}}{{{As:.8g}}}''')
    sigma_a = Fa / As
    st.write("**Izračunata vrednost σₐ:**")
    st.latex(f'''\\sigma_{{a}} = {sigma_a:.8g} \\text{{ N/mm²}}''')

    S_a = SigmaAM / sigma_a
    st.write("**Izračunat koeficijent sigurnosti Sₐ:**")
    st.latex(f'''S_a = \\frac{{\\sigma_{{AM}}}}{{\\sigma_{{a}}}} = \\frac{{50}}{{{sigma_a:.8g}}} = {S_a:.8g}''')
    st.info("Veće od **S_min = 1.25 – 2.5** (Dodati komentar)")
def tacka4():
    # ===================================
    # Tačka 4
    # ===================================
    st.markdown('<a id="tacka4"></a>', unsafe_allow_html=True)
    st.header("Tačka 4")

    # Odabir pogonskog elektromotora
    st.subheader("Odabir pogonskog elektromotora")

    # Unos vrednosti
    Vnv = st.number_input("Unesite brzinu pomeraja navrtke Vₙᵥ (mm/s):", value=30.0, format="%.8g", key="Vnv_t4")
    P = st.number_input("Unesite korak navoja P (mm):", value=5.0, format="%.8g", key="P_t4")
    Trm = st.number_input("Unesite vrednost Tᵣₘ (Nm):", value=80.0, format="%.8g", key="Trm_t4")
    nem = st.number_input("Unesite vrednost nₑₘ (min⁻¹):", value=1450.0, format="%.8g", key="nem_t4")
    z1 = st.number_input("Unesite vrednost z₁ = z₃:", value=19, format="%.8g", key="z1_t4")
    z3 = z1
    z2 = st.number_input("Unesite vrednost z₂:", value=38, format="%.8g", key="z2_t4")
    z4 = st.number_input("Unesite vrednost z₄:", value=23, format="%.8g", key="z4_t4")
    z5 = st.number_input("Unesite vrednost z₅:", value=38, format="%.8g", key="z5_t4")
    z6 = st.number_input("Unesite vrednost z₆:", value=20, format="%.8g", key="z6_t4")
    z7 = st.number_input("Unesite vrednost z₇:", value=39, format="%.8g", key="z7_t4")
    eta_z = st.number_input("Unesite vrednost η_z:", value=0.99, format="%.8g", key="eta_z_t4")

    # Odabir kaišnog para
    st.subheader("Odabir kaišnog para")
    kaisni_par = st.selectbox("Izaberite kaišni par:", ("Trapezni - normalni/uski", "Zupčasti", "Višeprofilni"), key="kaisni_par_t4")

    if kaisni_par == "Trapezni - normalni/uski":
        Uk12 = st.number_input("Unesite vrednost Uₖ₁₂:", value=1.0, format="%.8g", key="Uk12_t4")
        xi_p = st.number_input("Unesite vrednost ξₚ:", value=0.985, format="%.8g", key="xi_p_t4")
        eta_k = st.number_input("Unesite vrednost ηₖ:", value=0.97, format="%.8g", key="eta_k_t4")

        # Izračunavanje nᵣₘ
        nrm = nem / ((Uk12 / xi_p) * (z2 / z1) * (z3 / z2) * (z7 / z6))
        st.write("**Izračunavanje nᵣₘ:**")
        st.latex(
            f'''
            n_{{rm}} = \\frac{{n_{{em}}}}{{\\left(\\dfrac{{U_{{k12}}}}{{\\xi_{{p}}}}\\right) \\times \\dfrac{{z_{{2}}}}{{z_{{1}}}} \\times \\dfrac{{z_{{3}}}}{{z_{{2}}}} \\times \\dfrac{{z_{{7}}}}{{z_{{6}}}}}} = 
            \\frac{{{nem:.8g}}}{{\\left(\\dfrac{{{Uk12:.8g}}}{{{xi_p:.8g}}}\\right) \\times \\dfrac{{{z2:.8g}}}{{{z1:.8g}}} \\times \\dfrac{{{z3:.8g}}}{{{z2:.8g}}} \\times \\dfrac{{{z7:.8g}}}{{{z6:.8g}}}}} = {nrm:.8g} \\text{{ min}}^{{-1}}
            '''
        )

    elif kaisni_par == "Zupčasti":
        ik12 = st.number_input("Unesite vrednost iₖ₁₂:", value=2.1, format="%.8g", key="ik12_t4")
        eta_k = st.number_input("Unesite vrednost ηₖ:", value=0.985, format="%.8g", key="eta_k_t4")

        # Izračunavanje nᵣₘ
        nrm = nem / (ik12 * (z2 / z1) * (z3 / z2) * (z7 / z6))
        st.write("**Izračunavanje nᵣₘ:**")
        st.latex(
            f'''
            n_{{rm}} = \\frac{{n_{{em}}}}{{i_{{k12}} \\times \\dfrac{{z_{{2}}}}{{z_{{1}}}} \\times \\dfrac{{z_{{3}}}}{{z_{{2}}}} \\times \\dfrac{{z_{{7}}}}{{z_{{6}}}}}} = 
            \\frac{{{nem:.8g}}}{{{ik12:.8g} \\times \\dfrac{{{z2:.8g}}}{{{z1:.8g}}} \\times \\dfrac{{{z3:.8g}}}{{{z2:.8g}}} \\times \\dfrac{{{z7:.8g}}}{{{z6:.8g}}}}} = {nrm:.8g} \\text{{ min}}^{{-1}}
            '''
        )

    elif kaisni_par == "Višeprofilni":
        Uk12 = st.number_input("Unesite vrednost Uₖ₁₂:", value=1.0, format="%.8g", key="Uk12_t4")
        xi_p = st.number_input("Unesite vrednost ξₚ:", value=0.99, format="%.8g", key="xi_p_t4")
        eta_k = st.number_input("Unesite vrednost ηₖ:", value=0.98, format="%.8g", key="eta_k_t4")

        # Izračunavanje nᵣₘ
        nrm = nem / ((Uk12 / xi_p) * (z2 / z1) * (z3 / z2) * (z7 / z6))
        st.write("**Izračunavanje nᵣₘ:**")
        st.latex(
            f'''
            n_{{rm}} = \\frac{{n_{{em}}}}{{\\left(\\dfrac{{U_{{k12}}}}{{\\xi_{{p}}}}\\right) \\times \\dfrac{{z_{{2}}}}{{z_{{1}}}} \\times \\dfrac{{z_{{3}}}}{{z_{{2}}}} \\times \\dfrac{{z_{{7}}}}{{z_{{6}}}}}} = 
            \\frac{{{nem:.8g}}}{{\\left(\\dfrac{{{Uk12:.8g}}}{{{xi_p:.8g}}}\\right) \\times \\dfrac{{{z2:.8g}}}{{{z1:.8g}}} \\times \\dfrac{{{z3:.8g}}}{{{z2:.8g}}} \\times \\dfrac{{{z7:.8g}}}{{{z6:.8g}}}}} = {nrm:.8g} \\text{{ min}}^{{-1}}
            '''
        )

    # Izračunavanje Pₙᵥ
    Fnv = F / 1000  # Pretvaranje F u kN
    Vnv_m_s = Vnv / 1000  # Pretvaranje Vₙᵥ u m/s
    Pnv = Fnv * Vnv_m_s
    st.write("**Izračunavanje Pₙᵥ:**")
    st.latex(
        f'''
        P_{{nv}} = F_{{nv}} \\times V_{{nv}} = {Fnv:.8g} \\times {Vnv_m_s:.8g} = {Pnv:.8g} \\text{{ kW}}
        '''
    )

    # Izračunavanje Pᵣₘ
    Prm = (Trm * nrm) / 9550
    st.write("**Izračunavanje Pᵣₘ:**")
    st.latex(
        f'''
        P_{{rm}} = \\frac{{T_{{rm}} \\times n_{{rm}}}}{{9550}} = \\frac{{{Trm:.8g} \\times {nrm:.8g}}}{{9550}} = {Prm:.8g} \\text{{ kW}}
        '''
    )

    # Izračunavanje Pₑₘ
    Pem = (Pnv) / (eta_k * eta_z ** 2) + (Prm) / (eta_k * eta_z ** 3)
    st.write("**Izračunavanje Pₑₘ:**")
    st.latex(
        f'''
        P_{{em}} = \\frac{{P_{{nv}}}}{{\\eta_{{k}} \\times \\eta_{{z}}^2}} + \\frac{{P_{{rm}}}}{{\\eta_{{k}} \\times \\eta_{{z}}^3}} = 
        \\frac{{{Pnv:.8g}}}{{{eta_k:.8g} \\times {eta_z:.8g}^2}} + \\frac{{{Prm:.8g}}}{{{eta_k:.8g} \\times {eta_z:.8g}^3}} = {Pem:.8g} \\text{{ kW}}
        '''
    )
    st.info("Sada treba izabrati motor iz tabele i izvuci parametre Pem i nem. npr za pocetne podatke (zupcasti) usvaja se 2.ZK 112 M-4")
    novo_nem = st.number_input("Unesite novu vrednost nₑₘ (min⁻¹):", value=1450.0, format="%.8g", key="nem_t4_new")

    if kaisni_par == "Zupčasti":
        i12 = z2 / z1
        z5_display = (P * novo_nem * z4) / (60 * Vnv * ik12 * i12)
        st.write("**Izračunavanje Z₅:**")
        st.latex(
            f'''
            Z_{{5}} = \\frac{{P \\times n_{{em}} \\times z_{{4}}}}{{60 \\times V_{{nv}} \\times i_{{k12}} \\times i_{{12}}}} = 
            \\frac{{{P:.8g} \\times {nem:.8g} \\times {z4:.8g}}}{{60 \\times {Vnv:.8g} \\times {ik12:.8g} \\times {i12:.8g}}} = {z5_display:.8g}
            '''
        )
    else:
        i12 = z2 / z1
        i56 = z6 / z5
        ik12_display = (P * novo_nem) / (60 * Vnv * i12 * i56)
        st.write("**Izračunavanje iₖ₁₂:**")
        st.latex(
            f'''
            i_{{k12}} = \\frac{{P \\times n_{{em}}}}{{60 \\times V_{{nv}} \\times i_{{12}} \\times i_{{56}}}} = 
            \\frac{{{P:.8g} \\times {nem:.8g}}}{{60 \\times {Vnv:.8g} \\times {i12:.8g} \\times {i56:.8g}}} = {ik12_display:.8g}
            '''
        )
def tacka5 ():
    st.markdown('<a id="tacka5"></a>', unsafe_allow_html=True)
    st.title("Tačka 5")

# Poziv funkcija
nulta_tacka()
tacka1()
tacka2()
tacka4()
tacka5()