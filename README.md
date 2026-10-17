# ProAnalysis - Autonomiczny System AI do Analizy Fundamentalnej GPW

Zaawansowany system analityczny napisany w języku Python, łączący uczenie maszynowe z zasadami analizy fundamentalnej i ekonomicznej dla spółek z Giełdy Papierów Wartościowych (GPW).

## O projekcie
Projekt powstał w celu automatyzacji oceny atrakcyjności inwestycyjnej spółek giełdowych. System pobiera dane finansowe w czasie rzeczywistym, przetwarza je przez model optymalizujący wagi wskaźników, a następnie generuje rzetelny ranking spółek od najlepszej do najsłabszej.

## Kluczowe Wskaźniki Finansowe
Model analizuje spółki w oparciu o zróżnicowany zestaw wskaźników jakościowych i rynkowych:
- Wycena: Odchylenie wskaźnika C/Z od średniej rynkowej.
- Rentowność: ROE (Return on Equity) oraz aktualna marża operacyjna.
- Dynamika: Dynamika zysku oraz dynamika przychodów na przestrzeni lat.
- Jakość zysku: Wskaźnik konwersji wolnych przepływów pieniężnych (FCF / Zysk Netto).
- Zadłużenie: Wskaźnik ogólnego zadłużenia spółki.

## Architektura i Zabezpieczenia Inżynieryjne
- Kaganiec Logiczny (core.py): Autorski mechanizm kontroli wag, który uniemożliwia sztucznej inteligencji odwracanie praw ekonomii (dług i wysoka wycena nie mogą być nagradzane, a kluczowe filary rentowności i FCF nie mogą być karane).
- Strażnik Anti-NaN (main.py): Zabezpiecza proces obliczeniowy przed przerwaniem lub skażeniem wag przez brakujące sprawozdania finansowe.
- Trwałość stanu: Automatyczny zapis i odczyt zoptymalizowanych wag modelu z pliku konfiguracyjnego wagi_modelu.json.

## Technologie
- Język: Python
- Biblioteki: yfinance (pobieranie danych giełdowych), obsługa struktur matematycznych i pliki JSON.
- Środowisko: Visual Studio

## Struktura Projektu
- main.py - Główny skrypt odpowiedzialny za konfigurację spółek, pobieranie danych i uruchamianie silnika.
- core.py - Logika matematyczna modelu, algorytm uczenia, kagańce logiczne oraz generowanie rankingu.
- wagi_modelu.json - Trwały magazyn wyuczonych wag.

