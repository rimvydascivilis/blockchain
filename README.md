# Maišos funkcija
## Pseudokods
```
funkcija maišos_funkcija(įvestis):
    Sukuriamas 256 bitų ilgio bitų masyvas rezultatas = 1011001001000000101010111001001100101001000111101011000101001111010011111101010110110101010100010110110111001001101111000000111001111111110011000110001011100110000100111110010001111110001010001110110101010100101100011010010101011111100101101101001100010000

    kiekvienam simboliui iš įvesties:
        Sukuriamas 256 bitų ilgio bitų masyvas generavimo_rezultatas
        Priskiriama generavimo seed'ą = simbolio ASCII kodas * (simbolio indeksas + 0xFOODBABE)

        kiekvienam bitui j iš generavimo_rezultato:
            generavimo_rezultatas[j] = atsitiktinis bitas

        rezultatas = rezultatas XOR generavimo_rezultatas

    gražink rezultatas
```
## Programos paleidimas
1. Sukompiliuokite programą [(žr. Kompiliavimas)](#kompiliavimas)
2. Paleiskite programą
    ```
    $ ./build/main
    Usage:
    ./build/main <string_to_hash>
    ./build/main f <file_to_hash>
    ./build/main t <string_to_hash> (gives hashing time)
    ./build/main tf <file_to_hash> (gives hashing time)
    ```
## Kompiliavimas
- Optimizuotos versijos (rekomenduojama)
    ```
    $ make release
    ```
- Debug versijos
    ```
    $ make
    ```
## Testavimas
### Testų paleidimas
```
$ make test
```
### Testavimo procesas
1. Testas
    - Tikrina
      - Ar programa veikia su bet kokio ilgio string'ais
      - Ar programa grąžina 256 bitų ilgio hash'ą
      - Ar programa grąžina tą patį hash'ą, kai paleidžiama su tuo pačiu string'u (deterministinė)
    - Testavimo failai
      - 10 failų, kuriuose yra 10000 vienodų string'ų
      - 10 failų, kuriuose yra 10000 atsitiktinių string'ų
      - 10 failų, kuriuose yra 10000 atsitiktinių string'ų ir kiekvienas string'as turi vieną pakeistą simbolį
      - Tuščias failas
    - Rezultatas
      - Skaičius, kiek kartų hash'o ilgis nesutapo su 256 bitų ilgiu
      - Skaičius, kiek kartų hash'as nesutapo su hash'u, gautu paleidus programą su tuo pačiu string'u
2. Testas
    - Tikrina
      - Laiko priklausomybę nuo eilučių skaičiaus. Kiekvienas failas yra dvigubai ilgesnis už prieš tai buvusį, pradedant nuo 1 eilutės (1, 2, 4, 8, ...)
    - Testavimo failai
      - Lietuvos konstitucija (789 eilutės)
    - Rezultatas
      - Grafikas, kurio x ašis yra eilučių skaičius, o y ašis yra laikas milisekundėmis
3. Testas
    - Tikrina
      - Ar maišos funkcija atspari kolizijoms
      - Ar maišos funkcija turi lavinos efektą
    - Testavimo įvestis
      - 10, 100, 500, 1000 ilgio atsitiktinių string'ų poros, kurios skiriasi viena nuo kitos vienu simboliu. Kiekvieno ilgio string'ų porų yra po 25000
    - Rezultatas
      - Skaičius, kiek kartų buvo rasta kolizija
      - Vidutinis, mažiausias ir didžiausias hex'ų ir bitų skirtumas tarp string'ų porų hash'ų
      - Grafikas, kuris rodo, kiek vidutiniškai pasikeičia kiekvienas bitas hash'e, kai viename string'e pakeičiamas vienas simbolis

### Testavimo rezultatai
```json
[
  {
    "name": "Rimvydas Civilis",
    "not_deterministic_count": 0,
    "size_diff_count": 0,
    "collision_count": 0,
    "hashing_time": [
      {
        "lines": 1,
        "time": 0.7785736
      },
      {
        "lines": 2,
        "time": 1.1241524
      },
      {
        "lines": 4,
        "time": 1.7420578
      },
      {
        "lines": 8,
        "time": 3.114778
      },
      {
        "lines": 16,
        "time": 8.447424
      },
      {
        "lines": 32,
        "time": 15.619127999999998
      },
      {
        "lines": 64,
        "time": 31.54336
      },
      {
        "lines": 128,
        "time": 77.42084
      },
      {
        "lines": 256,
        "time": 172.37507999999997
      },
      {
        "lines": 512,
        "time": 403.09680000000003
      },
      {
        "lines": 789,
        "time": 639.5328000000001
      }
    ],
    "avg_hex_diff": 0.937374375,
    "min_hex_diff": 0.765625,
    "max_hex_diff": 1.0,
    "avg_bit_diff": 0.4999576171875,
    "min_bit_diff": 0.3515625,
    "max_bit_diff": 0.62109375
  }
]
```
### Testavimo rezultatų išvados
1. Galime paleisti programą su bet kokio ilgio string'ais ir failais, ir gauti hash'ą, programa veikia kaip tikimasi.
2. Programa visada grąžina 256 bitų ilgio hash'ą.
3. Programą paleidus su tuo pačiu string'u, hash'as visada yra tas pats.
4. Programą veikia O(n) laiku, kur n yra string'o ilgis.

    ![Maišos funkcijos laiko grafikas](/img/time.png)

5. Maišos funkcija atspari kolizijoms. Bandyta su 1000000 skirtingų string'ų, kolizijų nerasta.
6. Funkcija turi lavinos efektą. Bandyta su 1000000 skirtingų string'ų, 1 bito pakeitimas string'e vidutiniškai pakeičia 93% hex'ų ir 50% bitų.

Funkcijos stiprybės:
- Deterministinė
- Lavinos efektas

Funkcijos silpnybės:
- Ganėtinai lėta (100_000 simbolių string'as hash'uojamas ~0.5s)