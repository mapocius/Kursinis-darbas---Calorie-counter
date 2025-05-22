# Calorie Counter

**Kursinis darbas – objektinis programavimas**  
**Autorius:** Matas Augustas Pocius (EDIf-24/2)  
**Metai:** 2025  

---

## 1 Įvadas

**Calorie Counter** – komandinės eilutės (CLI) programa, skirta:

* apskaičiuoti individualų paros kalorijų palaikymo (*maintenance*) poreikį;  
* registruoti dienos maisto produktus;  
* stebėti bendrą suvartotų kalorijų kiekį ir palyginti jį su palaikymo norma;  
* išsaugoti / įkelti mitybos istoriją **CSV** faile;  
* paleisti vienetų testus, tikrinančius pagrindinių funkcijų teisingumą.

Projektas realizuoja visus keturis OOP ramsčius, naudoja **Factory Method** dizaino šabloną bei pateikia kompozicijos ir agregacijos pavyzdžius.

---

## 2 Diegimas ir paleidimas

```bash
git clone https://github.com/<jusu-vartotojas>/calorie-counter.git
cd calorie-counter
python calorie_counter.py        # paleidžia programą
python -m unittest               # paleidžia testus
```

<sup>(Jei naudojate virtualią aplinką, prieš paleisdami įdiekite priklausomybes:  
`pip install -r requirements.txt`)</sup>

---

## 3 Programos naudojimas

1. Įveskite **svorį** (kg), **ūgį** (cm), **amžių** ir **aktyvumo lygį** (*low / medium / high*).  
2. Programa parodys Jūsų dienos palaikymo kalorijas.  
3. Įveskite kiekvieno maisto produkto pavadinimą ir BKV (baltymai, angliavandeniai, riebalai).  
4. Sistema realiu laiku skaičiuoja kalorijas ir rodo, kiek liko iki palaikymo normos.  
5. Dienos pabaigoje įrašas išsaugomas; galite tęsti kitą dieną arba išeiti.  
6. Pasirinkus, istorija išsaugoma **history.csv** faile.

---

## 4 Kodo struktūra

| Failas / Klasė        | Paskirtis                                                                              |
|-----------------------|----------------------------------------------------------------------------------------|
| **Food**              | Laiko produkto pavadinimą ir maistines vertes; skaičiuoja kcal.                        |
| **DailyIntake**       | Kaupia dienos `Food` sąrašą (*kompozicija*).                                           |
| **Person**            | Abstrakti bazė su privačiais laukais – inkapsuliacija.                                 |
| **User**              | Paveldi `Person`, perrašo BMR skaičiavimą – paveldėjimas.                              |
| **UserData**          | Saugo `User` + `DailyIntake` istoriją (*agregacija*).                                  |
| **FoodFactory**       | Įgyvendina **Factory Method** maistui kurti.                                           |
| **show_maintenance**  | Priima bet kurį `Person` palikuonį → polimorfizmas.                                    |
| **TestCalorieCounter**| Vienetų testai su `unittest`.                                                          |

---

## 5 OOP principai

| Ramstis            | Realizacija                                                                   |
|--------------------|-------------------------------------------------------------------------------|
| **Inkapsuliacija** | Privatūs `__weight`, `__height`, `__age`, `__activity_level` + getter/setter. |
| **Abstrakcija**    | `Person` kaip abstrakti klasė su `@abstractmethod`.                           |
| **Paveldėjimas**   | `User(Person)` perima ir specializuoja funkcionalumą.                         |
| **Polimorfizmas**  | `show_maintenance(user: Person)` veikia su bet kuriuo `Person` palikuoniu.    |

---

## 6 Vienetų testai

`TestCalorieCounter` tikrina:  

* `Food.get_calories()` formulę;  
* `DailyIntake.total_calories()` sumą;  
* BMR × aktyvumo koeficientą (*low*, *high*).  

Paleidžiama komanda:

```bash
python -m unittest
```

---

## 7 Rezultatai

* Įgyvendinti visi techniniai reikalavimai (OOP, dizaino šablonas, CSV I/O, testai).  
* Programa patikimai skaičiuoja kalorijas ir saugo istoriją.  
* CLI įvedimas apsaugotas `try/except`, kad išvengtų avarijų dėl netinkamų skaičių.  
* Testai užtikrina formulės teisingumą ir palengvina priežiūrą.

