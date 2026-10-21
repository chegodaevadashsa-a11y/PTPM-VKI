
import os
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from triangle import TriangleCalculator
from database import TriangleDatabase
from controller import Controller
from user_interface import ConsoleUserInterface
from external_service import MockExternalService


class TriangleIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.calculator = TriangleCalculator()
        self.database = TriangleDatabase(":memory:")
        self.user = Mock()
        self.external = MockExternalService()

        self.controller = Controller(
            self.calculator,
            self.database,
            self.user,
            self.external
        )

    def tearDown(self):
        self.database.close()

    def test_controller_calculates_and_saves_result(self):
        self.user.get_input.return_value = ("3", "4", "5")

        result = self.controller.run()

        self.assertEqual(result["type"], "разносторонний")
        self.assertIsNone(result["error"])
        self.assertEqual(
            self.database.get(3, 4, 5)["type"],
            "разносторонний"
        )
        self.assertEqual(len(self.external.sent_messages), 1)

    def test_controller_uses_cached_result(self):
        saved_result = {
            "type": "равносторонний",
            "error": None
        }
        self.database.add(5, 5, 5, saved_result)
        self.user.get_input.return_value = ("5", "5", "5")

        with patch.object(
            self.calculator,
            "calculate",
            side_effect=AssertionError("Повторное вычисление")
        ):
            result = self.controller.run()

        self.assertEqual(result, saved_result)

    def test_controller_sends_error_for_invalid_triangle(self):
        self.user.get_input.return_value = ("1", "2", "10")

        result = self.controller.run()

        self.assertEqual(result["type"], "не треугольник")
        self.assertIsNotNone(result["error"])
        self.assertEqual(len(self.external.sent_messages), 1)
        self.assertIn("не существует", self.external.sent_messages[0])

    def test_console_interface_reads_three_sides(self):
        interface = ConsoleUserInterface()

        with patch(
            "builtins.input",
            side_effect=["3", "4", "5"]
        ) as mocked_input:
            result = interface.get_input()

        self.assertEqual(result, ("3", "4", "5"))
        self.assertEqual(mocked_input.call_count, 3)

    def test_database_deletes_saved_result(self):
        result = {"type": "равносторонний", "error": None}
        self.database.add(5, 5, 5, result)

        self.assertTrue(self.database.delete(5, 5, 5))
        self.assertIsNone(self.database.get(5, 5, 5))

    def test_external_service_records_sent_message(self):
        service = MockExternalService()

        self.assertTrue(service.send("Тестовое сообщение"))
        self.assertEqual(
            service.sent_messages,
            ["Тестовое сообщение"]
        )


if __name__ == "__main__":
    unittest.main()
