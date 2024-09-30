# Applicazione Insulinometro

### Gruppo O 
 - Importuna Leonardo Giovanni
 - Russo Anna
 - Terracciano Raffaele
 - Verde Francesco
### Link al prototipo
https://www.figma.com/proto/Iiyhb0qHPti0s1IfKdfc0f/Progetto-Misure?node-id=76-3124&t=0g2YE0rK646NnbU4-1

# Caratteristiche dell'applicazione
## Esperienza per l'utente
- **App responsiva**: ogni componente si adatta al ridimensionamento della finestra
- **Grafici adattivi**: ogni grafico deve essere in grado di accomodare i dati in entrata rendendoli visibili zoomando in avanti o in fuori
## Interazione con board
- Permettere **reset memoria** del dispositivo
- **Barra di avanzamento** del campionamento
- Possibilità di verificare la **batteria del dispositivo** (icona con hover): introduzione di un meccanismo di fail-save che impedisce di iniziare un campionamento se la batteria del dispositivo è troppo bassa
## Connessione con board
- Possibilità di scegliere il **metodo di connessione**
  - **Bluetooth**: poter filtrare i dispositivi (per nome/tipo e per utilizzo recente)
  - **Seriale**
- Possibilità di **disconnettere il dispositivo**
- Possibilità di verificare lo **stato della connessione** al dispositivo (icona con hover)
## Gestione dei dati
- Possibilità di **esportare i dati**
  - Excel
  - CSV
- Possibilità di iniziare un **nuovo campionamento** (creazione di un nuovo file) senza uscire dall'applicazione
## Funzionalità
- Possibilità di impostare **due punti diversi** per l'acquisizione della fase e visualizzare la differenza tra essi su un grafico

# Modalità di misura
- **Singola frequenza** (1 variabile)
  - fissata la **frequenza**, si registrano i cambiamenti della fase e del modulo
- **Sweep** (4 variabili)
  - si fissano gli **estremi dell'intervallo** delle frequenze e il **numero di punti** di esso nel quale registrare la fase e il modulo
  - si può stabilire il **numero di volte** per il quale ripetere il campionamento

# Intervallo valori
- **Frequenza**: 1-100 kHz (incremento di 1)
- **Ampiezza**: 10-500 mV (incremento di 10)

# Pulsanti per campionamento
- **Start**: inizio registrazione valori
- **Stop**: fine registrazione valori
- **Mark**: segnare un punto della registrazione per controllo in un momento successivo (indicarlo nel file)

# Sezione grafici
- 2 di **Bode** (per parte reale e immaginaria del segnale)
- 1 di **Nyquist**
- 1 per la **differenza tra i punti**
Quando il grafico ricomincia dall'inizio, quello **immediatamente precedente sbiadisce** ed inizia quello nuovo con il colore primario

# Sezione log
- **Messaggi di stato**
  - Dispositivo
  - Applicazione
- **Dati numerici** in tempo reale
