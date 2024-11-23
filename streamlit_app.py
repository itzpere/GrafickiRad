import streamlit as st
import numpy as np
import pandas as pd

st.title("Proračun navojnog vretena")
st.info("Ovaj program služi za izračunavanje prvih 3 tačaka grafičkog rada. Idalje treba pratiti uputstvo radi pravilnog ispisivanja na papiru.")

# ===================================
# Nulta tačka 0
# ===================================
st.header("Nulta tačka 0")

mnv = st.selectbox("Izaberite materijal navojnog vretena (mnv):", ["E335", "E295"])
F = st.number_input("Unesite silu F (N):", value=10000.0, format="%.6f")

# Podesavanje σ_D0 i τ_D0 u zavisnosti od materijala
if mnv == "E335":
    sigmaD0 = 360
    tauD0 = 215
else:
    sigmaD0 = 310
    tauD0 = 205

st.write("**Dozvoljeni napon zatezanja:**")
st.latex(f'''\\sigma_{{D0}} = {sigmaD0} \\, \\text{{N/mm}}^2''')
st.write("**Dozvoljeni napon smicanja:**")
st.latex(f'''\\tau_{{D0}} = {tauD0} \\, \\text{{N/mm}}^2''')

st.write("**Formula za A₃:**")
st.latex(r'''A_3 = \frac{1.3 \cdot F \cdot 2.5}{\sigma_{D0}}''')

# Izračunavanje A₃
A3 = (1.3 * F * 2.5) / sigmaD0
st.write(f"**A₃ = {A3:.6f} mm²**")

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

h = st.number_input("Unesite visinu h (mm):", value=400.0, format="%.6f")

st.write("**Formula za d₃:**")
st.latex(r'''d_3 = \sqrt[4]{ \frac{64 \cdot F \cdot S \cdot h^2}{\pi^3 \cdot E}}''')

# Izračunavanje d₃
d3 = ((64 * F * S * h ** 2) / (np.pi ** 3 * E)) ** (1 / 4)
st.write(f"**d₃ ≥ {d3:.6f} mm**")
st.info("Uzmi prvi veći prečnik iz tabele 3.2")

# ===================================
# Nulta tačka 2
# ===================================
st.header("Nulta tačka 2")

d = st.number_input("Unesite prečnik navoja d (mm):", value=24.0, format="%.6f")
P = st.number_input("Unesite korak navoja P (mm):", value=5.0, format="%.6f")
d2 = st.number_input("Unesite srednji prečnik navoja d₂ (mm):", value=21.5, format="%.6f")

H1 = P / 2
st.write(f"**H₁ = {H1:.6f} mm**")

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
st.header("Unesite parametre za dalji proračun")

d = st.number_input("Ponovo unesite prečnik navoja d (mm):", value=d, format="%.6f")
P = st.number_input("Ponovo unesite korak navoja P (mm):", value=P, format="%.6f")
d2 = st.number_input("Ponovo unesite srednji prečnik navoja d₂ (mm):", value=d2, format="%.6f")
d3 = st.number_input("Unesite prečnik d₃ (mm):", value=d3, format="%.6f")
A3 = st.number_input("Unesite površinu A₃ (mm²):", value=A3, format="%.6f")
Ln = st.number_input("Unesite dužinu navoja Lₙ (mm):", value=results[0]['L_n [mm]'] if results else 1, format="%.6f")

# ===================================
# Nulta tačka 3
# ===================================
st.header("Nulta tačka 3")

st.write("**Formula za ϕ:**")
st.latex(r'''\varphi = \arctan\left( \frac{P}{\pi \cdot d_2} \right)''')

fi = np.arctan(P / (d2 * np.pi))
st.write(f"**ϕ = {np.degrees(fi):.6f}°**")

st.write("**Postavljena vrednost faktora trenja f:**")
f = 0.09
st.write(f"**f = {f}**")

