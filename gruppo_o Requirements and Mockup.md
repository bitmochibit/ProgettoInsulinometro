# Applicazione Insulinometro

### Gruppo O 
 - Importuna Leonardo Giovanni
 - Russo Anna
 - Terracciano Raffaele
 - Verde Francesco

# Requisiti
- L'applicazione deve essere responsiva, ovvero deve reagire al ridimensionamento della finestra e adattare i componenti.
- Il dato prelevato è un numero immaginario e viene visualizzato in due grafici:
    - Diagramma di Nyquist (modulo e fase uniti in un unico grafico)
    - Diagramma di Bode (modulo e fase in due grafici separati)
- Stampare i dati in tempo reale anche in formato numerico
- Pulsante per iniziare il prelievo dei dati
- Pulsante per fermare il prelievo dei dati
- Pulsante per svuotare il buffer sul dispositivo
- Pulsante per marcare un punto di riferimento (utile per confrontare i dati)
- 3 modalità di campionamento:
    - [Singola misura](#Singola-misura) (frequenza fissa : regolabile)
    - [Range di frequenze parametrico](#range-di-frequenze-parametrico) (frequenza iniziale, frequenza finale)
    - [Modalità sweep](#modalità-sweep): Campionamento in un breve intervallo
        - Barra di caricamento per visualizzare lo stato del campionamento (avanzamento in misura)
- Connettività con il dispositivo
    - Bluetooth (BLE) o Seriale
    - Possibilità di scegliere quale metodo di connessione usare
    - Possibilità di scegliere il dispositivo con cui connettersi (filtrato) (magari avere in alto "dispositivi utilizzati di recente")
    - Possibilità di disconnettersi dal dispositivo
    - Possibilità di riconnettersi al dispositivo
    - Possibilità di visualizzare lo stato della connessione
- Fail-safe: Verificare il livello di carica della batteria del dispositivo prima di iniziare il campionamento
- Possibilità di esportare i dati in formato Excel o CSV
- Possibilità di iniziare un nuovo campionamento senza chiudere l'applicazione
- Aggiungere un visualizattore della batteria del dispositivo
- Aggiungere un visualizzatore della qualità del segnale
- Quando la misurazione riprende dalla frequenza iniziale, il grafico si ripete preservando SOLO quello subito precedente (più sbiadito) sul quale viene mostrata la nuova misurazione per confrontare i dati
- Punti diversi per l'acquisizione della fase (punto 1, punto 2, differenza)


    
## Specifiche
### Singola misura
- Il range di frequenza è compreso tra 1 Hz a 100 Hz, incrementi di 1 (numero intero)

### Range di frequenze parametrico
- Il range di frequenza è compreso tra 1 Hz a 100 Hz, incrementi di 1 (numero intero)
- Ampiezza da 10 mV a 500 mV (incrementi di 10 mV) (numero intero)

### Modalità sweep
- Possibilità di ripetere il campionamento per un numero di volte definito dall'utente
- Scegliere quante frequenze campionare (numero intero)
- Spaziatura fra le frequenze fissa (logaritmica)

# Mockup