---

## 8 Reikalavimų atitiktis – kodo pavyzdžiai

### 8.1 Inkapsuliacija  
```python
class Person(ABC):
    def __init__(self, weight, height, age, activity_level):
        self.__weight = weight
        self.__height = height
        self.__age = age
        self.__activity_level = activity_level
```
Privatūs atributai (__weight, __height, __age, __activity_level) klasėje Person saugomi nuo tiesioginės prieigos. Prie jų prieinama per „getter“ ir „setter“ metodus (get_weight, set_weight, ir t.t.).*

---

### 8.2 Abstrakcija  
```python
@abstractmethod
def calculate_maintenance_calories(self):
    pass
```
`Person` apibrėžia bendrą metodą `calculate_maintenance_calories`, bet palieka tuščią (`pass`)

---

### 8.3 Paveldėjimas ir metodo perrašymas  
```python
class User(Person):
    def calculate_maintenance_calories(self):
        bmr = 10 * self.get_weight() + 6.25 * self.get_height() - 5 * self.get_age() + 5
        multiplier = {"low": 1.2, "medium": 1.55, "high": 1.9}
        return bmr * multiplier.get(self.get_activity_level(), 1.2)
```
Klasė `User` paveldi iš `Person` ir perrašo abstraktų metodą `calculate_maintenance_calories`. Taip pasiekiamas dinamiškas elgesys – skirtingos `Person` atmainos gali skirtingai apskaičiuoti kalorijas.

---

### 8.4 Polimorfizmas  
```python
def show_maintenance(user: Person):
    print(user.calculate_maintenance_calories())
```
Funkcija `show_maintenance(user: Person)` demonstruoja polimorfizmą: priima bet kokį objektą, paveldintį `Person`, ir kviečia metodą `calculate_maintenance_calories`, nepriklausomai nuo konkretaus tipo.

---

### 8.5 Kompozicija  
```python
class DailyIntake:
    def __init__(self):
        self.food_items = []      # sudėtinė dalis
```
`DailyIntake` turi sąrašą `Food` objektų – tai stiprus ryšys, kai dienos įrašai egzistuoja tik kaip dalis visumos.

---

### 8.6 Agregacija  
```python
class UserData:
    def __init__(self, user: User):
        self.user = user          # egzistuoja savarankiškai
        self.daily_history = []   # laiko kelias dienas
```
`UserData` turi nuorodą į `User` objektą ir sąrašą `DailyIntake` – šie objektai egzistuoja atskirai.

---

### 8.7 Dizaino šablonas – Factory Method  
```python
class FoodFactory:
    @staticmethod
    def create_food(name, carbs, protein, fats):
        return Food(name, carbs, protein, fats)
```
Factory Klasė `FoodFactory` įgyvendina Factory dizaino šabloną, leidžiantį kurti `Food` objektus centralizuotai per metodą `create_food`.

---

## 9 Išvados

### Pagrindiniai pasiekimai
* Įgyvendintos visos OOP paradigmos ir **Factory Method** dizaino šablonas, pademonstruojant tvirtą objektinio projektavimo supratimą.  
* Sukurta stabili CLI programa, leidžianti vartotojui apskaičiuoti paros palaikymo kalorijų normą ir sekti suvartojimą realiu laiku.  
* Įdiegta CSV įrašymo / skaitymo logika, todėl vartotojo duomenų istorija išlieka tarp paleidimų.  
* Vienetų testai patikrina svarbiausias funkcijas, užtikrindami kodo patikimumą.

### Darbo rezultatas
Galutinis produkto prototipas – **Calorie Counter** – paruoštas naudoti terminale iškart po diegimo. Jis:
1. Priima individualius duomenis.  
2. Dinamiškai vizualizuoja kalorijų balansą.  
3. Saugo maisto istoriją, kurią galima peržiūrėti ar importuoti į kitas sistemas (pvz., Excel).


**Apibendrinant**, šiam kursiniui darbui sukūriau praktiškai naudingą įrankį, paremtą OOP principais.

---