st.write("**Formula za ρ:**")
st.latex(r'''\rho = \arctan\left( \frac{f}{\cos 15^\circ} \right)''')
rho = np.arctan(f / np.cos(np.radians(15)))
st.write(f"**ρ = {np.degrees(rho):.6f}°**")

st.write("**Formula za Tₙₚ:**")
st.latex(r'''T_{np} = \frac{F \cdot d_2}{2} \cdot \tan(\varphi + \rho)''')
Tnp = (F * d2) / 2 * np.tan(fi + rho)
st.write(f"**Tₙₚ = {Tnp:.6f} N·mm**")

# ===================================
# Tačka 1.1
# ===================================
st.header("Tačka 1.1")

st.write("**Formula za σ:**")
st.latex(r'''\sigma = \frac{F}{A_3}''')
sigma = F / A3
st.write(f"**σ = {sigma:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za zatezanje:**")
st.latex(r'''S_{\sigma} = \frac{\sigma_{D0}}{\sigma}''')
S_sigma = sigmaD0 / sigma
st.write(f"**S_σ = {S_sigma:.6f}**")

st.write("**Formula za τ:**")
st.latex(r'''\tau = \frac{T_{np}}{0.2 \cdot d_3^3}''')
tau = Tnp / (0.2 * d3 ** 3)
st.write(f"**τ = {tau:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za smicanje:**")
st.latex(r'''S_{\tau} = \frac{\tau_{D0}}{\tau}''')
S_tau = tauD0 / tau
st.write(f"**S_τ = {S_tau:.6f}**")

st.write("**Ukupni koeficijent sigurnosti:**")
st.latex(r'''S = \frac{S_{\sigma} \cdot S_{\tau}}{\sqrt{S_{\sigma}^2 + S_{\tau}^2}}''')
S_total = (S_sigma * S_tau) / np.sqrt(S_sigma ** 2 + S_tau ** 2)
st.write(f"**Ukupni koeficijent sigurnosti S = {S_total:.6f}**")
st.info("Treba da bude veće od **Smin = 1.5 – 2** + komentar")

# ===================================
# Tačka 1.2
# ===================================
st.header("Tačka 1.2")

st.write("**Postavljena vrednost Bₗ:**")
Bl = st.number_input("Unesite vrednost Bₗ (mm):", value=19.0, format="%.6f")
st.write(f"**Bₗ = {Bl} mm**")

i = d3 / 4
st.write(f"**i = {i:.6f} mm**")

st.write("**Formula za Lₖ:**")
st.latex(r'''L_k = \frac{L_n}{2} + h + 10 + \frac{B_l}{2}''')
Lk = (Ln / 2) + h + 10 + (Bl / 2)
st.write(f"**Lₖ = {Lk:.6f} mm**")

st.write("**Formula za λ (lambda):**")
st.latex(r'''\lambda = \frac{L_k}{i}''')
lamda = Lk / i
st.write(f"**λ = {lamda:.6f}**")

if lamda <= 89:
    st.info("Za **σₖ** koristi se Tetmajerov obrazac zato što je λ < 89")
    st.latex(r'''\sigma_K = 335 - 0.62 \cdot \lambda''')
    sigmaK = 335 - 0.62 * lamda
    st.write(f"**σₖ = {sigmaK:.6f} N/mm²**")
else:
    st.info("Za **σₖ** koristi se Ojlerov obrazac zato što je λ ≥ 89")
    st.latex(r'''\sigma_K = \frac{E \cdot \pi^2}{\lambda^2}''')
    sigmaK = (E * np.pi ** 2) / (lamda ** 2)
    st.write(f"**σₖ = {sigmaK:.6f} N/mm²**")

