
class Controller:
    def __init__(self, calculator, database, user_interface, external_service):
        self.calculator = calculator
        self.database = database
        self.user_interface = user_interface
        self.external_service = external_service

    def run(self):
        a, b, c = self.user_interface.get_input()

        try:
            numeric_sides = (float(a), float(b), float(c))
        except (ValueError, TypeError):
            result = {
                "type": "",
                "error": "Стороны должны быть числами"
            }
            message = result["error"]
            self.external_service.send(message)
            return result

        cached_result = self.database.get(*numeric_sides)

        if cached_result is None:
            result = self.calculator.calculate(a, b, c)
            self.database.add(*numeric_sides, result)
        else:
            result = cached_result

        if result["error"]:
            message = result["error"]
        else:
            message = "Тип треугольника: " + result["type"]

        self.external_service.send(message)
        return result
