import pandas as pd
import json
from pprint import pprint


def get_components(file_path):
    components = []

    # Read all sheets from Excel file
    xl = pd.read_excel(file_path, sheet_name=None)

    # Iterate through all sheets
    for sheet_name, df in xl.items():
        # Limit to first 9776 rows
        df = df.iloc[24:9776]

        # Print rows
        for _, row in df.iterrows():
            # Convert row to string, handle None/NaN values
            info, price = [str(cell) if pd.notnull(cell) else "" for cell in row][5:7]
            try:
                components.append((info, int(price)))
            except:
                pass

    sorted_components = {'components':
                             {'Система жидкостного охлаждения': [], 'Кулер': [],
                              'Видеокарта': [], 'Процессор': [],
                              'Материнская плата': [], 'Оперативная память': [],
                              'Жёсткий диск': [], 'Накопитель SSD': [],
                              'Блок питания': [], 'Корпус': []}}

    for component in components:
        info, price = component
        piece1, *other = info.split()
        if piece1 == 'Кулер':
            other = ' '.join(other)
            sorted_components['components']['Кулер'].append((other, price))
            continue
        elif piece1 == 'Видеокарта':
            other = ' '.join(other)
            sorted_components['components']['Видеокарта'].append((other, price))
            continue
        elif piece1 == 'Процессор':
            other = ' '.join(other)
            sorted_components['components']['Процессор'].append((other, price))
            continue
        elif piece1 == 'Корпус':
            other = ' '.join(other)
            sorted_components['components']['Корпус'].append((other, price))
            continue
        piece2, *other = other
        if piece1 == 'Материнская' and piece2 == 'плата':
            other = ' '.join(other)
            sorted_components['components']['Материнская плата'].append((other, price))
            continue
        elif piece1 == 'Оперативная' and piece2 == 'память':
            other = ' '.join(other)
            sorted_components['components']['Оперативная память'].append((other, price))
            continue
        elif piece1 == 'Жёсткий' and piece2 == 'диск':
            other = ' '.join(other)
            sorted_components['components']['Жёсткий диск'].append((other, price))
            continue
        elif piece1 == 'Накопитель' and piece2 == 'SSD':
            other = ' '.join(other)
            sorted_components['components']['Накопитель SSD'].append((other, price))
            continue
        elif piece1 == 'Блок' and piece2 == 'питания':
            other = ' '.join(other)
            sorted_components['components']['Блок питания'].append((other, price))
            continue
        piece3, *other = other
        if piece1 == 'Система' and piece2 == 'жидкостного' and piece3 == 'охлаждения':
            other = ' '.join(other)
            sorted_components['components']['Система жидкостного охлаждения'].append((other, price))

    return sorted_components


# Specify path to your XLSX file
file_name = "regard_price_230425_21.xlsx"

# Call function to print contents
components = get_components(file_name)

# Преобразование словаря в JSON
json_data = json.dumps(components, indent=4, ensure_ascii=False)

# Запись JSON в файл
with open("components_prices.json", "w", encoding="utf-8") as file:
    file.write(json_data)

print(json_data)
