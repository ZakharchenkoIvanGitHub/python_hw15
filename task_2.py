"""
Создайте модуль и напишите в нём функцию,
которая получает на вход дату в формате DD.MM.YYYY
Функция возвращает истину, если дата может
существовать или ложь, если такая дата невозможна.
Для простоты договоримся, что год может быть в диапазоне [1, 9999].
Весь период (1 января 1 года - 31 декабря 9999 года) действует
Григорианский календарь.
Проверку года на високосность вынести в отдельную защищённую функцию.
"""

import logging
import argparse
from datetime import datetime

logging.basicConfig(filename="log/log2.log",
                    filemode="a",
                    encoding="utf-8",
                    format='{levelname:<6} - {asctime} в строке {lineno:>3d}, функция - "{funcName}()" : {msg}',
                    style="{",
                    level=logging.INFO
                    )
logger = logging.getLogger("my_logger")


def check_date(date_str: str) -> bool:
    logger.info(f"Проверяю введенную дату {date_str}")
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
    except ValueError:
        logger.error(f"Проверка даты {date_str} не успешна")
        return False
    else:
        logger.info(f"Дата  {date_str} существует")
        leap_year = _leap_year(date_str.split(".")[2])
        leap_text = "год високоснный" if leap_year else "год не високоснный"
        print(leap_text)
        logger.info(f"{leap_year} {leap_text}")
        return True


def _leap_year(year_str: str) -> bool:
    year = int(year_str)
    return year % 400 == 0 or year % 4 == 0 and year % 100 != 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Принимает текстовую дату в формате DD.MM.YYYY и проверяет, существует ли она ")
    parser.add_argument('-date', type=str, default=datetime.now().date().strftime('%d.%m.%Y'))
    try:
        args = parser.parse_args()
    except:
        print("Не верные входные данные")
        logger.error(f"Не верные входные данные")

    else:
        print(f"Проверяю строку {args.date}")
        print("дата существует" if check_date(args.date) else "дата не существует")
