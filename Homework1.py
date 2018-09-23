""" Homework #1 - Jady Rodriguez """

import csv
import sqlite3


FILE_PATH = r'/Users/jadyrodriguez/Documents/nyu/classes/Class 1/session_1_working_files/weather_newyork.csv'
DB_FILE_PATH = r'/Users/jadyrodriguez/Documents/nyu/classes/Class 1/session_1_working_files/session_1.db'


def calc_with_csv(weather_file):
    """
    Function that reads input weather file and uses csv module to
    calculate the min_temp, max_temp, count, and mean of temperatures provided.
    Sentence of all variables is printed and min_temp, max_temp, count, and mean are returned.

    Args:
        - weather_file (str): path of relevant weather file to be read in

    Returns:
        - min_temp (int): minimum temperature
        - max_temp (int): maximum temperature
        - count (int): count of all temperatures
        - mean (int): mean of temperatures
    """

    count = 0
    mean_temps = []

    with open(weather_file) as f:
        file_reader = csv.reader(f)
        next(file_reader)
        for row in file_reader:
            count += 1
            mean_temps.append(int(row[1]))

    min_temp, max_temp = min(mean_temps), max(mean_temps)
    mean = sum(mean_temps) / count
    print("Count: {}, Max: {}, Min: {}, Mean: {}".format(count, max_temp, min_temp, mean))

    return min_temp, max_temp, count, mean


def calc_with_builtin(weather_file):
    """
    Function that reads input weather file and uses built-in python functionality to
    calculate the min_temp, max_temp, count, and mean of temperatures provided.
    Sentence of all variables is printed and min_temp, max_temp, count, and mean are returned.

    Args:
        - weather_file (str): path of relevant weather file to be read in

    Returns:
        - min_temp (int): minimum temperature
        - max_temp (int): maximum temperature
        - count (int): count of all temperatures
        - mean (int): mean of temperatures
    """

    count = 0
    mean_temps = []

    with open(weather_file) as f:
        next(f)
        for line in f:
            items = line.rstrip().split(',')
            count += 1
            mean_temps.append(int(items[1]))

    min_temp, max_temp = min(mean_temps), max(mean_temps)
    mean = sum(mean_temps) / count
    print("Count: {}, Max: {}, Min: {}, Mean: {}".format(count, max_temp, min_temp, mean))

    return min_temp, max_temp, count, mean


def calc_with_sqlite3(weather_file):
    """
    Function that reads input weather db file and uses sqlite3 module to
    calculate the min_temp, max_temp, count, and mean of temperatures provided.
    Sentence of all variables is printed and min_temp, max_temp, count, and mean are returned.

    Args:
        - weather_file (str): path of relevant weather file to be read in

    Returns:
        - min_temp (int): minimum temperature
        - max_temp (int): maximum temperature
        - count (int): count of all temperatures
        - mean (int): mean of temperatures
    """

    count = 0
    mean_temps = []

    conn = sqlite3.connect(weather_file)
    c = conn.cursor()
    temps = c.execute('SELECT mean_temp FROM weather_newyork')

    for item in temps:
        count += 1
        mean_temps.append(item[0])
    min_temp, max_temp = min(mean_temps), max(mean_temps)
    mean = sum(mean_temps) / count
    print("Count: {}, Max: {}, Min: {}, Mean: {}".format(count, max_temp, min_temp, mean))

    return min_temp, max_temp, count, mean


if __name__ == '__main__':
    calc_with_csv(FILE_PATH)
    calc_with_builtin(FILE_PATH)
    calc_with_sqlite3(DB_FILE_PATH)
