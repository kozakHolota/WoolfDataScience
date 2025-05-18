from math import sqrt

import matplotlib.pyplot as plt
from matplotlib_venn import venn3

full_range = range(1, 31)

def is_full_square(num):
    res = sqrt(num)
    return res == int(res)

pair_nums = {i for i in full_range if i % 2 == 0}
devided_by_5 = {i for i in full_range if i % 5 == 0}
full_square = {i for i in full_range if is_full_square(i)}

labels = ("Парні", "Діляться на 5", "Повні квадрати")
venn3((pair_nums, devided_by_5, full_square), labels)
plt.show()