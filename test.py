def sve(funkcija):
    try:
        prvi = int(input('Unesite prvi broj: '))
        drugi = int(input('Unesite drugi broj: '))
    except ValueError:
        print('Niste upisali broj.\nProgram sada izlazi')
        return
    else:
        if funkcija == '1':
            ukupno = prvi + drugi
        if funkcija == '2':
            ukupno = prvi - drugi
        if funkcija == '3':
            ukupno = prvi * drugi
        if funkcija == '4':
            ukupno = prvi / drugi
        print(f'Rezultat je: {ukupno}')

# Ovo je komentar, ovo program ne čita a tebi olakšava koentiranje koda

## Odkomentiraj ovo za pokretanje kalkulatora 4 puta (makni di ima jedan # sa pocetka linije)
#for nesto in range(4):
#    izbor = input('Odaberite fuknciju kalkulatora unosom broja fukcije\n1 - zbrajanje\n2 - oduzimanje\n3 - množenje\n4 - djeljenje\n')
#    sve(izbor)

## Odkomentiraj ovo za pokretanje kalkulatora zauvjek (makni di ima jedan # sa pocetka linije) - za zaustavljanje ovako skripte koja se pokreće zauvjek stisni CTRL+D
#while True:
#    izbor = input('Odaberite fuknciju kalkulatora unosom broja fukcije\n1 - zbrajanje\n2 - oduzimanje\n3 - množenje\n4 - djeljenje\n')
#    sve(izbor)