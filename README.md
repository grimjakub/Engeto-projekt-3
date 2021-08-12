# Engeto 2021 projekt 3

Třetí Python projekt do Python Akademie na Engetu

# Popis projektu

Tento projekt slouží k získání výsledků z parlamentních voleb 2017

# Instalace knihoven

Použité knihovny v tomto projektu jsou uloženy v souboru `requirements.txt.` 
Pro instalaci je vhodné použít nové virtuální prostředí a pomocí terminálu nainstalovat knihovny:

`pip install -r requirements.txt`

# Spuštění projektu

Pro spuštění souboru projekt3.py pomocí příkazového řádku v terminálu je třeba dvou argumentů pomocí příkazu:

`python projekt3.py <URL adresa uzemniho celku> <nazev csv souboru pro zapsani>
`

# Praktický příklad spuštěného projektu:

Výsledky pro okres Prostějov:

`python projekt3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv"
`

Průběh programu:

`Stahuji data z vybrané URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103`

`Ukládám výsledky do souboru: vysledky_prostejov.csv`

`Data zapsaná úspěšně do tabulky`

`Ukoncuji program projekt3.py`

Částěčný výstup programu:

`kod obce, nazev obce, voliči v seznamu, vydané obálky, platné hlasy,...
`

`506761, Alojzov, 205, 145, 144, 29, 0, 0, 9, 0, 5, 17, 4, 1, 1, 0, 0, 18, 0, 5, 32, 0, 0, 6, 0, 0, 1, 1, 15, 0
`
