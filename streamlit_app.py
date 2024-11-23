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

# Podešavanje sigmaD0 i tauD0 u zavisnosti od materijala
if mnv == "E335":
    sigmaD0 = 360
    tauD0 = 215
else:
    sigmaD0 = 310
    tauD0 = 205

st.write(f"**sigmaD0 = {sigmaD0} N/mm²**")
st.write(f"**tauD0 = {tauD0} N/mm²**")

# Konstante za A3
k1 = 1.3
k2 = 2.5
st.write(f"**Konstante:** k1 = {k1}, k2 = {k2}")

st.write("**Formula za A3:**")
st.latex(r'''A3 = \frac{k1 \cdot F \cdot k2}{\sigma_{D0}}''')

# Izračunavanje A3
A3 = (k1 * F * k2) / sigmaD0
st.write(f"**A3 = {A3:.6f} mm²**")

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
S = 7       # Koeficijent sigurnosti
st.write(f"**E = {E} N/mm²**")
st.write(f"**S = {S}**")

h = st.number_input("Unesite visinu h (mm):", value=400.0, format="%.6f")

st.write("**Formula za d3:**")
st.latex(r'''d3 = \sqrt[4]{ \frac{64 \cdot F \cdot S \cdot h^2}{\pi^3 \cdot E}}''')

# Izračunavanje d3
d3 = ((64 * F * S * h ** 2) / (np.pi ** 3 * E)) ** (1 / 4)
st.write(f"**d3 ≥ {d3:.6f} mm**")
st.info("Uzmi prvi veći prečnik iz tabele 3.2")

# ===================================
# Nulta tačka 2
# ===================================
st.header("Nulta tačka 2")

d = st.number_input("Unesite prečnik navoja d (mm):", value=24.0, format="%.6f")
P = st.number_input("Unesite korak navoja P (mm):", value=5.0, format="%.6f")
d2 = st.number_input("Unesite srednji prečnik navoja d2 (mm):", value=21.5, format="%.6f")

H1 = P / 2
st.write(f"**H1 = {H1} mm**")

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
        'pdoz [N/mm²]': pdoz,
        'Zn pre': round(Zn_pre, 6),
        'Zn': Zn,
        'Ln [mm]': round(Ln, 6),
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
# Unos dodatnih parametara
# ===================================
st.header("Unesite parametre za dalji proračun")

st.write("**Unete vrednosti:**")
st.write(f"Prečnik navoja d = {d} mm")
st.write(f"Korak navoja P = {P} mm")
st.write(f"Srednji prečnik navoja d2 = {d2} mm")

# Unos d3, A3 i Ln
d3 = st.number_input("Unesite prečnik d3 (mm):", value=d3, format="%.6f")
A3 = st.number_input("Unesite površinu A3 (mm²):", value=A3, format="%.6f")
Ln = st.number_input("Unesite dužinu navoja Ln (mm):", value=results[0]['Ln [mm]'] if results else 1, format="%.6f")

# ===================================
# Nulta tačka 3
# ===================================
st.header("Nulta tačka 3")

st.write("**Formula za ϕ:**")
st.latex(r'''\varphi = \arctan\left( \frac{P}{\pi \cdot d2} \right)''')

fi = np.arctan(P / (d2 * np.pi))
st.write(f"**ϕ = {np.degrees(fi):.6f}°**")

# Konstante za ρ
f = 0.09
angle = 15
st.write(f"**Konstante:** f = {f}, ugao = {angle}°")

st.write("**Formula za ρ:**")
st.latex(r'''\rho = \arctan\left( \frac{f}{\cos 15^\circ} \right)''')
Ron = np.arctan(f / np.cos(np.radians(angle)))
st.write(f"**ρ = {np.degrees(Ron):.6f}°**")

