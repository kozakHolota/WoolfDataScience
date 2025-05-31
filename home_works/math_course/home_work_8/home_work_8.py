import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import gamma


def get_dataset_from_gdrive_csv(url: str) -> pd.DataFrame:
    url = url[:url.find('/edit')] + '/export?format=csv'
    return pd.read_csv(url)

def build_hists(df: pd.DataFrame) -> None:
    for col in df.columns:
        plt.figure(figsize=(10, 6))  # розмір графіка
        plt.hist(df[col], bins=30, color='skyblue', edgecolor='black', alpha=0.7)

        # Додаємо підписи
        plt.title(f'Гістограма розподілу значень {col}', fontsize=16)
        plt.xlabel('Значення', fontsize=14)
        plt.ylabel('Частота', fontsize=14)

        # Додаємо сітку
        plt.grid(True, linestyle='--', alpha=0.5)

        # Показуємо графік
        plt.tight_layout()
        plt.show()

def simulate_stock_price(start_price: float, times: int, q_step: float, p_step: float):
    return start_price + sum((float(np.random.choice(gamma.pdf([q_step, p_step], a=0.3, scale=1.1))) for _ in range(times)))


def build_distribution_histogramm_check_normality(data: list, t: int):
    # Перевіряємо нормальність вибірки
    stat, p = stats.normaltest(data)
    print(
        f"Розподіл для колонки t={str(t)} нормальний" if p > 0.05 else f"Розподіл для колонки t={str(t)} не нормальний")
    # Створюємо гістограму
    n, bins, patches = plt.hist(data, bins=10, density=True, alpha=0.7, color='y')

    el_min = min(data)
    el_max = max(data)

    # Підганяємо нормальний розподіл
    mean, std = stats.norm.fit(data)

    # Створюємо точки для теоретичної кривої
    X1 = np.linspace(el_min, el_max, 1000)
    dist2 = stats.norm(loc=mean, scale=std)
    plt.plot(X1, dist2.pdf(X1), 'k-')

    # Додаємо підписи та сітку
    plt.xlabel('x')
    plt.ylabel(f'Розподіл цін: t={str(t)}')
    plt.grid(True)
    plt.show()
