import plotext as plt
import numpy as np

# Создаём данные
x = np.linspace(0, 2 * np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

# Настройки графика
plt.plot(x, y_sin, label="sin(x)", color="red")
plt.plot(x, y_cos, label="cos(x)", color="green")

plt.title("Графики синуса и косинуса")
plt.xlabel("x")
plt.ylabel("y")
plt.show()