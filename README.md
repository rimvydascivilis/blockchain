# Maišos funkcija
## Pseudokodas
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
[{
  "name":"Rimvydas Civilis",
  "not_deterministic_count":0,
  "size_diff_count":0,
  "collision_count":0,
  "hashing_time":[{"lines":1,"time":0.769491},{"lines":2,"time":1.0308778},{"lines":4,"time":1.6383412},{"lines":8,"time":2.8493539999999995},{"lines":16,"time":7.812054000000001},{"lines":32,"time":14.444640000000001},{"lines":64,"time":29.75768},{"lines":128,"time":71.40061999999999},{"lines":256,"time":159.45337999999998},{"lines":512,"time":371.11600000000004},{"lines":789,"time":592.8882}],
  "avg_hex_diff":0.93744546875,
  "min_hex_diff":0.765625,
  "max_hex_diff":1,
  "avg_bit_diff":0.4999525,
  "min_bit_diff":0.3515625,
  "max_bit_diff":0.6328125,
  "bit_diff_distr":[0.49899,0.49542,0.50409,0.50006,0.50108,0.50115,0.50031,0.50071,0.50085,0.4987,0.50256,0.5026,0.50231,0.50103,0.49698,0.50101,0.49916,0.50129,0.50188,0.50122,0.50074,0.50002,0.5028,0.50275,0.50246,0.49897,0.50053,0.49932,0.50034,0.49965,0.50257,0.49801,0.49876,0.50001,0.49917,0.50197,0.4998,0.50071,0.49926,0.49987,0.49963,0.4977,0.49821,0.50414,0.5004,0.50123,0.5017,0.49921,0.4985,0.49954,0.49893,0.5033,0.49945,0.50101,0.5005,0.49996,0.49916,0.49933,0.5019,0.4956,0.4979,0.50084,0.50014,0.50011,0.50024,0.49948,0.50003,0.49862,0.49648,0.49967,0.50044,0.50168,0.50062,0.49793,0.50023,0.4993,0.50157,0.49682,0.50145,0.50229,0.49902,0.49957,0.50065,0.4973,0.4997,0.49844,0.50184,0.5015,0.49962,0.49944,0.50142,0.50418,0.49964,0.49987,0.50078,0.50186,0.49846,0.49867,0.50028,0.49879,0.5011,0.49968,0.49899,0.50256,0.4997,0.49626,0.50099,0.49967,0.49981,0.49994,0.49937,0.50061,0.49802,0.49878,0.50072,0.50017,0.49895,0.50158,0.49804,0.49877,0.49945,0.501,0.49992,0.50055,0.49924,0.49689,0.50188,0.50149,0.49705,0.50141,0.50066,0.50192,0.49914,0.50218,0.49915,0.49896,0.49738,0.50126,0.49794,0.50299,0.50008,0.49895,0.49897,0.49928,0.50305,0.50158,0.49847,0.4986,0.49885,0.50268,0.49963,0.49676,0.49858,0.49904,0.50331,0.50277,0.498,0.49805,0.49978,0.50272,0.5015,0.49843,0.49968,0.50103,0.49884,0.49964,0.50067,0.5017,0.50076,0.49921,0.50078,0.50162,0.50045,0.49866,0.49942,0.50291,0.49807,0.4992,0.49761,0.49992,0.50238,0.49904,0.50125,0.49866,0.50034,0.49854,0.49827,0.49808,0.4997,0.50003,0.50061,0.49842,0.49919,0.49838,0.50013,0.49748,0.49758,0.50178,0.49974,0.49811,0.50079,0.49994,0.50188,0.49846,0.49947,0.49375,0.49998,0.50098,0.50323,0.49528,0.4959,0.49888,0.50231,0.4998,0.498,0.5033,0.49797,0.50286,0.49973,0.50266,0.50158,0.49942,0.49855,0.50025,0.50017,0.50079,0.49836,0.49927,0.49709,0.50152,0.50048,0.49972,0.49951,0.50278,0.49779,0.50242,0.50084,0.49822,0.4996,0.49931,0.49823,0.50051,0.49954,0.49763,0.49868,0.49871,0.50124,0.50191,0.50083,0.50064,0.4977,0.49996,0.4997,0.4993,0.50401,0.4999],
  "no_bits":256
}]
```
### Testavimo rezultatų išvados
1. Galime paleisti programą su bet kokio ilgio string'ais ir failais, ir gauti hash'ą, programa veikia kaip tikimasi.
2. Programa visada grąžina 256 bitų ilgio hash'ą.
3. Programą paleidus su tuo pačiu string'u, hash'as visada yra tas pats.
4. Programą veikia O(n) laiku, kur n yra string'o ilgis.

    ![Maišos funkcijos laiko grafikas](/img/time.png)

5. Maišos funkcija atspari kolizijoms. Bandyta su 1000000 skirtingų string'ų, kolizijų nerasta.
6. Funkcija turi lavinos efektą. Bandyta su 1000000 skirtingų string'ų, 1 simbolio pakeitimas string'e vidutiniškai pakeičia 94% hex'ų ir 50% bitų.
7. Hash'o skirtingų bit'ų pasiskirstymas:

    ![Maišos funkcijos skirtingų bitų pasiskirstymas](/img/bit_diff_dist.png)

Funkcijos stiprybės:
- Deterministinė
- Lavinos efektas

Funkcijos silpnybės:
- Ganėtinai lėta (100_000 simbolių string'as hash'uojamas ~0.5s)

## Palyginimas su SHA-1, SHA-256, MD5

### Hash'inimo laikai

![Hash'inimo laikai](/img/compare_time.png)

### Hash'o bit'ų, hex'ų skirtumai pasikeitus vienam simboliui

![Hash'o bit'ų, hex'ų skirtumai pasikeitus vienam simboliui](/img/compare_diff.png)

### Kiekvieno hash'o bit'o skirtumo procentas

![Kiekvieno hash'o bit'o skirtumo procentas](/img/compare_bit_diff.png)