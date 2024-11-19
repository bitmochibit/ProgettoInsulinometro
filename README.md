# Progetto Insulinometro
Progetto per il laboratorio di misure del GRUPPO O

### Come utilizzare l'app
Per utilizzare il progetto base, quindi l'applicazione con il front-end e backend basta
eseguire lo script in app\main.py; i requirements si trovano all'interno del file "requirements.txt", possibilmente installare tutte le dipendenze su una venv, se si vuole poi testare il server.

### Come testare il server?
Bisogna creare una venv con la versione di python 3.9 (testata) fino alla 3.11; dalla 3.12 in poi da problemi la libreria "bless" usata per hostare un server GATT su qualsiasi sistema operativo.

### ⚠️ PER HOSTARE SU WINDOWS INSTALLARE LE [BUILD TOOLS DI MICROSOFT](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)

> Nella venv dedicata al server installare **bless**
> ``` pip install bless ```

Dopo aver installato bless, se non si e' installato da solo, occorre installare **bleak**
> Installazione di **bleak** ``` pip install bleak```

Dopo occorre installare **pysetupdi** con il seguente comando:

> installazione di **pysetupdi**
> 
> ```pip install git+https://github.com/gwangyi/pysetupdi.git```
