import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
import subprocess

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Otonom Hava Savunma & Tehdit Skorlama",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyber Military Style CSS
st.markdown("""
<style>
    /* Dashboard header style */
    .dashboard-header {
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        background: linear-gradient(90deg, #1E293B, #0F172A);
        border: 2px solid #0F766E;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0px 4px 20px rgba(15, 118, 110, 0.25);
        margin-bottom: 25px;
    }
    .dashboard-title {
        color: #06B6D4;
        font-size: 2rem;
        font-weight: bold;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
    }
    .dashboard-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-top: 5px;
        margin-bottom: 0;
    }
    /* Credit line - small and subtle */
    .credit-line {
        text-align: right;
        color: #475569;
        font-size: 0.7rem;
        margin-top: -18px;
        margin-bottom: 10px;
        padding-right: 10px;
        font-style: italic;
    }
    /* Threat Score Card style */
    .score-card {
        background: #0F172A;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    .score-title {
        font-size: 1.1rem;
        color: #94A3B8;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .score-value {
        font-size: 3.5rem;
        font-weight: 800;
        font-family: 'Courier New', Courier, monospace;
        margin: 10px 0;
    }
    .score-status {
        font-size: 1.4rem;
        font-weight: bold;
        padding: 6px 16px;
        border-radius: 20px;
        display: inline-block;
    }
    /* Rule table styling */
    .rule-item {
        background-color: #1E293B;
        border-left: 5px solid #64748B;
        padding: 8px 12px;
        margin-bottom: 6px;
        border-radius: 0 4px 4px 0;
        font-size: 0.85rem;
        color: #CBD5E1;
    }
    .rule-active {
        background-color: rgba(15, 118, 110, 0.15);
        border-left: 5px solid #0D9488;
        color: #E2E8F0;
    }
    .rule-inactive {
        background-color: #1E293B;
        border-left: 5px solid #334155;
        color: #94A3B8;
    }
    .rule-trigger-val {
        color: #22D3EE;
        font-weight: bold;
        float: right;
    }
    .rule-trigger-val-inactive {
        color: #64748B;
        font-weight: normal;
        float: right;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- FUZZY LOGIC CONFIGURATION -----------------

# Define universes
x_mesafe = np.arange(0, 101, 1)
x_hiz = np.arange(0, 1201, 1)
x_irtifa = np.arange(0, 10001, 10)
x_tehdit = np.arange(0, 101, 1)

# Create Antecedent/Consequent objects
mesafe = ctrl.Antecedent(x_mesafe, 'mesafe')
hiz = ctrl.Antecedent(x_hiz, 'hiz')
irtifa = ctrl.Antecedent(x_irtifa, 'irtifa')
tehdit = ctrl.Consequent(x_tehdit, 'tehdit')

# Membership Functions (trimf)
mesafe['yakin'] = fuzz.trimf(mesafe.universe, [0, 0, 50])
mesafe['orta'] = fuzz.trimf(mesafe.universe, [20, 50, 80])
mesafe['uzak'] = fuzz.trimf(mesafe.universe, [50, 100, 100])

hiz['yavas'] = fuzz.trimf(hiz.universe, [0, 0, 500])
hiz['normal'] = fuzz.trimf(hiz.universe, [300, 600, 900])
hiz['hizli'] = fuzz.trimf(hiz.universe, [700, 1200, 1200])

irtifa['dusuk'] = fuzz.trimf(irtifa.universe, [0, 0, 4000])
irtifa['orta'] = fuzz.trimf(irtifa.universe, [2000, 5000, 8000])
irtifa['yuksek'] = fuzz.trimf(irtifa.universe, [6000, 10000, 10000])

tehdit['dusuk'] = fuzz.trimf(tehdit.universe, [0, 0, 50])
tehdit['orta'] = fuzz.trimf(tehdit.universe, [25, 50, 75])
tehdit['yuksek'] = fuzz.trimf(tehdit.universe, [50, 100, 100])

# Define Rules
rules_list = [
    ctrl.Rule(mesafe['yakin'] & hiz['hizli'] & irtifa['dusuk'], tehdit['yuksek']),
    ctrl.Rule(mesafe['yakin'] & hiz['yavas'] & irtifa['dusuk'], tehdit['yuksek']),
    ctrl.Rule(mesafe['yakin'] & hiz['hizli'] & irtifa['yuksek'], tehdit['yuksek']),
    ctrl.Rule(mesafe['yakin'] & hiz['normal'] & irtifa['orta'], tehdit['yuksek']),
    ctrl.Rule(mesafe['yakin'] & hiz['yavas'] & irtifa['yuksek'], tehdit['orta']),
    ctrl.Rule(mesafe['orta'] & hiz['hizli'] & irtifa['dusuk'], tehdit['yuksek']),
    ctrl.Rule(mesafe['orta'] & hiz['normal'] & irtifa['orta'], tehdit['orta']),
    ctrl.Rule(mesafe['orta'] & hiz['yavas'] & irtifa['dusuk'], tehdit['orta']),
    ctrl.Rule(mesafe['orta'] & hiz['hizli'] & irtifa['yuksek'], tehdit['yuksek']),
    ctrl.Rule(mesafe['uzak'] & hiz['normal'] & irtifa['orta'], tehdit['dusuk']),
    ctrl.Rule(mesafe['uzak'] & hiz['yavas'] & irtifa['dusuk'], tehdit['dusuk']),
    ctrl.Rule(mesafe['uzak'] & hiz['hizli'] & irtifa['yuksek'], tehdit['dusuk']),
    ctrl.Rule(mesafe['uzak'] & hiz['yavas'] & irtifa['yuksek'], tehdit['dusuk']),
    ctrl.Rule(mesafe['uzak'] & hiz['hizli'] & irtifa['dusuk'], tehdit['orta']),
    ctrl.Rule(mesafe['orta'] & hiz['yavas'] & irtifa['yuksek'], tehdit['dusuk'])
]

tehdit_ctrl = ctrl.ControlSystem(rules_list)
tehdit_sim = ctrl.ControlSystemSimulation(tehdit_ctrl)

# Rule descriptions for display
rule_texts = [
    ("Kural 1: Mesafe Yakın VE Hız Hızlı VE İrtifa Düşük ⇒ Tehdit Yüksek", "yakin", "hizli", "dusuk", "yuksek"),
    ("Kural 2: Mesafe Yakın VE Hız Yavaş VE İrtifa Düşük ⇒ Tehdit Yüksek", "yakin", "yavas", "dusuk", "yuksek"),
    ("Kural 3: Mesafe Yakın VE Hız Hızlı VE İrtifa Yüksek ⇒ Tehdit Yüksek", "yakin", "hizli", "yuksek", "yuksek"),
    ("Kural 4: Mesafe Yakın VE Hız Normal VE İrtifa Orta ⇒ Tehdit Yüksek", "yakin", "normal", "orta", "yuksek"),
    ("Kural 5: Mesafe Yakın VE Hız Yavaş VE İrtifa Yüksek ⇒ Tehdit Orta", "yakin", "yavas", "yuksek", "orta"),
    ("Kural 6: Mesafe Orta VE Hız Hızlı VE İrtifa Düşük ⇒ Tehdit Yüksek", "orta", "hizli", "dusuk", "yuksek"),
    ("Kural 7: Mesafe Orta VE Hız Normal VE İrtifa Orta ⇒ Tehdit Orta", "orta", "normal", "orta", "orta"),
    ("Kural 8: Mesafe Orta VE Hız Yavaş VE İrtifa Düşük ⇒ Tehdit Orta", "orta", "yavas", "dusuk", "orta"),
    ("Kural 9: Mesafe Orta VE Hız Hızlı VE İrtifa Yüksek ⇒ Tehdit Yüksek", "orta", "hizli", "yuksek", "yuksek"),
    ("Kural 10: Mesafe Uzak VE Hız Normal VE İrtifa Orta ⇒ Tehdit Düşük", "uzak", "normal", "orta", "dusuk"),
    ("Kural 11: Mesafe Uzak VE Hız Yavaş VE İrtifa Düşük ⇒ Tehdit Düşük", "uzak", "yavas", "dusuk", "dusuk"),
    ("Kural 12: Mesafe Uzak VE Hız Hızlı VE İrtifa Yüksek ⇒ Tehdit Düşük", "uzak", "hizli", "yuksek", "dusuk"),
    ("Kural 13: Mesafe Uzak VE Hız Yavaş VE İrtifa Yüksek ⇒ Tehdit Düşük", "uzak", "yavas", "yuksek", "dusuk"),
    ("Kural 14: Mesafe Uzak VE Hız Hızlı VE İrtifa Düşük ⇒ Tehdit Orta", "uzak", "hizli", "dusuk", "orta"),
    ("Kural 15: Mesafe Orta VE Hız Yavaş VE İrtifa Yüksek ⇒ Tehdit Düşük", "orta", "yavas", "yuksek", "dusuk"),
]

# Output membership term mapping for aggregate computation
output_term_map = {
    "yuksek": tehdit['yuksek'].mf,
    "orta": tehdit['orta'].mf,
    "dusuk": tehdit['dusuk'].mf,
}

# ----------------- STREAMLIT GUI -----------------

# Header Section (6: Hazırlayan ismi küçük ve dikkat çekmeyen yerde)
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">OTONOM HAVA SAVUNMA & TEHDİT SKORLAMA SİSTEMİ</div>
    <div class="dashboard-subtitle">Bulanık Mantık (Fuzzy Logic) Karar Destek Paneli</div>
</div>
<div class="credit-line">Geliştiren: Muammer Çelik</div>
""", unsafe_allow_html=True)

