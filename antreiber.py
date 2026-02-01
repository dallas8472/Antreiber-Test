import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import os
import random
from datetime import datetime

# --- 1. DATENBASIS (Bereinigt um Sonderzeichen) ---

QUESTIONS = {
    1: "Wenn ich eine Arbeit mache, dann mache ich sie gründlich.",
    2: "Ich fühle mich verantwortlich, dass diejenigen, die mit mir zu tun haben, sich wohlfühlen.",
    3: "Ich bin ständig auf Trab.",
    4: "Wenn ich raste, roste ich.",
    5: "Anderen gegenüber zeige ich meine Schwächen nicht gerne.",
    6: "Häufig gebrauche ich den Satz: 'Es ist schwierig, etwas so genau zu sagen'.",
    7: "Ich sage oft mehr, als eigentlich nötig wäre.",
    8: "Ich habe Mühe, Leute zu akzeptieren, die nicht in ihrer Arbeit genau sind.",
    9: "Es fällt mir schwer, Gefühle zu zeigen.",
    10: "'Nur nicht lockerlassen', ist meine Devise.",
    11: "Wenn ich eine Meinung äußere, begründe ich sie.",
    12: "Wenn ich einen Wunsch habe, erfülle ich ihn mir schnell.",
    13: "Ich liefere einen Bericht erst ab, wenn ich ihn mehrere Male überarbeitet habe.",
    14: "Leute, die 'herumtrödeln', regen mich auf.",
    15: "Es ist für mich wichtig, von anderen akzeptiert zu werden.",
    16: "Ich habe eher eine harte Schale, aber einen weichen Kern.",
    17: "Ich versuche oft herauszufinden, was andere von mir erwarten, um mich danach zu richten.",
    18: "Leute, die unbekümmert in den Tag hineinleben, kann ich nur schwer verstehen.",
    19: "Bei Diskussionen unterbreche ich die anderen oft.",
    20: "Ich löse meine Probleme selbst.",
    21: "Aufgaben erledige ich möglichst rasch.",
    22: "Im Umgang mit anderen bin ich auf Distanz bedacht.",
    23: "Ich sollte viele Aufgaben noch besser erledigen.",
    24: "Ich kümmere mich persönlich auch um nebensächliche Dinge.",
    25: "Erfolge fallen nicht vom Himmel, ich muss sie hart erarbeiten.",
    26: "Für dumme Fehler habe ich wenig Verständnis.",
    27: "Ich schätze es, wenn andere meine Fragen rasch und bündig beantworten.",
    28: "Es ist mir wichtig, von anderen zu erfahren, ob ich meine Sache gut gemacht habe.",
    29: "Wenn ich eine Aufgabe einmal begonnen habe, führe ich sie auch zu Ende.",
    30: "Ich stelle meine Wünsche und Bedürfnisse zugunsten der Bedürfnisse anderer Personen zurück.",
    31: "Ich bin anderen gegenüber oft hart, um von ihnen nicht verletzt zu werden.",
    32: "Ich trommle oft ungeduldig mit den Fingern auf den Tisch (ich bin ungeduldig).",
    33: "Beim Erklären von Sachverhalten verwende ich gerne die klare Aufzählung: Erstens..., zweitens...",
    34: "Ich glaube, dass die meisten Dinge nicht so einfach sind, wie viele meinen.",
    35: "Es ist mir unangenehm, andere Leute zu kritisieren.",
    36: "Bei Diskussionen nicke ich häufig mit dem Kopf.",
    37: "Ich strenge mich an, um meine Ziele zu erreichen.",
    38: "Mein Gesichtsausdruck ist eher ernst.",
    39: "Ich bin nervös.",
    40: "So schnell kann mich nichts erschüttern.",
    41: "Meine Probleme gehen die anderen nichts an.",
    42: "Ich sage oft: 'Tempo, Tempo, das muss rascher gehen!'",
    43: "Ich sage oft: 'genau', 'exakt', 'logisch', 'klar' u.ä.",
    44: "Ich sage oft: 'Das verstehe ich nicht...'",
    45: "Ich sage gerne: 'Könnten Sie es nicht einmal versuchen?' und sage nicht gerne: 'Versuchen Sie es einmal.'",
    46: "Ich bin diplomatisch.",
    47: "Ich versuche, die an mich gestellten Erwartungen zu übertreffen.",
    48: "Ich mache manchmal zwei Tätigkeiten gleichzeitig.",
    49: "'Die Zähne zusammenbeißen' heißt meine Devise.",
    50: "Trotz enormer Anstrengungen will mir vieles einfach nicht gelingen."
}