st.write("**Izračunavanje σᵢ:**")
st.latex(r'''\sigma_i = \sqrt{\sigma^2 + 3 \tau^2}''')
sigma_i = np.sqrt(sigma ** 2 + 3 * tau ** 2)
st.write(f"**σᵢ = {sigma_i:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti Sᵢ:**")
st.latex(r'''S_i = \frac{\sigma_K}{\sigma_i}''')
S_i = sigmaK / sigma_i
st.write(f"**Sᵢ = {S_i:.6f}**")

# ===================================
# Tačka 1.3
# ===================================
st.header("Tačka 1.3")

st.write("**Formula za p:**")
st.latex(r'''p = \frac{F \cdot P}{L_n \cdot d_2 \cdot \pi \cdot H_1}''')
p = (F * P) / (Ln * d2 * np.pi * H1)
st.write(f"**p = {p:.6f} N/mm²**")
if 10 <= p <= 20:
    st.success("Rezultat zadovoljava uslov (**10 ≤ p ≤ 20**)")
else:
    st.warning("Rezultat ne zadovoljava uslov")
st.info("Ovo je provera nulte tačke i treba napisati komentar")

# ===================================
# Tačka 1.4
# ===================================
st.header("Tačka 1.4")

st.write("**Formula za ηₙₚ:**")
st.latex(r'''\eta_{np} = \frac{\tan \varphi}{\tan (\varphi + \rho)}''')
eta_np = np.tan(fi) / np.tan(fi + rho)
st.write(f"**ηₙₚ = {eta_np:.6f}**")

st.write("**Formula za ηₙᵥ:**")
st.latex(r'''\eta_{nv} = 0.9 \cdot \eta_{np}''')
eta_nv = 0.9 * eta_np
st.write(f"**ηₙᵥ = {eta_nv:.6f}**")

# ===================================
# Tačka 1.5
# ===================================
st.header("Tačka 1.5")

if fi > rho:
    st.warning("**Navoj nije samokočiv**")
else:
    st.success("**Navoj je samokočiv**")

# ===================================
# Tačka 2
# ===================================
st.header("Tačka 2")

z = st.number_input("Unesite broj z:", value=4.0, format="%.6f")
st.write(f"**z = {z}**")

Reh = st.number_input("Unesite vrednost RₑH (N/mm²) iz tabele 3.5:", value=300.0, format="%.6f")
st.write(f"**RₑH = {Reh} N/mm²**")

st.write("**Formula za Fᵣ:**")
st.latex(r'''F_r = \frac{F}{z}''')
Fr = F / z
st.write(f"**Fᵣ = {Fr:.6f} N**")

st.write("**Formula za Fₚ:**")
st.latex(r'''F_p = 3 \cdot F_r''')
Fp = 3 * Fr
st.write(f"**Fₚ = {Fp:.6f} N**")

st.write("**Formula za Aₛ:**")
st.latex(r'''A_s = \frac{F_p}{0.6 \cdot R_{eH}}''')
As = Fp / (0.6 * Reh)
st.write(f"**Aₛ = {As:.6f} mm²**")

st.write("**Provera:**")
Fp_check = 0.6 * As * Reh
st.write(f"Fₚ = 0.6 × Aₛ × RₑH = **{Fp_check:.6f} N**")

# ===================================
# Tačka 2.1
# ===================================
st.header("Tačka 2.1")

st.write("**Postavljena vrednost dozvoljenog napona smicanja τₜ:**")
tauT = st.number_input("Unesite dozvoljeni napon smicanja τₜ (N/mm²):", value=200.0, format="%.6f")
st.write(f"**τₜ = {tauT} N/mm²**")

st.write("**Postavljena vrednost dozvoljenog amplitudnog napona σ_Aₘ:**")
SigmaAM = st.number_input("Unesite dozvoljeni amplitudni napon σ_Aₘ (N/mm²):", value=50.0, format="%.6f")
st.write(f"**σ_Aₘ = {SigmaAM} N/mm²**")

