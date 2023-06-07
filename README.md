# Flask-Tic-Tac-Toe

## DOCKER IMAGE
Here is the docker image: [Docker Image](https://hub.docker.com/r/skwdebski/flask-tic-tac-toe).


Aplikacja zawiera obsługę logowania i rejestrowania użytkowników.

Gracz rozpoczyna sesję, jeśli takowej nie posiada, mając na koncie 10 kredytów.

Wchodzi do pokoju gier i czeka bądź dołącza do czekającego już przeciwnika.

Gracze grają aż do zakończenia gry wygraną jednej ze stron bądź remisem.
Rozgrywka jest prowadzona w czasie rzeczywistym bazując na *SocketIO*.

Raport z zakończonej gry trafia do bazy danych *SQL Alchemy*.

Za wygraną gracz otrzymuje 4 kredyty, a za przegraną traci 3.
Jeśli gracz po zakończeniu gry i aktualizacji bilansu kredytów posiada mniej niż 3 kredyty, to nie może rozpocząć kolejnej gry.

W takim wypadku sesja się kończy i gracz jest przekierowywany do ekranu początkowego, gdzie może rozpocząć kolejną sesję z pulą 10 kredytów.

*Możliwy jest również podgląd statystyk z danego dnia.*
