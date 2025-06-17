import matplotlib.pyplot as plt

# Дані: список елементів і кількість ітерацій
elements = [6/4, 3/4, 8/7, 1/3, 3.1415956]  # Елементи, які шукаємо
iterations = [2, 2, 3, 1, 4]  # Ітерації для кожного елемента

# Побудова бар-діаграми
plt.bar(elements, iterations, color='skyblue', edgecolor='black')

# Додавання підписів для кожного стовпчика
for i in range(len(elements)):
    plt.text(elements[i], iterations[i] + 0.1,  # Координати підпису (трішки вище стовпця)
             str(iterations[i]),               # Текст підпису — значення
             ha='center', fontsize=10)         # Вирівнювання по центру і розмір шрифта

# Налаштування підписів до осей
plt.xlabel("Елементи (Cases)", fontsize=12)
plt.ylabel("Кількість ітерацій (Iterations)", fontsize=12)
plt.title("Кількість ітерацій для кожного елемента", fontsize=14)

# Відображення графіка
plt.show()