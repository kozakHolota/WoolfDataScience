import csv
import zlib
from typing import Any

import numpy as np
import optuna
import pandas as pd
from catboost import CatBoostClassifier
from imblearn.ensemble import BalancedRandomForestClassifier
from imblearn.over_sampling import SMOTE
from lightgbm import LGBMClassifier
from matplotlib import pyplot as plt
from pandas import Series
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score, train_test_split, StratifiedKFold
from xgboost import XGBClassifier


class HyperParametersOptimizer:
    def __init__(self,
                 x: pd.DataFrame,
                 y: pd.Series,
                 cv: int = 5,
                 scoring: str = "f1",
                 cat_cols: list = None
                 ):
        self.scoring = scoring
        self.cv = cv
        self.y = y
        self.X = x
        self.cat_cols = cat_cols if cat_cols is not None else []

    def xgb_objective(self, trial)-> float:
        params = {
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            # log=True часто краще для learning rate
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.3, 1.0),
            'n_estimators': trial.suggest_int('n_estimators', 200, 1000),
            'scale_pos_weight': trial.suggest_float('scale_pos_weight', 1.0, 10.0),  # Додаємо балансування ваг
            'n_jobs': -1,
            'random_state': 42
        }

        model = XGBClassifier(**params)

        # Змінюємо метрику на f1 або roc_auc
        score = cross_val_score(model, self.X, self.y, cv=self.cv, scoring=self.scoring).mean()

        return score

    def brf_objective(self, trial):
        """
        Функція валідації гіперпараметрів для BalancedRandomForestClassifier.
        """
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 200, 1000),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 15),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
            'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
            'replacement': trial.suggest_categorical('replacement', [True, False]),
            'sampling_strategy': trial.suggest_categorical('sampling_strategy', ['auto', 'all']),
            'random_state': 42,
        }

        model = BalancedRandomForestClassifier(**params)
        score = cross_val_score(model, self.X, self.y, cv=self.cv, scoring=self.scoring).mean()
        return score

    def catboost_objective(self, trial):
        weight_pos = trial.suggest_float("weight_pos", 1.0, 50.0, log=True)
        params  = {
            'iterations': trial.suggest_int('iterations', 100, 1000),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'depth': trial.suggest_int('depth', 3, 12),
            'loss_function': 'Logloss',
            'class_weights': [1.0, weight_pos],
            'eval_metric': trial.suggest_categorical('eval_metric', ['Accuracy', 'AUC']),
            'verbose': 50,
            'cat_features': self.cat_cols,
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1e-5, 50.0, log=True),
            'bagging_temperature': trial.suggest_float('bagging_temperature', 0.0, 1.0),
            'rsm': trial.suggest_float('rsm', 0.0, 1.0),
            'min_data_in_leaf': trial.suggest_int('min_data_in_leaf', 1, 100),
            'leaf_estimation_iterations': trial.suggest_int('leaf_estimation_iterations', 1, 10),
        }

        for col in self.cat_cols:
            self.X[col] = self.X[col].fillna("Missing").astype(str)

        model = CatBoostClassifier(**params)
        score = cross_val_score(model, self.X, self.y, cv=self.cv, scoring=self.scoring).mean()
        return score

    def lightgbm_objective(self, trial):
        params = {
            'objective': 'binary',
            'metric': 'auc',
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'boosting_type': trial.suggest_categorical('boosting_type', ['gbdt', 'dart']),
            'scale_pos_weight': trial.suggest_float('scale_pos_weight', 1.0, 10.0),
            'num_leaves': trial.suggest_int('num_leaves', 31, 127),
            'max_depth': trial.suggest_int('max_depth', -1, 9),
            'min_data_in_leaf': trial.suggest_int('min_data_in_leaf', 20, 100),
            'feature_fraction': trial.suggest_float('feature_fraction', 0.4, 1.0),
            'bagging_fraction': trial.suggest_float('bagging_fraction', 0.4, 1.0),
            'bagging_freq': trial.suggest_int('bagging_freq', 1, 7),
        }

        model = LGBMClassifier(**params)
        score = cross_val_score(model, self.X, self.y, cv=self.cv, scoring=self.scoring).mean()
        return score

    def __get_model_best_params(self, model_boost_func, n_trials=50) -> dict[str, Any]:
        study = optuna.create_study(direction="maximize")
        study.optimize(model_boost_func, n_trials=n_trials)
        return study.best_params

    def get_xgb_best_params(self, n_trials=50) -> dict[str, Any]:
        return self.__get_model_best_params(self.xgb_objective, n_trials)

    def get_brf_best_params(self, n_trials=50) -> dict[str, Any]:
        return self.__get_model_best_params(self.brf_objective, n_trials)

    def get_catboost_best_params(self, n_trials=50) -> dict[str, Any]:
        return self.__get_model_best_params(self.catboost_objective, n_trials)

    def get_lightgbm_best_params(self, n_trials=50) -> dict[str, Any]:
        return self.__get_model_best_params(self.lightgbm_objective, n_trials)

