import re
from collections import Counter

def tokenizuj(tekst):
    return re.findall(r'\b\w+\b', tekst.lower())

def czest_dok(dokumenty):
    return [Counter(tokenizuj(dokument)) for dokument in dokumenty]

def czest_korpusu(czestotliwosci_dokumentow):
    czestotliwosci_korpusu = Counter()
    for czestotliwosci in czestotliwosci_dokumentow:
        czestotliwosci_korpusu.update(czestotliwosci)
    return czestotliwosci_korpusu

def podobienstwo_zapytania(czestotliwosci_dokumentow, czestotliwosci_korpusu, zapytanie, lambda_wartosc=0.5):
    tokeny_zapytania = tokenizuj(zapytanie)
    wyniki = []

    for czestotliwosci_dokumentu in czestotliwosci_dokumentow:
        wynik = 1
        dlugosc_dokumentu = sum(czestotliwosci_dokumentu.values())
        dlugosc_korpusu = sum(czestotliwosci_korpusu.values())

        for token in tokeny_zapytania:
            prawd_doc = czestotliwosci_dokumentu[token] / dlugosc_dokumentu if dlugosc_dokumentu else 0
            prawd_korpus = czestotliwosci_korpusu[token] / dlugosc_korpusu if dlugosc_korpusu else 0
            wynik *= lambda_wartosc * prawd_doc + (1 - lambda_wartosc) * prawd_korpus

        wyniki.append(wynik)

    return wyniki

def posortuj_dok(dokumenty, zapytanie):
    czestotliwosci_dokumentow = czest_dok(dokumenty)
    czestotliwosci_korpusu = czest_korpusu(czestotliwosci_dokumentow)
    wyniki = podobienstwo_zapytania(czestotliwosci_dokumentow, czestotliwosci_korpusu, zapytanie)
    return [indeks for indeks, wynik in sorted(enumerate(wyniki), key=lambda x: x[1], reverse=True)]

# Główna funkcja programu
def main():

    liczba_dokumentow = int(input().strip())

    dokumenty = []
    for i in range(liczba_dokumentow):
        dokument = input().strip()
        dokumenty.append(dokument)

    zapytanie = input().strip()

    wynik = posortuj_dok(dokumenty, zapytanie)
    print(wynik)

if __name__ == "__main__":
    main()
