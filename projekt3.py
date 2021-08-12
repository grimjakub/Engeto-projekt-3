import requests
import sys
from bs4 import BeautifulSoup
import csv

# url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"  # prostějov
# nazev_csv = "vysledky_prostejov.csv"

csv_tabulka = ["kod obce", "nazev obce", "voliči v seznamu", "vydané obálky",
               "platné hlasy"]  # ,"kandidující strany"]

tabulka = []


def get_soup(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def ziskat_vysledky(url):
    soup = get_soup(url)
    print("Stahuji data z vybrané URL:", url)
    ## Vytahnu cislo obce a jmeno obce
    i = 0
    while True:
        i += 1
        new_radek = []
        if i>5:
            break
        if soup.select("tr")[i].text.split("\n")[1] == "-":
            break
        if not str(soup.select("tr")[i].text.split("\n")[1]).isdigit():
            continue

        cislo = soup.select("tr")[i].text.split("\n")[1]
        mesto = soup.select("tr")[i].text.split("\n")[2]
        new_radek.append(cislo)  # cislo
        new_radek.append(mesto)  # nazev
        hledam_odkazy = soup.select("tr")[i].select("a")[0].get("href")

        new_url = "https://volby.cz/pls/ps2017nss/" + (
            hledam_odkazy)  # odkaz z cisla
        new_soup = get_soup(new_url)

        ## z jednotlivych odkazu taham udaje z vrchni tabulky
        vysledky = new_soup.select("td.cislo")
        new_radek.append(vysledky[3].text)  # voliči v seznamu
        new_radek.append(vysledky[4].text)  # vydané obálky
        new_radek.append(vysledky[7].text)  # platné hlasy

        strany = []
        ## Z prvniho odkazu vytaham nazvy stran a pak vysledky pro jednotlive strany ze vsech odkazu
        for j in (range(5, 32)):
            if j not in range(18, 20):
                strany.append(new_soup.select("tr")[j].text.split("\n")[2])
                if i == 2:
                    csv_tabulka.append(
                        new_soup.select("tr")[j].text.split("\n")[2])
                new_radek.append(new_soup.select("tr")[j].text.split("\n")[3])
        tabulka.append(new_radek)


# def jmena_stran(new_soup):
#     for i in (range(5, 32)):
#         if i not in range(18, 20):
#             csv_tabulka.append(new_soup.select("tr")[i].text.split("\n")[2])


def zapsat_data(filename):
    print("Ukládám výsledky do souboru:", filename)
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(csv_tabulka)
        for radek in tabulka:
            writer.writerow(radek)
    print("Data zapsaná úspěšně do tabulky")


def main():
    try:
        url=sys.argv[1]
        nazev_csv=sys.argv[2]
        get_soup(url)
    except:
        print(
            "Musíte zadat správnou URL adresu a název CSV souboru\n---EXIT---")
        exit()
    if "Page not found" in get_soup(url).select("h3")[0].text or nazev_csv[
                                                                 -4:] != ".csv":
        print(
            "Musíte zadat správnou URL adresu a název CSV souboru\n---EXIT---")
        exit()
    ziskat_vysledky(url)
    zapsat_data(nazev_csv)


if __name__ == "__main__":
    main()