st.write("**Formula za Tnp:**")
st.latex(r'''T_{np} = \frac{F \cdot d2}{2} \cdot \tan(\varphi + \rho)''')
Tnp = (F * d2) / 2 * np.tan(fi + Ron)
st.write(f"**Tnp = {Tnp:.6f} N·mm**")

# ===================================
# Tačka 1.1
# ===================================
st.header("Tačka 1.1")

st.write("**Formula za σ:**")
st.latex(r'''\sigma = \frac{F}{A3}''')
sigma = F / A3
st.write(f"**σ = {sigma:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za zatezanje:**")
st.latex(r'''S_{\sigma} = \frac{\sigma_{D0}}{\sigma}''')
Ssigma = sigmaD0 / sigma
st.write(f"**Sσ = {Ssigma:.6f}**")

# Konstanta k3
k3 = 0.2
st.write(f"**Konstanta:** k3 = {k3}")

st.write("**Formula za τ:**")
st.latex(r'''\tau = \frac{T_{np}}{k3 \cdot d3^3}''')
tau = Tnp / (k3 * d3 ** 3)
st.write(f"**τ = {tau:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za smicanje:**")
st.latex(r'''S_{\tau} = \frac{\tau_{D0}}{\tau}''')
Stau = tauD0 / tau
st.write(f"**Sτ = {Stau:.6f}**")

st.write("**Ukupni koeficijent sigurnosti:**")
st.latex(r'''S = \frac{S_{\sigma} \cdot S_{\tau}}{\sqrt{S_{\sigma}^2 + S_{\tau}^2}}''')
S_total = (Ssigma * Stau) / np.sqrt(Ssigma ** 2 + Stau ** 2)
st.write(f"**Ukupni koeficijent sigurnosti S = {S_total:.6f}**")
st.info("Treba da bude veće od **Smin = 1.5 – 2** + komentar")

# ===================================
# Tačka 1.2
# ===================================
st.header("Tačka 1.2")

st.info("Bl je vrednost koja se uzima iz kataloga na stranici predmeta nazvanim 'dvoredni ležajevi'. U slučaju da je d = 24 uzima se sledeći veći tj. 25 i Bl je 19.")

Bl = st.number_input("Unesite vrednost Bl (mm):", value=19.0, format="%.6f")
i = d3 / 4
st.write(f"**i = d3 / 4 = {i:.6f} mm**")

# Konstanta k4
k4 = 10
st.write(f"**Konstanta:** k4 = {k4} mm")

st.write("**Formula za Lk:**")
st.latex(r'''L_k = \frac{L_n}{2} + h + k4 + \frac{B_l}{2}''')
lk = (Ln / 2) + h + k4 + (Bl / 2)
st.write(f"**Lk = {lk:.6f} mm**")

st.write("**Formula za λ (lambda):**")
st.latex(r'''\lambda = \frac{L_k}{i}''')
lamda = lk / i
st.write(f"**λ = {lamda:.6f}**")

# Modul elastičnosti E is already defined
if lamda <= 89:
    st.info("Za **σK** koristi se Tetmajerov obrazac zato što je λ < 89")
    # Konstante k5 i k6
    k5 = 335
    k6 = 0.62
    st.write(f"**Konstante:** k5 = {k5}, k6 = {k6}")
    st.latex(r'''\sigma_K = k5 - k6 \cdot \lambda''')
    sigmaK = k5 - k6 * lamda
    st.write(f"**σK = {sigmaK:.6f} N/mm²**")
    st.info("**Si** treba biti veće **2 – 4** + komentar")
else:
    st.info("Za **σK** koristi se Ojlerov obrazac zato što je λ ≥ 89")
    st.latex(r'''\sigma_K = \frac{E \cdot \pi^2}{\lambda^2}''')
    sigmaK = (E * np.pi ** 2) / (lamda ** 2)
    st.write(f"**σK = {sigmaK:.6f} N/mm²**")
    st.info("**Si** treba biti veće **3 – 6** + komentar")

