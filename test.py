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