class VarMeanEstimator(BaseEstimator, TransformerMixin):
    def __init__(self, col_name: str, cols_to_mean: list[str]):
        self.cols_to_mean = cols_to_mean
        self.col_name = col_name
        # self.var_mean видалено, оскільки це не параметр стану моделі

    def fit(self, X, y=None):
        # Для transformer, який обчислює статистику "по рядках" (row-wise),
        # fit зазвичай нічого не робить.
        return self

    def transform(self, X):
        # Робимо копію, щоб не змінювати оригінальний датафрейм
        X = X.copy()
        # Обчислюємо нову колонку
        X[self.col_name] = X[self.cols_to_mean].mean(axis=1)
        return X

    def get_feature_names_out(self, input_features=None):
        """
        Повертає імена колонок після трансформації.
        Потрібен для коректної роботи set_output(transform="pandas").
        """
        # Якщо вхідні імена не надані, ми не можемо гарантувати правильний порядок,
        # але для DataFrame пайплайнів вони зазвичай передаються.
        if input_features is None:
             # У випадку відсутності імен повертаємо просто ім'я нової колонки, 
             # або генеруємо заглушки (залежить від логіки sklearn версії),
             # але безпечніше повернути список з новою колонкою, якщо це єдине, що ми знаємо.
             # Однак, оскільки ми повертаємо X + нову колонку, ідеально мати input_features.
             raise ValueError("input_features must be provided to generate output names")
        
        # Повертаємо всі вхідні колонки + нову колонку
        return list(input_features) + [self.col_name]

class CategoryHasher(BaseEstimator, TransformerMixin):
    def __init__(self, col_name: str, cat_cols: list[str]):
        self.cat_cols = cat_cols
        self.col_name = col_name
        self.num_hash = None

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X[self.col_name] = X[self.cat_cols].apply(lambda x: zlib.crc32(str(x).encode('utf-8')), axis=1)
        return X

    def get_feature_names_out(self, input_features=None):
        """
        Повертає імена колонок після трансформації.
        Потрібен для коректної роботи set_output(transform="pandas").
        """
        # Якщо вхідні імена не надані, ми не можемо гарантувати правильний порядок,
        # але для DataFrame пайплайнів вони зазвичай передаються.
        if input_features is None:
            # У випадку відсутності імен повертаємо просто ім'я нової колонки,
            # або генеруємо заглушки (залежить від логіки sklearn версії),
            # але безпечніше повернути список з новою колонкою, якщо це єдине, що ми знаємо.
            # Однак, оскільки ми повертаємо X + нову колонку, ідеально мати input_features.
            raise ValueError("input_features must be provided to generate output names")

        # Повертаємо всі вхідні колонки + нову колонку
        return list(input_features) + [self.col_name]

def get_nan_percentage(df: pd.DataFrame) -> Series:
    return df.isna().mean() * 100

def concat_dfs(*dfs: pd.DataFrame) -> pd.DataFrame:
    return pd.concat(dfs, axis=1)

def split_df_to_x_y(df: pd.DataFrame, target_col: str) -> tuple[pd.DataFrame, pd.Series]:
    X = df.drop(columns=[target_col], axis=1)
    X = X.loc[:, ~X.columns.duplicated()]
    y = df[target_col]

    return X, y

def split_train_test(
        x: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.2,
        random_state: int=42,
        balance_classes: bool=True) -> tuple:
    X_train, X_test, y_train, y_test = train_test_split(
    x, y,
    test_size=test_size,
    random_state=random_state,
    shuffle=True
   )

    if balance_classes:
        sm = SMOTE(random_state=42)

        X_train, y_train = sm.fit_resample(X_train, y_train)

    return X_train, X_test, y_train, y_test

def evaluate_model_avg_accuracy(model, X, y):
    # Створюємо стратифікований поділ на 5 фолдів
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Виконуємо крос-валідацію
    scores = cross_val_score(model, X, y, cv=skf)

    print("Точність для кожного фолду:", scores)
    print("Середня точність:", scores.mean())

def evaluate_model(model, X_train, y_train, X_test, y_test, cat_cols: list = None):
    kwargs = {"cat_features": cat_cols} if cat_cols else {}
    model.fit(X_train, y_train, **kwargs)

    # Отримуємо ймовірності замість готових класів (0 або 1)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    # Спробуйте різні пороги, наприклад 0.4 або 0.6
    threshold = 0.4
    pred_custom = (y_pred_proba >= threshold).astype(int)

    print(f"Звіт для порогу {threshold}:")
    print(classification_report(y_test, pred_custom))

def draw_feature_importance(model, max_num_features: int=15):
    # Візуалізація важливості ознак
    model.plot_importance(model, max_num_features=max_num_features)
    plt.show()

def write_submission_csv(prediction: np.ndarray, filename: str):
    index = 0
    with open(filename, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['index', 'y'])
        for y in prediction:
            csv_writer.writerow([index, y])
            index += 1