st.write("**Izračunavanje σi:**")
st.latex(r'''\sigma_i = \sqrt{\sigma^2 + 3 \tau^2}''')
sigmai = np.sqrt(sigma ** 2 + 3 * tau ** 2)
st.write(f"**σi = {sigmai:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti Si:**")
st.latex(r'''S_i = \frac{\sigma_K}{\sigma_i}''')
Si = sigmaK / sigmai
st.write(f"**Si = {Si:.6f}**")

# ===================================
# Tačka 1.3
# ===================================
st.header("Tačka 1.3")

st.write("**Formula za p:**")
st.latex(r'''p = \frac{F \cdot P}{L_n \cdot d2 \cdot \pi \cdot H1}''')
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

st.write("**Formula za ηnp:**")
st.latex(r'''\eta_{np} = \frac{\tan \varphi}{\tan (\varphi + \rho)}''')
eta_np = np.tan(fi) / np.tan(fi + Ron)
st.write(f"**ηnp = {eta_np:.6f}**")

# Konstanta k7
k7 = 0.9
st.write(f"**Konstanta:** k7 = {k7}")

st.write("**Formula za ηnv:**")
st.latex(r'''\eta_{nv} = k7 \cdot \eta_{np}''')
eta_nv = k7 * eta_np
st.write(f"**ηnv = {eta_nv:.6f}**")

# ===================================
# Tačka 1.5
# ===================================
st.header("Tačka 1.5")

if fi > Ron:
    st.warning("**Navoj nije samokočiv**")
else:
    st.success("**Navoj je samokočiv**")

# ===================================
# Tačka 2
# ===================================
st.header("Tačka 2")

st.write(f"**Unete vrednosti:** F = {F} N, d2 = {d2} mm, P = {P} mm")
st.write(f"**ϕ = {np.degrees(fi):.6f}°**")

z = st.number_input("Unesite broj z:", value=4.0, format="%.6f")
Reh = st.number_input("Unesite vrednost ReH (N/mm²) iz tabele 3.5:", value=300.0, format="%.6f")

st.write("**Formula za Fr:**")
st.latex(r'''F_r = \frac{F}{z}''')
Fr = F / z
st.write(f"**Fr = {Fr:.6f} N**")

# Konstanta k8
k8 = 3
st.write(f"**Konstanta:** k8 = {k8}")
st.write("**Formula za Fp:**")
st.latex(r'''F_p = k8 \cdot F_r''')
Fp = k8 * Fr
st.write(f"**Fp = {Fp:.6f} N**")

# Konstanta k9
k9 = 0.6
st.write(f"**Konstanta:** k9 = {k9}")
st.write("**Formula za As:**")
st.latex(r'''A_s = \frac{F_p}{k9 \cdot R_{eH}}''')
As = Fp / (k9 * Reh)
st.write(f"**As = {As:.6f} mm²**")

st.write("**Provera:**")
Fp_check = k9 * As * Reh
st.write(f"Fp = {k9} × As × ReH = **{Fp_check:.6f} N**")

# ===================================
# Tačka 2.1
# ===================================
st.header("Tačka 2.1")

st.info("Vrednosti **τT** i **σAM** se dobijaju iz odgovarajućih tabela 3.5 i 3.6 i unose se ručno.")

tauT = st.number_input("Unesite dozvoljeni napon smicanja τT (N/mm²):", value=200.0, format="%.6f")
SigmaAM = st.number_input("Unesite dozvoljeni amplitudni napon σAM (N/mm²):", value=50.0, format="%.6f")

st.write("**Formula za σ:**")
st.latex(r'''\sigma = \frac{F_p}{A_s}''')
sigma = Fp / As
st.write(f"**σ = {sigma:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za zatezanje:**")
st.latex(r'''S_{\sigma} = \frac{R_{eH}}{\sigma}''')
Ssigma = Reh / sigma
st.write(f"**Sσ = {Ssigma:.6f}**")

