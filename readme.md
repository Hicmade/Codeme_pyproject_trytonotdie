TryToNotDie
===========

W pierwszym kroku należy zainicjować bazę danych do przechowywania danych gry - uruchamiając **"database_init.py"** w głównym katalogu.
Następnie aplikację uruchamia się plikiem **"serv.py"**.

TryToNotDie jest grą przeglądarkową. Gracz otrzymuje 4 lub więcej postaci, które musi utrzymać przy życiu przez
określoną ilosć dni.
Każda postać ma predefiniowaną z góry lub losowo przydzielaną profesję, która z kolei ma wpływ na poszczególne zdolności postaci:
* zdolność regenereacji zdrowia
* tempo ubytku zdrowia
* zdolność samolecznia
* konsumpcja pożywienia
* efektywność zdobywania pożywienia
* odporność na ekstremalne warunki pogodowe
* umiejętność budowania
* zdolność zbierania ziół
* punkty życia

Czynnikiem koniecznym do utrzymania na możliwie wysokim poziomie są punkty życia. Gdy spadną do 0, postać ginie i 
przestaje być dostępna w rozgrywce. Każdego dnia, każda z postaci może wg. uznania gracza wykonać jedną z czterech 
czynności:
* zbierać żywność
* zbierać zioła lecznicze
* budować schronienia (maksymalnie tyle ile jest postaci)
* leczyć siebie (konsumując zioła)

Kliknięcie przycisku "next day" powoduje wykonanie akcji każdej z postaci i odpowiednie zwiększenie ogólnych zasobów 
grupy lub zużycie ziół i zwiększenie punktów życia postaci która tą czynność wykonała.
Dodatkowo w tym momencie następuje zmiana pogody. Losowo w ograniczonych przedziałach skoku generuje się temperatura, 
oraz warunki atmosferyczne: wiatr, deszcz. Zbyt wysoka lub zbyt niska temperatura prowadzi do większego ubytku punktów 
życia postaci przy uwzględnieniu jej osobistej odporności. Tak samo silne wiatry lub silne deszcze zwiększają ubytek 
punktów zdrowia.

Schronienia łagodzą skutki złych warunków atmosferycznych proporcjonalnie do ilości wybudowanych schornień. Dodatkowo 
silne wiatry lub deszcze niszczą systematycznie schornienia, które można odbudować przydzielając właściwą akcję do 
wykonania postaci.

Gra na każdym etapie wyświelania treści html pobiera aktualny stan (tj. wszystkie niezbędne parametry) z bazy danych
identyfikując dane po unikalnym ID gry oraz uaktualnia ten rekord.

Dodatkowe informacje
--------------------
Gra wykorzystuje:
* Flask
* Jinja2
* Sqlite3
* python 3.8

pip install -r requirements.txt

Dodatkowe informacje
--------------------
Autor: Bartosz Kozikowski [Hicmade]
Mail: kozikowski.bartosz@gmail.com

_Pozostało do zrobienia:_
* Hashowanie hasła - za późno weszło, za dużo przerabiania :/

Kiedyś:
* Porządnie przetestować narzucone parametry / wyważyć grę (testy, testy, testy)
* Dodać prostą grafikę



