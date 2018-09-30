"""
    Homework #2 ad_buys_agg.py
    Author: Jady Rodriguez jr5182@nyu.edu
    Last modified: 9/30/2018

"""

import csv
import sqlite3


AD_BUYS_FILE = r'/Users/jadyrodriguez/Documents/nyu/classes/Class 2/session_2_working_files/homework/ad_buys.csv'
AD_COMPANIES = r'/Users/jadyrodriguez/Documents/nyu/classes/Class 2/session_2_working_files/homework/ad_companies.csv'
SQL_TABLES = r'/Users/jadyrodriguez/Documents/nyu/classes/Class 2/session_2_working_files/homework/session_2.db'


def by_builtin():
    """
    Reads in two csv files and returns an aggregated list of tuples with ad company information
    Returns:
        - listed_results (list): list of tuples each with buyer_id, company_name, and volume
    """
    ad_buyers_dict = {}

    with open(AD_BUYS_FILE, 'r') as fh:
        reader = csv.reader(fh)
        next(reader)
        for date_time, buyer_id, seller_id, volume, price in reader:
            if int(buyer_id) in ad_buyers_dict.keys():
                ad_buyers_dict[int(buyer_id)]['volume'] += int(volume)
            else:  # why needed else?
                ad_buyers_dict[int(buyer_id)] = {
                    'volume': int(volume)
                }

    with open(AD_COMPANIES, 'r') as fh_companies:
        reader_companies = csv.reader(fh_companies)
        next(reader_companies)
        for company_id, company_name, city, state in reader_companies:
            if int(company_id) in ad_buyers_dict.keys():
                ad_buyers_dict[int(company_id)].update({
                    'company_name': company_name
                })

    ad_buyers_dict = {key: dict_ for key, dict_ in ad_buyers_dict.items() if 'company_name' in dict_}

    listed_results = [
        (
            key,
            ad_buyers_dict[key]['company_name'],
            ad_buyers_dict[key]['volume']
        )
        for key in ad_buyers_dict
    ]

    return sorted(listed_results, key=lambda x: x[2], reverse=True)


def by_sql():
    """
    Reads in sql db file and returns an aggregated list of tuples with ad company information
    Returns:
        - listed_results (list): list of tuples each with buyer_id, company_name, and volume
    """

    conn = sqlite3.connect(SQL_TABLES)
    cursor = conn.cursor()
    query = 'SELECT ad_buys.buyer_id, ad_companies.company_name, SUM(ad_buys.volume) \
             FROM ad_buys \
             INNER JOIN ad_companies \
             ON ad_buys.buyer_id = ad_companies.company_id \
             GROUP BY ad_buys.buyer_id \
             ORDER BY ad_buys.volume;'
    joined_table = cursor.execute(query)

    listed_results = [row for row in joined_table]

    return listed_results


if __name__ == '__main__':
    by_builtin()
    by_sql()
