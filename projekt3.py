import requests
import sys
from bs4 import BeautifulSoup
import csv
import pandas as pd

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
    odkazy = stahnout_odkazy(soup)
    cisla = uzemni_celek(url)[0]
    obce = uzemni_celek(url)[1]
    jmena_stran(odkazy[0])
    for i in range(len(cisla)):
        new_radek = []
        new_radek.append(cisla[i])
        new_radek.append(obce[i])
        new_radek += jednotlive_obce(odkazy[i])
        tabulka.append(new_radek)


def jmena_stran(new_url):
    data_obce = pd.read_html(new_url, encoding='utf-8')
    vysledky = data_obce[1].values.tolist() + data_obce[2].values.tolist()
    for radek in vysledky:
        if radek[0] != "-":
            csv_tabulka.append(radek[1])


def jednotlive_obce(new_url):
    data_obce = pd.read_html(new_url, encoding='utf-8')
    info = data_obce[0].values.tolist()
    vysledek = [info[0][3], info[0][4], info[0][7]]
    vysledky = data_obce[1].values.tolist() + data_obce[2].values.tolist()
    for radek in vysledky:
        if radek[0] != "-":
            vysledek.append(radek[2])
    return vysledek


def stahnout_odkazy(soup):
    odkazy = soup.find_all("tr")
    links = []
    for odkaz in odkazy:
        try:
            links.append(
                "https://volby.cz/pls/ps2017nss/" + odkaz.select("a")[0].get(
                    "href"))
        except:
            pass
    return links


def uzemni_celek(url):
    cisla = []
    obce = []
    info = (pd.read_html(url, encoding='utf-8'))
    for sloupec in info:
        for sl in sloupec.values.tolist():
            if sl[0] != "-":
                cisla.append(sl[0])
                obce.append(sl[1])
    return [cisla, obce]


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
        url = sys.argv[1]
        nazev_csv = sys.argv[2]
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
