from abc import ABC, abstractmethod
from datetime import datetime
import csv
import unittest

# --- Food Class ---
class Food:
    def __init__(self, name: str, carbs: float, protein: float, fats: float):
        self.name = name
        self.carbs = carbs
        self.protein = protein
        self.fats = fats

    def get_calories(self):
        return self.carbs * 4 + self.protein * 4 + self.fats * 9

    def __str__(self):
        return f"{self.name}: {self.get_calories():.2f} kcal"


# --- Daily Intake (Composition of Food) ---
class DailyIntake:
    def __init__(self, date=None):
        self.date = date if date else datetime.today().strftime('%Y-%m-%d')
        self.food_items = []

    def add_food(self, food: Food):
        self.food_items.append(food)

    def total_calories(self):
        return sum(food.get_calories() for food in self.food_items)

    def __str__(self):
        food_list = "\n  ".join([str(food) for food in self.food_items])
        return f"\nDate: {self.date}\n  {food_list}\n  Total: {self.total_calories():.2f} kcal"


# --- Person (Abstract Base Class) ---
class Person(ABC):
    def __init__(self, weight, height, age, activity_level):
        self.__weight = weight
        self.__height = height
        self.__age = age
        self.__activity_level = activity_level

    def get_weight(self): return self.__weight
    def set_weight(self, weight): self.__weight = weight

    def get_height(self): return self.__height
    def set_height(self, height): self.__height = height

    def get_age(self): return self.__age
    def set_age(self, age): self.__age = age

    def get_activity_level(self): return self.__activity_level
    def set_activity_level(self, level): self.__activity_level = level

    @abstractmethod
    def calculate_maintenance_calories(self):
        pass


# --- User (Inheritance & Method Override) ---
class User(Person):
    def calculate_maintenance_calories(self):
        bmr = 10 * self.get_weight() + 6.25 * self.get_height() - 5 * self.get_age() + 5
        multiplier = {
            'low': 1.2,
            'medium': 1.55,
            'high': 1.9
        }
        return bmr * multiplier.get(self.get_activity_level(), 1.2)


# --- UserData (Aggregation) ---
class UserData:
    def __init__(self, user: User):
        self.user = user
        self.daily_history = []

    def add_daily_intake(self, intake: DailyIntake):
        self.daily_history.append(intake)

    def show_history(self):
        print("\n========== Intake History ==========")
        for day in self.daily_history:
            print(day)
        print("====================================")

    def save_to_file(self, filename="history.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Food", "Carbs", "Protein", "Fats", "Calories"])
            for day in self.daily_history:
                for food in day.food_items:
                    writer.writerow([day.date, food.name, food.carbs, food.protein, food.fats, food.get_calories()])

    def load_from_file(self, filename="history.csv"):
        self.daily_history = []
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                current_date = None
                current_day = None
                for row in reader:
                    if row['Date'] != current_date:
                        if current_day:
                            self.daily_history.append(current_day)
                        current_day = DailyIntake(row['Date'])
                        current_date = row['Date']
                    food = Food(row['Food'], float(row['Carbs']), float(row['Protein']), float(row['Fats']))
                    current_day.add_food(food)
                if current_day:
                    self.daily_history.append(current_day)
        except FileNotFoundError:
            pass


# --- Factory Pattern ---
class FoodFactory:
    @staticmethod
    def create_food(name, carbs, protein, fats):
        return Food(name, carbs, protein, fats)


# --- Polymorphic Function ---
def show_maintenance(user: Person):
    print(f"\nYour maintenance calories are: {user.calculate_maintenance_calories():.2f} kcal\n")


# --- Main Program ---
def main():
    print("====================================")
    print("     Welcome to the Calorie Counter")
    print("====================================")

    weight = float(input("Enter your weight (kg): "))
    height = float(input("Enter your height (cm): "))
    age = int(input("Enter your age: "))
    activity_level = input("Activity level (low, medium, high): ").strip().lower()

    user = User(weight, height, age, activity_level)
    data = UserData(user)

    show_maintenance(user)

    while True:
        print("\n-------- New Day's Intake --------")
        intake = DailyIntake()
        maintenance = user.calculate_maintenance_calories()

        while True:
            name = input("Food name (or 'done' to finish): ").strip()
            if name.lower() == 'done':
                print()
                break

            try:
                carbs = float(input("  Grams of carbs: "))
                protein = float(input("  Grams of protein: "))
                fats = float(input("  Grams of fats: "))
                print()
            except ValueError:
                print("  ❌ Invalid input! Please enter numbers.\n")
                continue

            food = FoodFactory.create_food(name, carbs, protein, fats)
            intake.add_food(food)

            total = intake.total_calories()
            remaining = maintenance - total

            print(f"✅ Current Total Calories Today: {total:.2f}")
            print(f"📉 Remaining to Maintenance: {remaining:.2f}\n")

        data.add_daily_intake(intake)
        print(f"✅ Total calories for {intake.date}: {intake.total_calories():.2f} kcal")

        cont = input("\nWould you like to enter another day? (y/n): ").strip().lower()
        if cont != 'y':
            break

    data.show_history()

    save = input("\nSave data to file? (y/n): ").strip().lower()
    if save == 'y':
        data.save_to_file()
        print("✅ Data saved to 'history.csv'")

    print("\n✅ Thank you for using the Calorie Counter!\n")


# --- Unit Tests ---
class TestCalorieCounter(unittest.TestCase):
    def test_food_calories(self):
        f = Food("TestFood", 10, 5, 2)
        self.assertEqual(f.get_calories(), 10*4 + 5*4 + 2*9)

    def test_daily_intake_total(self):
        f1 = Food("A", 5, 5, 5)
        f2 = Food("B", 10, 0, 0)
        di = DailyIntake("2025-01-01")
        di.add_food(f1)
        di.add_food(f2)
        expected = f1.get_calories() + f2.get_calories()
        self.assertAlmostEqual(di.total_calories(), expected)

    def test_user_maintenance_low(self):
        u = User(70, 175, 25, "low")
        expected = (10*70 + 6.25*175 - 5*25 + 5) * 1.2
        self.assertAlmostEqual(u.calculate_maintenance_calories(), expected)

    def test_user_maintenance_high(self):
        u = User(60, 160, 30, "high")
        expected = (10*60 + 6.25*160 - 5*30 + 5) * 1.9
        self.assertAlmostEqual(u.calculate_maintenance_calories(), expected)


if __name__ == '__main__':
    #main()
    # To run tests, comment out main() and uncomment line below
    unittest.main()