CATEGORIES = {
    "Sei perfekt": [1, 8, 11, 13, 23, 24, 33, 38, 43, 47],
    "Mach schnell": [3, 12, 14, 19, 21, 27, 32, 39, 42, 48],
    "Streng dich an": [4, 6, 10, 18, 25, 29, 34, 37, 44, 50],
    "Mach es allen recht": [2, 7, 15, 17, 28, 30, 35, 36, 45, 46],
    "Sei stark": [5, 9, 16, 20, 22, 26, 31, 40, 41, 49]
}

FEEDBACK = {
    "Sei perfekt": {
        "Glaubenssatz": "Ich muss alles noch besser machen, es ist nie gut genug.",
        "Erlauber": "Ich darf Fehler machen und aus ihnen lernen. Es können manchmal auch 90% genügen."
    },
    "Mach schnell": {
        "Glaubenssatz": "Ich muss schnell sein, sonst werde ich nicht fertig.",
        "Erlauber": "Ich darf mir Zeit nehmen und auch Pausen machen. Manches darf auch länger dauern."
    },
    "Streng dich an": {
        "Glaubenssatz": "Ich muss mich immer anstrengen, egal wobei. 'Ohne Fleiß kein Preis.'",
        "Erlauber": "Ich darf auch ohne Anstrengung Sachen erledigen. Erfolge dürfen auch Zeit benötigen."
    },
    "Mach es allen recht": {
        "Glaubenssatz": "Ich bin dann wertvoll, wenn alle mit mir zufrieden sind.",
        "Erlauber": "Ich darf meine Bedürfnisse ernst nehmen. Ich bin OK, auch wenn jemand unzufrieden mit mir ist."
    },
    "Sei stark": {
        "Glaubenssatz": "Niemand darf es merken, dass ich schwach oder ratlos bin.",
        "Erlauber": "Ich darf offen sein für Zuwendung. Ich darf mir Hilfe holen und sie annehmen."
    }
}

TIPS = {
    "Sei perfekt": ["Lass heute eine E-Mail mit einem kleinen Tippfehler raus.", "Gut genug ist das neue Perfekt."],
    "Mach schnell": ["Mach heute eine 5-Minuten-Pause ohne Handy.", "Gehe heute bewusst langsam zu einem Termin."],
    "Streng dich an": ["Feiere heute einen Erfolg, der dir leicht gefallen ist.", "Genieße den Feierabend ohne schlechtes Gewissen."],
    "Mach es allen recht": ["Sage heute einmal freundlich aber bestimmt 'Nein'.", "Entscheide heute etwas nur für dich."],
    "Sei stark": ["Bitte heute einen Kollegen um Hilfe.", "Teile eine kleine Sorge mit jemandem."]
}

# --- 2. PDF KLASSE & FUNKTION ---

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Antreiber-Test Ergebnis', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Seite {self.page_no()}', 0, 0, 'C')

def clean_text(text):
    """Ersetzt Zeichen, die FPDF (Latin-1) nicht mag."""
    replacements = {
        "„": '"', "“": '"', "”": '"', "’": "'", "–": "-"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Sicherstellen, dass alles Latin-1 kompatibel ist
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_pdf_file(results, chart_path):
    pdf = PDF()
    pdf.add_page()
    
    # Einführung
    pdf.set_font("Arial", size=11)
    intro = "Dies ist deine persönliche Auswertung. Werte ab 30 Punkten deuten auf eine starke Ausprägung hin (Stresspotenzial), Werte ab 40 auf eine sehr starke Ausprägung."
    pdf.multi_cell(0, 6, clean_text(intro))
    pdf.ln(5)
    
    # 1. Bild einfügen
    if os.path.exists(chart_path):
        pdf.image(chart_path, x=30, w=150)
    pdf.ln(5)
    
    # 2. Tabelle der Ergebnisse
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, clean_text("Detailübersicht"), 0, 1)
    
    # Daten sortieren
    sorted_items = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    for antreiber, punkte in sorted_items:
        status = ""
        color = (0, 0, 0)
        if punkte >= 40:
            status = "SEHR HOCH (Warnung)"
            color = (200, 0, 0)
        elif punkte >= 30:
            status = "HOCH (Stressanfällig)"
            color = (200, 100, 0)
        else:
            status = "Förderlich"
            color = (0, 100, 0)
            
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(*color)
        line_text = f"{antreiber}: {punkte} Punkte - {status}"
        pdf.cell(0, 8, clean_text(line_text), 0, 1)
        
        # Details schwarz
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 10)
        glaubenssatz = FEEDBACK[antreiber]['Glaubenssatz']
        erlauber = FEEDBACK[antreiber]['Erlauber']
        
        pdf.multi_cell(0, 5, clean_text(f"Glaubenssatz: {glaubenssatz}"))
        pdf.set_font("Arial", 'I', 10)
        pdf.multi_cell(0, 5, clean_text(f"Erlauber: {erlauber}"))
        pdf.ln(3)

    return pdf.output(dest='S').encode('latin-1', 'replace')