st.write("**Formula za σ:**")
st.latex(r'''\sigma = \frac{F_p}{A_s}''')
sigma = Fp / As
st.write(f"**σ = {sigma:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za zatezanje:**")
st.latex(r'''S_{\sigma} = \frac{R_{eH}}{\sigma}''')
S_sigma = Reh / sigma
st.write(f"**S_σ = {S_sigma:.6f}**")

st.write("**Postavljena vrednost faktora trenja f:**")
f_val = 0.15
st.write(f"**f = {f_val}**")

st.write("**Formula za ρ (rho):**")
st.latex(r'''\rho = \arctan\left( \frac{f}{\cos 30^\circ} \right)''')
rho_val = np.arctan(f_val / np.cos(np.radians(30)))
st.write(f"**ρ = {np.degrees(rho_val):.6f}°**")

st.write("**Formula za Wₚ:**")
st.latex(r'''W_p = 0.2 \cdot \left( \frac{d_2 + d_3}{2} \right)^3''')
Wp = 0.2 * ((d2 + d3) / 2) ** 3
st.write(f"**Wₚ = {Wp:.6f} mm³**")

st.write("**Formula za Tₜ:**")
st.latex(r'''T_t = \frac{F_p \cdot d_2}{2} \cdot \tan (\varphi + \rho)''')
Tt = (Fp * d2) / 2 * np.tan(fi + rho_val)
st.write(f"**Tₜ = {Tt:.6f} N·mm**")

st.write("**Formula za τ:**")
st.latex(r'''\tau = \frac{T_t}{W_p}''')
tau = Tt / Wp
st.write(f"**τ = {tau:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za smicanje:**")
st.latex(r'''S_{\tau} = \frac{\tau_T}{\tau}''')
S_tau = tauT / tau
st.write(f"**S_τ = {S_tau:.6f}**")

st.write("**Ukupni koeficijent sigurnosti:**")
st.latex(r'''S = \frac{S_{\sigma} \cdot S_{\tau}}{\sqrt{S_{\sigma}^2 + S_{\tau}^2}}''')
S_total = (S_sigma * S_tau) / np.sqrt(S_sigma ** 2 + S_tau ** 2)
st.write(f"**S = {S_total:.6f}**")
st.info("Veće od **Smin = 1.25 – 2.5** (proveriti) + komentar")

# ===================================
# Tabela 2.2
# ===================================
st.header("Tabela 2.2")

st.write("**Formula za F_z:**")
st.latex(r'''F_z = F_p + \frac{1}{6} F_r''')
Fz = Fp + (1 / 6) * Fr
st.write(f"**F_z = {Fz:.6f} N**")

st.write("**Formula za σ:**")
st.latex(r'''\sigma = \frac{F_z}{A_s}''')
sigma = Fz / As
st.write(f"**σ = {sigma:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za zatezanje:**")
st.latex(r'''S_{\sigma} = \frac{R_{eH}}{\sigma}''')
S_sigma = Reh / sigma
st.write(f"**S_σ = {S_sigma:.6f}**")
st.info("Veće od **Smin = 1.25 – 2.5** (proveriti) + komentar")

# ===================================
# Tabela 2.3
# ===================================
st.header("Tabela 2.3")

st.write("**Formula za Fₐ:**")
st.latex(r'''F_a = \frac{F_z - F_p}{2}''')
Fa = (Fz - Fp) / 2
st.write(f"**Fₐ = {Fa:.6f} N**")

st.write("**Formula za σₐ:**")
st.latex(r'''\sigma_a = \frac{F_a}{A_s}''')
sigma_a = Fa / As
st.write(f"**σₐ = {sigma_a:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za amplitudni napon:**")
st.latex(r'''S_a = \frac{\sigma_{AM}}{\sigma_a}''')
S_a = SigmaAM / sigma_a
st.write(f"**Sₐ = {S_a:.6f}**")
st.info("Veće od **Smin = 1.25 – 2.5** (proveriti) + komentar")