# Konstante za ρ
f1 = 0.15
angle1 = 30
st.write(f"**Konstante:** f = {f1}, ugao = {angle1}°")

st.write("**Formula za ρ (rho):**")
st.latex(r'''\rho = \arctan\left( \frac{f}{\cos {angle1}^\circ} \right)''')
Ron_val = np.arctan(f1 / np.cos(np.radians(angle1)))
st.write(f"**ρ = {np.degrees(Ron_val):.6f}°**")

# Konstanta k10
k10 = 0.2
st.write(f"**Konstanta:** k10 = {k10}")
st.write("**Formula za Wp:**")
st.latex(r'''W_p = k10 \cdot \left( \frac{d2 + d3}{2} \right)^3''')
Wp = k10 * ((d2 + d3) / 2) ** 3
st.write(f"**Wp = {Wp:.6f} mm³**")

st.write("**Formula za Tt:**")
st.latex(r'''T_t = \frac{F_p \cdot d2}{2} \cdot \tan (\varphi + \rho)''')
Tt = (Fp * d2) / 2 * np.tan(fi + Ron_val)
st.write(f"**Tt = {Tt:.6f} N·mm**")

st.write("**Formula za τ:**")
st.latex(r'''\tau = \frac{T_t}{W_p}''')
tau = Tt / Wp
st.write(f"**τ = {tau:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za smicanje:**")
st.latex(r'''S_{\tau} = \frac{\tau_T}{\tau}''')
Stau = tauT / tau
st.write(f"**Sτ = {Stau:.6f}**")

st.write("**Ukupni koeficijent sigurnosti:**")
st.latex(r'''S = \frac{S_{\sigma} \cdot S_{\tau}}{\sqrt{S_{\sigma}^2 + S_{\tau}^2}}''')
S_total = (Ssigma * Stau) / np.sqrt(Ssigma ** 2 + Stau ** 2)
st.write(f"**S = {S_total:.6f}**")
st.info("Veće od **Smin = 1.25 – 2.5** (proveriti) + komentar")

# ===================================
# Tabela 2.2
# ===================================
st.header("Tabela 2.2")

# Konstanta k11
k11 = 1/6
st.write(f"**Konstanta:** k11 = {k11}")
st.write("**Formula za Fz:**")
st.latex(r'''F_z = F_p + k11 \cdot F_r''')
Fz = Fp + k11 * Fr
st.write(f"**Fz = {Fz:.6f} N**")

st.write("**Formula za σ:**")
st.latex(r'''\sigma = \frac{F_z}{A_s}''')
sigma = Fz / As
st.write(f"**σ = {sigma:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za zatezanje:**")
st.latex(r'''S_{\sigma} = \frac{R_{eH}}{\sigma}''')
Ssigma = Reh / sigma
st.write(f"**Sσ = {Ssigma:.6f}**")
st.info("Veće od **Smin = 1.25 – 2.5** (proveriti) + komentar")

# ===================================
# Tabela 2.3
# ===================================
st.header("Tabela 2.3")

# Konstanta k12
k12 = 2
st.write(f"**Konstanta:** k12 = {k12}")
st.write("**Formula za Fa:**")
st.latex(r'''F_a = \frac{F_z - F_p}{k12}''')
Fa = (Fz - Fp) / k12
st.write(f"**Fa = {Fa:.6f} N**")

st.write("**Formula za σa:**")
st.latex(r'''\sigma_a = \frac{F_a}{A_s}''')
sigmaa = Fa / As
st.write(f"**σa = {sigmaa:.6f} N/mm²**")

st.write("**Koeficijent sigurnosti za amplitudni napon:**")
st.latex(r'''S_a = \frac{\sigma_{AM}}{\sigma_a}''')
Sa = SigmaAM / sigmaa
st.write(f"**Sa = {Sa:.6f}**")
st.info("Veće od **Smin = 1.25 – 2.5** (proveriti) + komentar")