# --- 3. STREAMLIT GUI ---

st.set_page_config(page_title="Antreiber-Test", page_icon="🧠", layout="wide")

st.title("🧠 Der Antreiber-Test")
st.markdown("""
Finde heraus, welche inneren Antreiber dich steuern. 
Bitte bewerte die Aussagen spontan (**1 = Gar nicht** bis **5 = Voll und ganz**).
""")

st.markdown("<style>.stSlider {padding-bottom: 10px;}</style>", unsafe_allow_html=True)

scores = {}

# Formular für die Eingabe
with st.form("test_form"):
    st.header("Die 50 Fragen")
    
    col1, col2 = st.columns(2)
    
    for i in range(1, 51):
        target_col = col1 if i <= 25 else col2
        with target_col:
            st.markdown(f"**{i}. {QUESTIONS[i]}**")
            scores[i] = st.slider(f"Frage {i}", 1, 5, 3, key=f"q{i}", label_visibility="collapsed")
    
    st.markdown("---")
    submitted = st.form_submit_button("Auswertung anzeigen", type="primary")

# --- 4. AUSWERTUNG ---

if submitted:
    st.divider()
    st.title("Dein Ergebnis")
    
    results = {cat: sum(scores[q] for q in q_list) for cat, q_list in CATEGORIES.items()}
    df = pd.DataFrame(list(results.items()), columns=["Antreiber", "Punkte"])
    df = df.sort_values(by="Punkte", ascending=False)
    
    # Radar Chart
    labels = list(results.keys())
    values = list(results.values())
    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'o-', linewidth=2, color='#4CAF50')
    ax.fill(angles, values, alpha=0.25, color='#4CAF50')
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0, 50)
    ax.set_yticks([10, 20, 30, 40, 50])
    ax.grid(True, color='gray', linestyle='--', alpha=0.5)
    ax.set_title("Dein Antreiber-Profil", va='bottom', fontweight='bold')
    
    res_col1, res_col2 = st.columns([1, 1])
    
    with res_col1:
        st.subheader("Deine Werte")
        st.dataframe(df.style.format({'Punkte': '{:.0f}'}).background_gradient(cmap='Greens', vmin=0, vmax=50), use_container_width=True)
        top_driver = df.iloc[0]['Antreiber']
        st.info(f"💡 **Tipp für deinen stärksten Antreiber ({top_driver}):**\n\n{random.choice(TIPS[top_driver])}")

    with res_col2:
        st.pyplot(fig)
    
    # PDF Generierung
    chart_filename = "temp_chart_antreiber.png"
    fig.savefig(chart_filename, format='png', bbox_inches='tight', dpi=100)
    
    try:
        pdf_bytes = generate_pdf_file(results, chart_filename)
        
        st.download_button(
            label="📄 Ergebnis als PDF herunterladen",
            data=pdf_bytes,
            file_name=f"Antreiber_Test_{datetime.now().strftime('%Y-%m-%d')}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Fehler bei PDF-Erstellung: {e}")
    finally:
        if os.path.exists(chart_filename):
            os.remove(chart_filename)

    st.subheader("Detaillierte Analyse")
    
    for index, row in df.iterrows():
        ant = row['Antreiber']
        pts = row['Punkte']
        
        if pts >= 40:
            header_emoji = "🔴"
            warn_msg = "Achtung: Dieser Antreiber ist sehr dominant und kann gesundheitsschädlich sein."
        elif pts >= 30:
            header_emoji = "🟠"
            warn_msg = "Dieser Antreiber ist stark ausgeprägt und verursacht Stress."
        else:
            header_emoji = "🟢"
            warn_msg = ""
            
        with st.expander(f"{header_emoji} {ant}: {pts} Punkte"):
            st.markdown(f"**Innerer Glaubenssatz:** *„{FEEDBACK[ant]['Glaubenssatz']}“*")
            st.success(f"**Dein Erlauber:** {FEEDBACK[ant]['Erlauber']}")
            if warn_msg:
                st.warning(warn_msg)