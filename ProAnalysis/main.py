import yfinance as yf
import math

spolki = ["XTB.WA", "LPP.WA", "SNT.WA", "ACP.WA", "ASB.WA", "VRC.WA", "CBF.WA", "PAS.WA", "MBR.WA", "PKN.WA",
          "ALE.WA","BDX.WA","KGH.WA","CPS.WA", "CDR.WA", "DNP.WA"
          ]

def pobierz_dane(tryb_treningu=False):
    result = {}

    for ticker in spolki:

        try:
            #---------------------------------------Dane z yfinance---------------------------------------#

            spolka = yf.Ticker(ticker)

            historia_cen = spolka.history(period="5y")

            zyski = spolka.financials.loc["Net Income"]
            przychody = spolka.financials.loc["Total Revenue"]
            zyski_operacyjne = spolka.financials.loc["Operating Income"]
            eps = spolka.financials.loc["Basic EPS"]

            dlug = spolka.balance_sheet.loc["Total Debt"]
            kapital_wlasny = spolka.balance_sheet.loc["Stockholders Equity"]

            zysk_netto_roe = spolka.financials.loc["Net Income"]

            fcf = spolka.cashflow.loc["Free Cash Flow"]

            #-------------------------------------Ustawienie czasu----------------------------------------#
        
            if tryb_treningu:
                i = 1        
                lata = 2     
            else:
                i = 0        
                lata = 3     

            #-------------------------------------Liczenie wskaznikow-------------------------------------#

            marza = (zyski_operacyjne / przychody) * 100

            aktualna_marza = marza.iloc[i]

            zmiana_marzy = (marza.iloc[i] - marza.iloc[3]) / lata

            dynamika_zysku = ((zyski.iloc[i] - zyski.iloc[3]) / abs(zyski.iloc[3]) * 100) / lata

            dynamika_przychodow = ((przychody.iloc[i] - przychody.iloc[3]) / abs(przychody.iloc[3]) * 100) / lata

            wskaznik_zadluzenia = dlug.iloc[i] / kapital_wlasny.iloc[i]

            roe = (zysk_netto_roe.iloc[i] / kapital_wlasny.iloc[i]) * 100

            wolny_przeplyw = fcf.iloc[i]/abs(zyski.iloc[i])

            #----------------------------------------Odchylenie C/Z---------------------------------------#

            ceny_close = historia_cen["Close"]
       
            data_startu = str(spolka.financials.columns[3].date())
        
            if tryb_treningu:
                data_decyzji = str(spolka.financials.columns[1].date())
                ceny_okres = ceny_close.loc[data_startu : data_decyzji]
            else:
                ceny_okres = ceny_close.loc[data_startu :]

            aktualna_cena = ceny_okres.iloc[-1]
            srednia_cena = ceny_okres.mean()

            aktualny_eps = eps.iloc[i]
            sredni_eps = (eps.iloc[i] + eps.iloc[i+1] + eps.iloc[i+2]) / 3

            cz_biezace = aktualna_cena / aktualny_eps
            cz_srednie = srednia_cena / sredni_eps

            odchylenie_cz = ((cz_biezace - cz_srednie) / cz_srednie) * 100

            #------------------------------Czy wartosci wskaznikow sa Nan----------------------------------#

            if math.isnan(odchylenie_cz) or math.isnan(zmiana_marzy) or math.isnan(dynamika_zysku) or math.isnan(dynamika_przychodow) or math.isnan(wskaznik_zadluzenia) or math.isnan(roe) or math.isnan(aktualna_marza) or math.isnan(wolny_przeplyw):
                raise ValueError("Wykryto brakujące dane (NaN)!")

            #--------------------------------------------Wynik--------------------------------------------#

            result[ticker] = {
                "odchylenie_cz": odchylenie_cz,
                "zmiana_marzy": zmiana_marzy,
                "dynamika_zysku": dynamika_zysku,
                "dynamika_przychodow": dynamika_przychodow,
                "wskaznik_zadluzenia": wskaznik_zadluzenia,
                "roe": roe,
                "aktualna_marza": aktualna_marza,
                "wolny_przeplyw": wolny_przeplyw
            }

            if tryb_treningu:
                data_sprawdzianu = str(spolka.financials.columns[0].date())
                cena_po_roku = ceny_close.loc[data_decyzji : data_sprawdzianu].iloc[-1]
                zwrot_z_akcji = ((cena_po_roku - aktualna_cena) / aktualna_cena) * 100
                result[ticker]["zwrot_z_akcji"] = zwrot_z_akcji

        except Exception as e:
            print(f"Pominięto spółkę {ticker} -> Powód: {e}")

    return result


result_trening = pobierz_dane(tryb_treningu=True)   
result = pobierz_dane(tryb_treningu=False)        