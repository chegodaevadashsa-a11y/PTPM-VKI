from triangle import calculat


def main():
    print("Вычисление вида треугольника")
    print("Введите длины трех сторон.")

    string1 = input("Сторона A: ")
    string2 = input("Сторона B: ")
    string3 = input("Сторона C: ")

    triangle_type, coordinates = calculat(
        string1,
        string2,
        string3
    )

    print()
    print("Тип треугольника:", triangle_type)
    print("Координаты вершин:", coordinates)


if __name__ == "__main__":
    main()