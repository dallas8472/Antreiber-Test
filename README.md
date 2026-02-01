# 🧠 Antreiber-Test (Transaktionsanalyse)

Dieses Projekt ist eine interaktive Web-Applikation zur Durchführung des klassischen **Antreiber-Tests** aus der Transaktionsanalyse (nach Taibi Kahler). Die App hilft dabei, innere Glaubenssätze zu identifizieren, die uns im Alltag und Beruf unter Stress setzen können.

## 🚀 Live-Demo
https://antreiber-test-2brxtjjryjtctqe6scxmva.streamlit.app/

## 📋 Über den Test
Das Modell der inneren Antreiber unterscheidet fünf Ausprägungen:
*   **Sei perfekt!**
*   **Mach schnell!**
*   **Streng dich an!**
*   **Mach es allen recht!**
*   **Sei stark!**

Die App wertet 50 gezielte Fragen aus und hilft dabei, die eigenen Stressverstärker zu erkennen und durch sogenannte "Erlauber-Sätze" gegenzusteuern.

## ✨ Features
- ✅ **Interaktiver Fragebogen:** 50 Fragen mit intuitiven Schiebereglern (1-5).
- ✅ **Visuelle Auswertung:** Darstellung der Ergebnisse in einem **Radar-Chart (Netzdiagramm)**.
- ✅ **Detailliertes Feedback:** Anzeige von Glaubenssätzen und individuellen Lösungsansätzen (Erlauber).
- ✅ **PDF-Export:** Generiere eine professionelle Zusammenfassung deiner Ergebnisse als PDF-Dokument.
- ✅ **Anti-Stress-Tipps:** Erhalte basierend auf deinem höchsten Wert eine tägliche Challenge.

## 🛠 Installation (Lokal)
Falls du die App lokal auf deinem Rechner ausführen möchtest:

1. Repository klonen:
   ```bash
   git clone https://github.com/DEIN-NUTZERNAME/antreiber-test.git
   cd antreiber-test
   ```

2. Benötigte Bibliotheken installieren:
   ```bash
   pip install -r requirements.txt
   ```

3. App starten:
   ```bash
   streamlit run antreiber_full.py
   ```

## 📦 Abhängigkeiten
Die App basiert auf folgenden Python-Bibliotheken:
- `streamlit` (Web-Interface)
- `pandas` (Datenverarbeitung)
- `matplotlib` & `numpy` (Visualisierung)
- `fpdf` (PDF-Generierung)

## 🔒 Datenschutz
Der Test verarbeitet alle Daten lokal im Browser-Cache oder temporär auf dem Server. Es werden keine persönlichen Daten oder Testergebnisse dauerhaft gespeichert.

---
*Erstellt auf Basis der Transaktionsanalyse nach Taibi Kahler.*
