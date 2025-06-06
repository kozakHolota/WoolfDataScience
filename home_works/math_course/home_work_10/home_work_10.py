import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def draw_comparable_scatter(y_test, y_pred):
    plt.figure(figsize=(6, 6))
    sns.scatterplot(x=y_test, y=y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r')  # ідеальна лінія
    plt.xlabel('Справжні значення')
    plt.ylabel('Передбачені значення')
    plt.title('Справжні vs Передбачені')
    plt.grid(True)
    plt.show()

def draw_error_plot(y_test, y_pred):
    residuals = y_test - y_pred

    plt.figure(figsize=(7, 5))
    sns.scatterplot(x=y_test, y=residuals)
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel("Передбачені значення")
    plt.ylabel("Рештки (y_true - y_pred)")
    plt.title("Рештки по передбаченню")
    plt.grid(True)
    plt.show()

def draw_dispersion_num(df: pd.DataFrame, col: str, title: str, x_label: str, y_label: str):
    # Стиль графіка
    sns.set(style="whitegrid")

    # Побудова графіка
    plt.figure(figsize=(10, 5))
    sns.histplot(df[col], bins=10, kde=True, color='teal', edgecolor='black', linewidth=1.2)

    # Декорації
    plt.title(title, fontsize=16)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()