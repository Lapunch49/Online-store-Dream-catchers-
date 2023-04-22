from typing import List

from .connector import StoreConnector
from pandas import DataFrame, Series
from datetime import datetime

from os import listdir, getcwd
from os.path import isfile, join

"""
    В данном модуле реализуется API (Application Programming Interface)
    для взаимодействия с БД с помощью объектов-коннекторов.
    
    ВАЖНО! Методы должны быть названы таким образом, чтобы по названию
    можно было понять выполняемые действия.
"""

def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def select_all_from_source_files(connector: StoreConnector) -> List[tuple]:
    """ Вывод списка обработанных файлов с сортировкой по дате в порядке убывания (DESCENDING) """
    query = f'SELECT * FROM source_file_catchers ORDER BY processed DESC'
    result = connector.execute(query).fetchall()
    return result


def insert_into_source_files(connector: StoreConnector, filename: str):
    """ Вставка в таблицу обработанных файлов """
    now = datetime.now()        # текущая дата и время
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")   # преобразуем в формат SQL
    query = f'INSERT INTO source_file_catchers (filename, processed) VALUES (\'{filename}\', \'{date_time}\')'
    result = connector.execute(query)
    return result


def insert_rows_into_processed_data(connector: StoreConnector, dataframe: DataFrame):
    """ Вставка строк из DataFrame в БД с привязкой данных к последнему обработанному файлу (по дате) """
    rows = dataframe.to_dict('records')
    files_list = select_all_from_source_files(connector)    # получаем список обработанных файлов
    # т.к. строка БД после выполнения SELECT возвращается в виде объекта tuple, например:
    # row = (1, 'seeds_dataset.csv', '2022-11-15 22:03:16') ,
    # то значение соответствующей колонки можно получить по индексу, например id = row[0]
    last_file_id = files_list[0][0]  # получаем индекс последней записи из таблицы с файлами
    if len(files_list) > 0:
        for row in rows:
            connector.execute(f'INSERT INTO '
                              f'dream_catchers (name, price, color, country, material,'
                              f'sizes, form, description, source_file) '
                              f'VALUES (\'{row["Название"]}\', \'{row["Цена"]}\','
                              f'\'{row["Цвет"]}\', \'{row["Страна производства"]}\','
                              f'\'{row["Материал"]}\', \'{row["Размер"]}\','
                              f'\'{row["Форма"]}\', \'{row["Описание"]}\', {last_file_id})')
        print('Data was inserted successfully')
    else:
        print('File records not found. Data inserting was canceled.')

def insert_photos_into_dataset(connector: StoreConnector):
    folder = 'database'
    onlyfiles = [f for f in listdir(join(getcwd(),folder)) if isfile(join(join(getcwd(),folder), f))]

    for thing in onlyfiles:
        if thing.endswith('.png'):
            id_products = int(thing[:thing.find('.')])
            photos = join(getcwd(),join(folder,thing))
        connector.execute(f'INSERT INTO '
                          f'photos (fk_product_id, photo) '
                          f'VALUES (\'{id_products}\', \'{photos})\')')
    print('Data was inserted successfully')