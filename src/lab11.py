import os
import pandas as pd

# Автоматичний шлях до файлу data/sales_data.csv відносно src/lab11.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales_data.csv")


def main():
    # --- Завдання для всіх варіантів ---
    # 1. Завантаження даних з файлу sales_data.csv у DataFrame
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])

    # 2. Первинний аналіз даних
    print("=== Перші 5 рядків ===")
    print(df.head())

    print("\n=== Загальна інформація про DataFrame ===")
    df.info()

    print("\n=== Статистичні характеристики числових стовпців ===")
    print(df.describe())

    # --- Варіант 8 ---
    # 1. Вибрати рядки, де date є останнім днем місяця
    month_end_df = df[df["date"].dt.is_month_end]
    print("\n=== 1. Рядки, де date є останнім днем місяця ===")
    print(month_end_df.head(10))
    print(f"Всього знайдено рядків: {len(month_end_df)}")

    # 2. Відсортувати дані за price (зростання), а потім за quantity (спадання)
    sorted_df = df.sort_values(by=["price", "quantity"], ascending=[True, False])
    print("\n=== 2. Відсортовані дані (price ↑, quantity ↓) ===")
    print(sorted_df.head(10))

    # 3. Згрупувати за product_id та обчислити коефіцієнт варіації (std / mean) для price
    cv_price = df.groupby("product_id")["price"].agg(lambda x: x.std() / x.mean())
    print("\n=== 3. Коефіцієнт варіації ціни (price) для кожного product_id ===")
    print(cv_price)

    # 4. Додати стовпець year, який містить рік, витягнутий з date
    df["year"] = df["date"].dt.year
    print("\n=== 4. Дані з новим стовпцем year ===")
    print(df[["order_id", "date", "year"]].head())

    # 5. Видалити рядки, де quantity дорівнює 1
    df = df[df["quantity"] != 1].copy()
    print(f"\n=== 5. Рядки з quantity == 1 видалено. Залишилось рядків: {len(df)} ===")

    # 6. Обчислити total_amount та замінити пропущені значення (NaN) на середнє для відповідного store_id та product_id
    df["total_amount"] = df["quantity"] * df["price"]
    nan_before = df["total_amount"].isna().sum()

    df["total_amount"] = df.groupby(["store_id", "product_id"])["total_amount"].transform(
        lambda x: x.fillna(x.mean())
    )
    nan_after = df["total_amount"].isna().sum()
    print(f"\n=== 6. Обробка NaN у total_amount: було {nan_before}, стало {nan_after} ===")
    print(df[["store_id", "product_id", "quantity", "price", "total_amount"]].head(10))

    # 7. Зведена таблиця: рядки - year, стовпці - store_id, комірки - максимальна виручка (total_amount)
    pivot_table = df.pivot_table(
        values="total_amount",
        index="year",
        columns="store_id",
        aggfunc="max"
    )
    print("\n=== 7. Зведена таблиця (максимальна виручка total_amount за роками та магазинами) ===")
    print(pivot_table)


if __name__ == "__main__":
    main()