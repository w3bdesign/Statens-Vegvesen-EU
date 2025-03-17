# EU-kontroll Statistikk / EU Control Statistics

[English](#english) | [Norsk](#norsk)

## Norsk

### Om Prosjektet
Dette prosjektet analyserer data fra EU-kontroller i Norge for å hjelpe folk å ta informerte valg når de skal kjøpe bil. Ved å analysere resultater fra periodiske kjøretøykontroller, identifiserer systemet hvilke bilmerker og modeller som har best og dårligst resultat på EU-kontroll.

### Hovedfunksjoner
- Viser topp 20 mest pålitelige biler basert på EU-kontroll resultater
- Viser bunn 20 minst pålitelige biler
- Søkefunksjon for spesifikke bilmerker og modeller
- Statistikk inkluderer:
  - Godkjenningsrate
  - Gjennomsnittlig antall alvorlige feil (kode 2 og 3)
  - Antall kontroller per modell

### Installasjon og Kjøring
1. Klon repositoriet
2. Opprett et Python virtuelt miljø:
   ```bash
   python -m venv venv
   ```
3. Aktiver miljøet:
   - Windows: `.\venv\Scripts\activate`
   - Unix/macOS: `source venv/bin/activate`
4. Installer avhengigheter:
   ```bash
   pip install -r requirements.txt
   ```
5. Prosesser dataene:
   ```bash
   cd src
   python process_data.py
   ```
6. Start webapplikasjonen:
   ```bash
   python app.py
   ```
7. Åpne nettleseren på `http://localhost:5000`

### Datakilde
Dataene er hentet fra Statens Vegvesens åpne datasett for periodiske kjøretøykontroller. Denne versjonen bruker data fra første kvartal 2023.

---

## English

### About the Project
This project analyzes vehicle inspection (EU-kontroll) data from Norway to help people make informed decisions when buying a car. By analyzing periodic vehicle inspection results, the system identifies which car makes and models perform best and worst in these inspections.

### Key Features
- Shows top 20 most reliable vehicles based on inspection results
- Shows bottom 20 least reliable vehicles
- Search functionality for specific makes and models
- Statistics include:
  - Approval rate
  - Average number of serious faults (code 2 and 3)
  - Number of inspections per model

### Installation and Running
1. Clone the repository
2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the environment:
   - Windows: `.\venv\Scripts\activate`
   - Unix/macOS: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Process the data:
   ```bash
   cd src
   python process_data.py
   ```
6. Start the web application:
   ```bash
   python app.py
   ```
7. Open your browser at `http://localhost:5000`

### Data Source
The data is sourced from the Norwegian Public Roads Administration's (Statens Vegvesen) open dataset for periodic vehicle inspections. This version uses data from Q1 2023.

---

## Future Development
- Integration with AI for natural language queries
- Support for multiple quarters of data
- Advanced filtering options
- Detailed fault analysis per vehicle model
- Integration with vehicle price data
