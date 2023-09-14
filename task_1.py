"""
Напишите функцию, которая получает на вход директорию и рекурсивно обходит её и все вложенные директории.
Результаты обхода сохраните в файлы json, csv и pickle
"""

import os
import json
import csv
import pickle
import logging
import argparse

logging.basicConfig(filename="log/log1.log",
                    filemode="a",
                    encoding="utf-8",
                    format='{levelname:<6} - {asctime} в строке {lineno:>3d}, функция - "{funcName}()" : {msg}',
                    style="{",
                    level=logging.INFO
                    )
logger = logging.getLogger("my_logger")


class ScanDirectory:
    def __init__(self, directory):
        self.directory = directory
        self.result = self.traverse_directory()

    def traverse_directory(self):
        logger.info(f"Сканирую директорию {self.directory}")
        result = []
        for root, dirs, files in os.walk(self.directory):
            current_dir = {
                'name': os.path.basename(root),
                'type': 'directory',
                'size': 0,
                'parent_directory': os.path.dirname(root)
            }

            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                current_dir['size'] += file_size

                result.append({
                    'name': file,
                    'type': 'file',
                    'size': file_size,
                    'parent_directory': os.path.basename(root)
                })

            result.append(current_dir)

        return result

    def save_as_json(self, filename):
        try:
            with open(filename, 'w') as file:
                json.dump(self.result, file, indent=4)
        except IOError:
            logger.error(f"Ошибка доступа к файлу {filename}")
        else:
            logger.info(f"Сохранил данные сканирования в json файл и именем {filename}")

    def save_as_csv(self, filename):
        keys = self.result[0].keys()
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.result)
        except IOError:
            logger.error(f"Ошибка доступа к файлу {filename}")
        else:
            logger.info(f"Сохранил данные сканирования в csv файл и именем {filename}")

    def save_as_pickle(self, filename):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.result, file)
        except IOError:
            logger.error(f"Ошибка доступа к файлу {filename}")
        else:
            logger.info(f"Сохранил данные сканирования в бинарный файл и именем {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Принимает путь, формат сохранения и имя файла сохранения результата сканирования ")
    parser.add_argument('-path', type=str, default=os.getcwd())
    parser.add_argument('-json', type=str, default=None)
    parser.add_argument('-csv', type=str, default=None)
    parser.add_argument('-bin', type=str, default=None)
    args = parser.parse_args()

    if args.json or args.csv or args.bin:

        my_dir = ScanDirectory(args.path)
        if args.json:
            my_dir.save_as_json(args.json)
        if args.csv:
            my_dir.save_as_csv(args.csv)
        if args.bin:
            my_dir.save_as_pickle(args.bin)
    else:
        print("Не указан файл сохранения данных")
        logger.info("Не указан файл сохранения данных")
