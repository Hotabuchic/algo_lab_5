import sys
from random import uniform

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QPushButton, QLabel, QLineEdit, QTextEdit, QCheckBox)

N = 2


def func(x1, x2):
    return (x1 - 2) ** 4 + (x1 - 2 * x2) ** 2


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots()
        super().__init__(fig)
        self.setParent(parent)
        self.ax.set_title('График точек')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')

        # Установка границ осей
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-100, 100)

    def plot(self, x, y):
        # Очистка предыдущих точек и отображение новых
        self.ax.cla()  # Очистка осей
        self.ax.set_title('График точек')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')

        # Установка границ осей
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-100, 100)

        # Отображение точек
        self.ax.scatter(x, y, color='blue', linewidths=0)
        self.ax.grid()
        self.draw()


class MainWinodow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.particles = []
        self.count_particles = None
        self.setWindowTitle("Роевой алгоритм")
        self.resize(800, 700)

        self.param = QLabel("Параметры", self)
        self.param.move(100, 10)
        self.param.setFont(QFont("Times", 10))
        self.param.adjustSize()

        self.func_label = QLabel("Функция:", self)
        self.func_label.move(10, 45)
        self.func_label.adjustSize()

        self.func_label_2 = QLabel("(X[1] - 2)^4 + (X[1] - 2*X[2])^2", self)
        self.func_label_2.setFont(QFont("Times", 9))
        self.func_label_2.move(100, 45)
        self.func_label_2.adjustSize()

        self.coef_speed_label = QLabel("Коэфф. текущей скорости:", self)
        self.coef_speed_label.move(10, 80)
        self.coef_speed_label.adjustSize()

        self.coef_best_value_label = QLabel("Коэфф. собственного лучшего значения:", self)
        self.coef_best_value_label.move(10, 115)
        self.coef_best_value_label.adjustSize()

        self.coef_global_best_value_label = QLabel("Коэфф. глобального лучшего значения:", self)
        self.coef_global_best_value_label.move(10, 150)
        self.coef_global_best_value_label.adjustSize()

        self.particle_count_label = QLabel("Количество частиц:", self)
        self.particle_count_label.move(10, 185)
        self.particle_count_label.adjustSize()

        self.modify_label = QLabel("Включить модификацию", self)
        self.modify_label.move(10, 220)
        self.modify_label.adjustSize()

        self.coef_speed_line = QLineEdit(self)
        self.coef_speed_line.setText("0.3")
        self.coef_speed_line.move(270, 75)

        self.coef_best_value_line = QLineEdit(self)
        self.coef_best_value_line.setText("1")
        self.coef_best_value_line.move(270, 110)

        self.coef_global_best_value_line = QLineEdit(self)
        self.coef_global_best_value_line.setText("2.5")
        self.coef_global_best_value_line.move(270, 145)

        self.particle_count_line = QLineEdit(self)
        self.particle_count_line.setText("100")
        self.particle_count_line.move(240, 180)

        self.modify_checkbox = QCheckBox(self)
        self.modify_checkbox.move(220, 220)

        self.management = QLabel("Управление", self)
        self.management.move(100, 245)
        self.management.setFont(QFont("Times", 10))
        self.management.adjustSize()

        self.make_hrom = QPushButton("Создать частицы", self)
        self.make_hrom.resize(250, 30)
        self.make_hrom.move(30, 285)
        self.make_hrom.clicked.connect(self.generate_particle)

        self.count_poc = QLabel("Количество итераций:", self)
        self.count_poc.move(10, 330)
        self.count_poc.adjustSize()

        self.count_poc_line = QLineEdit(self)
        self.count_poc_line.setText("10")
        self.count_poc_line.move(220, 325)

        self.make_do = QPushButton("Рассчитать", self)
        self.make_do.resize(250, 30)
        self.make_do.move(30, 365)
        self.make_do.clicked.connect(self.calculate_algo)

        self.res = QLabel("Результаты", self)
        self.res.move(100, 405)
        self.res.setFont(QFont("Times", 10))
        self.res.adjustSize()

        self.best_res_label = QLabel("Лучшее решение:", self)
        self.best_res_label.move(10, 440)
        self.best_res_label.adjustSize()

        self.res_textedit = QTextEdit(self)
        self.res_textedit.resize(320, 170)
        self.res_textedit.move(10, 470)

        self.best_func_label = QLabel("Значение функции:", self)
        self.best_func_label.move(10, 660)
        self.best_func_label.adjustSize()

        self.func_res_line = QLineEdit(self)
        self.func_res_line.move(150, 655)
        self.func_res_line.resize(180, 30)

        self.canvas = PlotCanvas(self)
        self.canvas.setGeometry(350, 190, 430, 500)

        self.range_label = QLabel("Диапазон генерации точек", self)
        self.range_label.move(450, 10)
        self.range_label.adjustSize()

        self.min_range_label = QLabel("От:", self)
        self.min_range_label.move(390, 50)

        self.max_range_label = QLabel("До:", self)
        self.max_range_label.move(530, 50)

        self.min_range_line = QLineEdit(self)
        self.min_range_line.move(420, 50)
        self.min_range_line.setText("-100")

        self.max_range_line = QLineEdit(self)
        self.max_range_line.move(560, 50)
        self.max_range_line.setText("100")

    def generate_particle(self):
        self.count_particles = int(self.particle_count_line.text())
        x1 = [uniform(float(self.min_range_line.text()), float(self.max_range_line.text())) for _ in
              range(self.count_particles)]
        x2 = [uniform(float(self.min_range_line.text()), float(self.max_range_line.text())) for _ in
              range(self.count_particles)]
        self.particles = [[x1[i], x2[i], [0, 0], [x1[i], x2[i], func(x1[i], x2[i])]] for i in
                          range(self.count_particles)]
        self.canvas.plot(x1, x2)

    def calculate_algo(self):
        global_best = sorted(self.particles, key=lambda x: x[-1][-1])[0]
        global_best_x, global_best_y, global_best_value = global_best[-1]
        speed = float(self.coef_speed_line.text())
        global_k = float(self.coef_global_best_value_line.text())
        local_k = float(self.coef_best_value_line.text())
        count_iter = int(self.count_poc_line.text())
        for _ in range(count_iter):
            for i in range(self.count_particles):
                v_i = self.particles[i][2]
                best_i_x = self.particles[i][-1][0]
                best_i_y = self.particles[i][-1][1]
                best_value = self.particles[i][-1][2]

                new_v_i_x = speed * v_i[0] + uniform(0, 1) * local_k * (best_i_x - self.particles[i][0]) + uniform(0,
                                                                                                                   1) * global_k * (
                                    global_best_x - self.particles[i][0])
                new_v_i_y = speed * v_i[1] + uniform(0, 1) * local_k * (best_i_y - self.particles[i][1]) + uniform(0,
                                                                                                                   1) * global_k * (
                                    global_best_y - self.particles[i][1])
                if self.modify_checkbox.isChecked():
                    if new_v_i_x > 20:
                        new_v_i_x = 20
                    if new_v_i_x < -20:
                        new_v_i_x = -20
                    if new_v_i_y > 20:
                        new_v_i_y = 20
                    if new_v_i_y < -20:
                        new_v_i_y = -20

                self.particles[i][0] += new_v_i_x
                self.particles[i][1] += new_v_i_y
                self.particles[i][2] = [new_v_i_x, new_v_i_y]
                new_func_value = func(self.particles[i][0], self.particles[i][1])
                if new_func_value < best_value:
                    self.particles[i][-1] = [self.particles[i][0], self.particles[i][1], new_func_value]
                if new_func_value < global_best_value:
                    global_best_x, global_best_y, global_best_value = self.particles[i][0], self.particles[i][
                        1], new_func_value
        x1 = [self.particles[i][0] for i in range(self.count_particles)]
        x2 = [self.particles[i][1] for i in range(self.count_particles)]
        self.res_textedit.setText(f"X[1]: {global_best_x}\nX[2]: {global_best_y}")
        self.func_res_line.setText(str(global_best_value))
        self.canvas.plot(x1, x2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWinodow()
    ex.show()
    sys.exit(app.exec_())
