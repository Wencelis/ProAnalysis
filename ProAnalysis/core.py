from main import result, result_trening
import json


class ModelFundamentalny:

    #------------------------------------Wyciaganie wag z json-----------------------------------------------#

    def __init__(self):
        with open("wagi_modelu.json", "r") as file: 
            self.wagi = json.load(file)

    #-------------------------Funckja oceniajaca czy spolka jest jakosciowa-----------------------------------#


    def ocena_spolki(self, dane_spolki):
        ocena = 0
        for nazwa_wskaznika, waga in self.wagi.items():
            wartosc = dane_spolki[nazwa_wskaznika]
            ocena += wartosc * waga
        return ocena
    
    #------------------------Funkcja poprawiajaca wagi wspolczynnikow------------------------------------------#

    def workouts(self, dane_treningowe, epoki = 1000, learning_rate = 0.000001):
        for epoka in range(epoki):
            for ticker, dane_spolki in dane_treningowe.items():
                ocena = self.ocena_spolki(dane_spolki)
                rzeczywisty_zwrot = dane_spolki["zwrot_z_akcji"]
                blad = rzeczywisty_zwrot - ocena

                for nazwa_wskaznika in self.wagi:
                    wartosc = dane_spolki[nazwa_wskaznika]
                    self.wagi[nazwa_wskaznika] += learning_rate * blad * wartosc

                    if nazwa_wskaznika in ["odchylenie_cz", "wskaznik_zadluzenia"]:
                        if self.wagi[nazwa_wskaznika] > 0:
                            self.wagi[nazwa_wskaznika] = 0.0
                    else:
                        if self.wagi[nazwa_wskaznika] < 0:
                            self.wagi[nazwa_wskaznika] = 0.0

        with open("wagi_modelu.json", "w") as plik:
            json.dump(self.wagi, plik, indent=4)

    #-------------------------Funkcja wypisujaca nam wynik------------------------------------------------------#

    def ranking(self,result):
        wynik = {}
        for ticker, dane_jednej_spolki in result.items():
            wynik[ticker] = self.ocena_spolki(dane_jednej_spolki)
        return wynik

model = ModelFundamentalny()
model.workouts(result_trening)

wynik_rankingu = model.ranking(result)

posortowany_ranking = sorted(wynik_rankingu.items(), key=lambda x: x[1], reverse=True)

print("--- RANKING SPÓŁEK PO TRENINGU ---")
for miejsce, (ticker, punkty) in enumerate(posortowany_ranking, 1):
    print(f"{miejsce}. {ticker} | Wynik: {punkty:.2f} pkt")