# Initialize session state for results
if 'computed' not in st.session_state:
    st.session_state.computed = False
if 'threat_score' not in st.session_state:
    st.session_state.threat_score = 0.0
if 'val_mesafe' not in st.session_state:
    st.session_state.val_mesafe = 50.0
if 'val_hiz' not in st.session_state:
    st.session_state.val_hiz = 600
if 'val_irtifa' not in st.session_state:
    st.session_state.val_irtifa = 5000

# Layout: Sidebar Controls + Main Dashboard
col_side, col_main = st.columns([1, 3])

with col_side:
    st.markdown("### 🛠️ Sistem Parametreleri")

    # --- (1) Senaryo Seçimi: 4 senaryo + manuel ---
    st.markdown("#### 📋 Senaryo Seçimi")
    scenario_option = st.selectbox(
        "Senaryo Şablonu:",
        [
            "Manuel Giriş",
            "Düşük İrtifa Kamikaze İHA",
            "Ticari Uçuş Geçişi",
            "Seyir Füzesi Yaklaşması",
            "Hızlı Taktik Balistik Füze",
        ],
        label_visibility="collapsed"
    )

    # Defaults depending on scenario
    if scenario_option == "Düşük İrtifa Kamikaze İHA":
        default_mesafe = 15.0
        default_hiz = 200
        default_irtifa = 500
    elif scenario_option == "Ticari Uçuş Geçişi":
        default_mesafe = 80.0
        default_hiz = 800
        default_irtifa = 9000
    elif scenario_option == "Seyir Füzesi Yaklaşması":
        default_mesafe = 25.0
        default_hiz = 900
        default_irtifa = 300
    elif scenario_option == "Hızlı Taktik Balistik Füze":
        default_mesafe = 40.0
        default_hiz = 1100
        default_irtifa = 2000
    else:
        default_mesafe = 50.0
        default_hiz = 600
        default_irtifa = 5000

    st.markdown("---")

    # --- Giriş Yöntemi Seçimi ---
    input_method = st.radio(
        "Giriş Yöntemi:",
        ["Slider (Kaydırıcı)", "Metin Kutusu (Sayısal)"],
        horizontal=True
    )

    if input_method == "Slider (Kaydırıcı)":
        val_mesafe = st.slider(
            "📏 Mesafe (km):", 0.0, 100.0, float(default_mesafe), 0.5,
            help="Hedefin bataryaya olan uzaklığı"
        )
        val_hiz = st.slider(
            "💨 Hız (km/h):", 0, 1200, int(default_hiz), 10,
            help="Hedefin yaklaşma hızı"
        )
        val_irtifa = st.slider(
            "✈️ İrtifa (metre):", 0, 10000, int(default_irtifa), 100,
            help="Hedefin uçuş yüksekliği"
        )
    else:
        val_mesafe = st.number_input(
            "📏 Mesafe (km):", min_value=0.0, max_value=100.0,
            value=float(default_mesafe), step=0.5,
            help="Hedefin bataryaya olan uzaklığı"
        )
        val_hiz = st.number_input(
            "💨 Hız (km/h):", min_value=0, max_value=1200,
            value=int(default_hiz), step=10,
            help="Hedefin yaklaşma hızı"
        )
        val_irtifa = st.number_input(
            "✈️ İrtifa (metre):", min_value=0, max_value=10000,
            value=int(default_irtifa), step=100,
            help="Hedefin uçuş yüksekliği"
        )

    st.markdown("---")

    # HESAPLA butonu
    calculate_clicked = st.button(
        "🔴 SİSTEMİ ÇALIŞTIR (HESAPLA)",
        use_container_width=True,
        type="primary"
    )

    if calculate_clicked:
        st.session_state.computed = True
        st.session_state.val_mesafe = val_mesafe
        st.session_state.val_hiz = val_hiz
        st.session_state.val_irtifa = val_irtifa

    st.markdown("---")

    # (5) PDF Sonuç Raporu — sadece girişler ve sonuç var
    st.markdown("### 📄 Sonuç Raporu")
    if st.button("📁 PDF Sonuç Raporu Oluştur", use_container_width=True):
        if not st.session_state.computed:
            st.warning("Lütfen rapor oluşturmadan önce sistemi çalıştırın!")
        else:
            with st.spinner("PDF Raporu hazırlanıyor..."):
                try:
                    result = subprocess.run([
                        "python", "generate_pdf.py",
                        str(st.session_state.val_mesafe),
                        str(st.session_state.val_hiz),
                        str(st.session_state.val_irtifa),
                        f"{st.session_state.threat_score:.1f}"
                    ], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        st.success("PDF Raporu başarıyla oluşturuldu!")
                    else:
                        st.error(f"Hata oluştu: {result.stderr}")
                except Exception as e:
                    st.error(f"Hata oluştu: {e}")

    pdf_filename = "Hesaplama_Sonucu.pdf"
    if os.path.exists(pdf_filename):
        with open(pdf_filename, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="⬇️ PDF Sonuç Raporunu İndir",
            data=pdf_bytes,
            file_name=pdf_filename,
            mime="application/pdf",
            use_container_width=True
        )

# ==========================================
# MAIN PANEL: Results (only after HESAPLA)
# ==========================================
with col_main:
    if not st.session_state.computed:
        st.info(
            "⬅️ Sol panelden giriş değerlerini ayarlayın ve **'SİSTEMİ ÇALIŞTIR (HESAPLA)'** "
            "butonuna basarak tehdit analizini başlatın."
        )
        st.stop()

    # Use stored values from session state
    val_mesafe = st.session_state.val_mesafe
    val_hiz = st.session_state.val_hiz
    val_irtifa = st.session_state.val_irtifa

    # ---- Compute Fuzzy Output ----
    tehdit_sim.input['mesafe'] = val_mesafe
    tehdit_sim.input['hiz'] = val_hiz
    tehdit_sim.input['irtifa'] = val_irtifa

    try:
        tehdit_sim.compute()
        threat_score = tehdit_sim.output['tehdit']
    except Exception:
        threat_score = 0.0

    st.session_state.threat_score = threat_score

    # Determine class & colors
    if threat_score <= 35:
        status_text = "DÜŞÜK TEHDİT"
        status_color = "#10B981"
        card_shadow = "rgba(16, 185, 129, 0.3)"
    elif threat_score <= 65:
        status_text = "ORTA TEHDİT"
        status_color = "#F59E0B"
        card_shadow = "rgba(245, 158, 11, 0.3)"
    else:
        status_text = "YÜKSEK TEHDİT"
        status_color = "#EF4444"
        card_shadow = "rgba(239, 68, 68, 0.3)"

    # Dilsel terim Türkçe etiketleri
    mesafe_labels = {"yakin": "Yakın", "orta": "Orta", "uzak": "Uzak"}
    hiz_labels = {"yavas": "Yavaş", "normal": "Normal", "hizli": "Hızlı"}
    irtifa_labels = {"dusuk": "Düşük", "orta": "Orta", "yuksek": "Yüksek"}
    tehdit_labels = {"dusuk": "Düşük", "orta": "Orta", "yuksek": "Yüksek"}

    # ---- Rule activation analysis (with per-input membership details) ----
    activated_rules = []
    for rule_txt, m_name, s_name, a_name, out_name in rule_texts:
        m_val = fuzz.interp_membership(x_mesafe, mesafe[m_name].mf, val_mesafe)
        s_val = fuzz.interp_membership(x_hiz, hiz[s_name].mf, val_hiz)
        a_val = fuzz.interp_membership(x_irtifa, irtifa[a_name].mf, val_irtifa)
        activation = min(m_val, s_val, a_val)
        activated_rules.append((rule_txt, activation, out_name, m_name, s_name, a_name, m_val, s_val, a_val))

    # Sonuç kartı
    st.markdown(f"""
    <div class="score-card" style="box-shadow: 0 8px 30px {card_shadow}; border: 1.5px solid {status_color}">
        <div class="score-title">🎯 Mamdani Bulanık Çıkarım Çıktısı (Centroid Durulaştırma)</div>
        <div class="score-value" style="color: {status_color}">{threat_score:.1f}%</div>
        <div class="score-status" style="background-color: {status_color}; color: #000000;">{status_text}</div>
    </div>
    """, unsafe_allow_html=True)

    # Üyelik Fonksiyonları Grafikleri
    st.markdown("### 📊 Üyelik Fonksiyonları")

    plt.style.use('dark_background')
    fig_mf, axes_mf = plt.subplots(1, 3, figsize=(14, 3.5))
    fig_mf.patch.set_facecolor('#0B0F19')

    ax = axes_mf[0]
    ax.set_facecolor('#0F172A')
    ax.plot(x_mesafe, mesafe['yakin'].mf, '#3B82F6', linewidth=1.8, label='Yakın')
    ax.plot(x_mesafe, mesafe['orta'].mf, '#F59E0B', linewidth=1.8, label='Orta')
    ax.plot(x_mesafe, mesafe['uzak'].mf, '#10B981', linewidth=1.8, label='Uzak')
    ax.axvline(x=val_mesafe, color='#FF2E93', linestyle='--', linewidth=2, label=f'Giriş ({val_mesafe})')
    ax.set_title('Mesafe (km)', fontsize=10, color='#06B6D4')
    ax.set_xlabel('km')
    ax.set_ylabel('Üyelik Derecesi')
    ax.legend(fontsize=7, loc='upper right')
    ax.grid(True, alpha=0.15)

    ax = axes_mf[1]
    ax.set_facecolor('#0F172A')
    ax.plot(x_hiz, hiz['yavas'].mf, '#3B82F6', linewidth=1.8, label='Yavaş')
    ax.plot(x_hiz, hiz['normal'].mf, '#F59E0B', linewidth=1.8, label='Normal')
    ax.plot(x_hiz, hiz['hizli'].mf, '#EF4444', linewidth=1.8, label='Hızlı')
    ax.axvline(x=val_hiz, color='#FF2E93', linestyle='--', linewidth=2, label=f'Giriş ({val_hiz})')
    ax.set_title('Hız (km/h)', fontsize=10, color='#06B6D4')
    ax.set_xlabel('km/h')
    ax.legend(fontsize=7, loc='upper right')
    ax.grid(True, alpha=0.15)

    ax = axes_mf[2]
    ax.set_facecolor('#0F172A')
    ax.plot(x_irtifa, irtifa['dusuk'].mf, '#3B82F6', linewidth=1.8, label='Düşük')
    ax.plot(x_irtifa, irtifa['orta'].mf, '#F59E0B', linewidth=1.8, label='Orta')
    ax.plot(x_irtifa, irtifa['yuksek'].mf, '#10B981', linewidth=1.8, label='Yüksek')
    ax.axvline(x=val_irtifa, color='#FF2E93', linestyle='--', linewidth=2, label=f'Giriş ({val_irtifa})')
    ax.set_title('İrtifa (m)', fontsize=10, color='#06B6D4')
    ax.set_xlabel('metre')
    ax.legend(fontsize=7, loc='upper right')
    ax.grid(True, alpha=0.15)

    plt.tight_layout()
    st.pyplot(fig_mf)
    plt.close(fig_mf)

    # Durulaştırma Grafiği
    st.markdown("### 📈 Durulaştırma (Çıkış) — Aggregate Alan ve Ağırlık Merkezi")

    aggregate = np.zeros_like(x_tehdit, dtype=float)
    for rule_data in activated_rules:
        activation = rule_data[1]
        out_name = rule_data[2]
        if activation > 0:
            clipped = np.fmin(activation, output_term_map[out_name])
            aggregate = np.fmax(aggregate, clipped)

    fig_defuzz, ax_d = plt.subplots(1, 1, figsize=(10, 4))
    fig_defuzz.patch.set_facecolor('#0B0F19')
    ax_d.set_facecolor('#0F172A')

    ax_d.plot(x_tehdit, tehdit['dusuk'].mf, '#10B981', linewidth=1, linestyle=':', alpha=0.5, label='Düşük (orijinal)')
    ax_d.plot(x_tehdit, tehdit['orta'].mf, '#F59E0B', linewidth=1, linestyle=':', alpha=0.5, label='Orta (orijinal)')
    ax_d.plot(x_tehdit, tehdit['yuksek'].mf, '#EF4444', linewidth=1, linestyle=':', alpha=0.5, label='Yüksek (orijinal)')

    ax_d.fill_between(x_tehdit, aggregate, alpha=0.45, color='#06B6D4', label='Birleşik Çıkış Alanı')
    ax_d.plot(x_tehdit, aggregate, '#06B6D4', linewidth=2)

    ax_d.axvline(x=threat_score, color='#FF2E93', linestyle='-', linewidth=2.5,
                 label=f'Ağırlık Merkezi (Centroid) = {threat_score:.1f}%')

    ax_d.annotate(f'{threat_score:.1f}%',
                  xy=(threat_score, 0), xytext=(threat_score + 5, 0.15),
                  fontsize=14, fontweight='bold', color='#FF2E93',
                  arrowprops=dict(arrowstyle='->', color='#FF2E93', lw=1.5))

    ax_d.axvspan(0, 35, alpha=0.05, color='#10B981')
    ax_d.axvspan(35, 65, alpha=0.05, color='#F59E0B')
    ax_d.axvspan(65, 100, alpha=0.05, color='#EF4444')
    ax_d.text(17.5, 0.95, 'DÜŞÜK', ha='center', fontsize=8, color='#10B981', alpha=0.6)
    ax_d.text(50, 0.95, 'ORTA', ha='center', fontsize=8, color='#F59E0B', alpha=0.6)
    ax_d.text(82.5, 0.95, 'YÜKSEK', ha='center', fontsize=8, color='#EF4444', alpha=0.6)

    ax_d.set_title('Çıkış Durulaştırma — Aggregate Çıkış Alanı ve Centroid', fontsize=11, color='#06B6D4')
    ax_d.set_xlabel('Tehdit Skoru (%)', fontsize=10)
    ax_d.set_ylabel('Üyelik Derecesi', fontsize=10)
    ax_d.set_xlim([0, 100])
    ax_d.set_ylim([0, 1.05])
    ax_d.legend(fontsize=8, loc='upper left')
    ax_d.grid(True, alpha=0.15)

    plt.tight_layout()
    st.pyplot(fig_defuzz)
    plt.close(fig_defuzz)

    # Kural Aktivasyon Analizi — detaylı sözel açıklama + üyelik dereceleri
    st.markdown("### 🔍 Kural Aktivasyon Analizi")

    active_list = [r for r in activated_rules if r[1] > 0]
    inactive_list = [r for r in activated_rules if r[1] == 0]
    active_list.sort(key=lambda x: x[1], reverse=True)

    col_act, col_inact = st.columns(2)

    with col_act:
        st.markdown("#### ✅ Tetiklenen Kurallar")
        if active_list:
            for rule_txt, activation, out_name, m_name, s_name, a_name, m_val, s_val, a_val in active_list:
                # Detaylı sözel açıklama
                detail_line = (
                    f"Mesafe → <b>{mesafe_labels[m_name]}</b> ({m_val:.3f}) &nbsp;|&nbsp; "
                    f"Hız → <b>{hiz_labels[s_name]}</b> ({s_val:.3f}) &nbsp;|&nbsp; "
                    f"İrtifa → <b>{irtifa_labels[a_name]}</b> ({a_val:.3f}) &nbsp;⇒&nbsp; "
                    f"Tehdit: <b>{tehdit_labels[out_name]}</b>"
                )
                st.markdown(f"""
                <div class="rule-item rule-active">
                    <div style="margin-bottom:4px; color:#E2E8F0; font-weight:bold;">{rule_txt}</div>
                    <div style="font-size:0.78rem; color:#94A3B8;">{detail_line}</div>
                    <div style="text-align:right; margin-top:3px;">
                        <span class="rule-trigger-val">MIN Aktivasyon: {activation:.3f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Hiçbir kural tetiklenmedi! Lütfen girdi değerlerini kontrol edin.")

    with col_inact:
        st.markdown("#### 💤 Uymayan (Pasif) Kurallar")
        with st.container(height=400):
            for rule_txt, _, _, _, _, _, _, _, _ in inactive_list:
                st.markdown(f"""
                <div class="rule-item rule-inactive">
                    {rule_txt}
                </div>
                """, unsafe_allow_html=True)
