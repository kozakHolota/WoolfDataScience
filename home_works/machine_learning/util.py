import logging
import pickle
from typing import Any

import pandas as pd
import requests
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import zscore

def get_desired_datasets(dataset_url: str, timeout: float = 15.0) -> Any:
    """
    Завантажує та розпаковує pickle з віддаленого джерела.

    :param dataset_url: Адреса датасету
    :param timeout: таймаут HTTP-запиту в секундах.
    :return: десеріалізовані дані.
    :raises: requests.RequestException, pickle.UnpicklingError, та інші винятки.
    """
    try:
        response = requests.get(dataset_url, timeout=timeout)
        response.raise_for_status()
        content: bytes = response.content
        return pickle.loads(content)
    except requests.RequestException as http_err:
        logging.error("Помилка HTTP під час завантаження з %s: %s", dataset_url, http_err)
        raise
    except pickle.UnpicklingError as unpickle_err:
        logging.error("Помилка десеріалізації pickle з %s: %s", dataset_url, unpickle_err)
        raise
    except Exception as err:
        logging.error("Несподівана помилка під час обробки даних з %s: %s", dataset_url, err)
        raise

def draw_heatmap(data):
    plt.figure(figsize=(9, 13))

    ax = sns.heatmap(data,
                     cmap='Blues',
                     linewidth=0.5,
                     square=True,
                     cbar_kws=dict(
                         location="bottom",
                         pad=0.01,
                         shrink=0.25))

    ax.xaxis.tick_top()
    ax.tick_params(axis='x', labelrotation=90)

    plt.show()

def show_outliers(values, z_thresh=3.0):
    """
    values: pd.Series | np.ndarray | list
    Показує Z-оцінки, вихідні значення та підсвічує викиди за порогом |Z| > z_thresh.
    """
    # Перетворюємо на 1D масив числових значень
    if isinstance(values, pd.Series):
        data = values.to_numpy()
        index = values.index.to_numpy()
    elif isinstance(values, pd.DataFrame):
        data = values.iloc[:, 0].to_numpy()
        index = values.index.to_numpy()
    else:
        data = np.asarray(values)
        index = np.arange(len(data))

    data = data.astype(float)

    # Обчислюємо Z-оцінки, ігноруючи NaN
    data_z = zscore(data, nan_policy='omit')

    # Маска викидів
    outlier_mask = np.abs(data_z) > z_thresh

    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 7))

    # Графік Z-оцінок
    axes[0].plot(index, data_z, color='tab:red', label='Z-score')
    axes[0].axhline(0.0, color='gray', lw=1, ls='--')
    axes[0].axhline(z_thresh, color='orange', lw=1, ls='--', label=f'+{z_thresh}')
    axes[0].axhline(-z_thresh, color='orange', lw=1, ls='--', label=f'-{z_thresh}')
    # Викиди на Z-графіку
    axes[0].scatter(index[outlier_mask], data_z[outlier_mask],
                    color='black', edgecolor='white', zorder=3, label='Outliers')
    axes[0].set_ylabel('Z')
    axes[0].legend()

    # Графік оригінальних значень
    axes[1].plot(index, data, color='tab:blue', label='Values')
    # Викиди на вихідних значеннях
    axes[1].scatter(index[outlier_mask], data[outlier_mask],
                    color='crimson', edgecolor='white', zorder=3, label='Outliers')
    axes[1].set_xlabel('Index')
    axes[1].set_ylabel('Value')
    axes[1].legend()

    plt.tight_layout()
    plt.show()

def remove_outliers(data: pd.DataFrame, column_name: str, z_thresh: float = 3.0) -> pd.DataFrame:
    """
    Видаляє викиди за однією колонкою на основі Z-оцінки.
    Рядки, де |Z(col)| > z_thresh, будуть видалені.

    Parameters:
        data: вхідний DataFrame
        column_name: назва колонки, за якою визначаються викиди
        z_thresh: поріг для |Z|

    Returns:
        DataFrame без рядків-викидів (копія)
    """
    if column_name not in data.columns:
        raise KeyError(f"Column '{column_name}' not found in DataFrame")

    col = data[column_name].astype(float)
    z = zscore(col, nan_policy='omit')

    # Зберігаємо рядки з |Z| <= z_thresh або з NaN Z (щоб не втрачати NaN за замовчуванням)
    keep_mask = (np.abs(z) <= z_thresh) | np.isnan(z)

    return data.loc[keep_mask].copy()


def show_num_features_dist(data):
    melted = data.melt()

    g = sns.FacetGrid(melted,
                      col='variable',
                      col_wrap=4,
                      sharex=False,
                      sharey=False,
                      aspect=1.25)

    g.map(sns.histplot, 'value')

    g.set_titles(col_template='{col_name}')

    g.tight_layout()

    plt.show()
