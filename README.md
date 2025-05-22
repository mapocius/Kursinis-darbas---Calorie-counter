Matas Augustas Pocius EDIf-24/2
Kursinis darbas

CALORIE COUNTER

1. Įvadas
   Šiame darbe sukūriau kalorijų skaičiuoklės programą, paremtą objektinio programavimo principais. Sistema leidžia vartotojui apskaičiuoti dienos kalorijų suvartojimą, pagal įvestą maistą, bei palyginti jį su individualiu kalorijų palaikymo lygiu. Programoje realizuotos visos reikalaujamos objektinio programavimo sąvokos: klasės, inkapsuliacija, paveldėjimas, metodų perrašymas, polimorfizmas, kompozicija, agregacija ir vienas dizaino šablonas.

2.  Klasių struktūra ir objektai
   Naudotos klasės:
- Food – saugo maisto produkto pavadinimą ir maistines medžiagas.
- DailyIntake – saugo vienos dienos maisto produktų sąrašą.
- Person – abstrakti bazinė klasė, skirta vartotojui.
- User – paveldėta klasė, perrašo kalorijų skaičiavimo metodą.
- UserData – saugo vartotojo dienos įrašų istoriją.
- FoodFactory – maisto kūrimo klasė, naudojanti Factory dizaino šabloną.

3. Inkapsuliacija
   Privatūs atributai (__weight, __height, __age, __activity_level) klasėje Person saugomi nuo tiesioginės prieigos. Prie jų prieinama per „getter“ ir „setter“ metodus (get_weight, set_weight, ir t.t.).

4. Paveldėjimas ir metodų perrašymas
   Klasė User paveldi iš Person ir perrašo abstraktų metodą calculate_maintenance_calories. Taip pasiekiamas dinamiškas elgesys – skirtingos Person atmainos gali skirtingai apskaičiuoti kalorijas.

5. Polimorfizmas
   Funkcija show_maintenance(user: Person) demonstruoja polimorfizmą: priima bet kokį objektą, paveldintį Person, ir kviečia metodą calculate_maintenance_calories, nepriklausomai nuo konkretaus tipo.

6. Kompozicija ir agregacija
    - Kompozicija: DailyIntake turi sąrašą Food objektų – tai stiprus ryšys, kai dienos įrašai egzistuoja tik kaip dalis visumos.
    - Agregacija: UserData turi nuorodą į User objektą ir sąrašą DailyIntake – šie objektai egzistuoja atskirai.

7. Dizaino šablonas: Factory
   Klasė FoodFactory įgyvendina Factory dizaino šabloną, leidžiantį kurti Food objektus centralizuotai per metodą create_food.

8. Programos veikimas
   Vartotojas įveda savo duomenis (svorį, ūgį, amžių, aktyvumo lygį), po to kasdien įveda suvalgyto maisto pavadinimus ir jų maistines vertes. Programa apskaičiuoja bendrą kalorijų kiekį ir lygina jį su palaikymo norma. Visi įrašai saugomi ir pateikiami vartotojo istorijoje.

9. Išvados
    Sukurtas kalorijų skaičiuotuvas sėkmingai įgyvendina visus objektinio programavimo principus. Projektas demonstruoja tiek teorinių žinių pritaikymą, tiek praktinį gebėjimą kurti struktūrizuotą, išplečiamą programinį kodą.
