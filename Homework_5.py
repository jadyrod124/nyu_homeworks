import json
import sqlite3
import sys
import jinja2

class Product:
    """
    Product Class

    """
    def __init__(self, prod_id):
        self.id = prod_id
        rows = Product._query_db(self.id)
        self.brand = rows[0][0]
        self.list_price = rows[0][1]
        self.description = rows[0][2]
        self.name = rows[0][4]
        self.sale_price = rows[0][5]

    @staticmethod
    def _query_db(prod_id):
        conn = sqlite3.connect('/Users/jadyrodriguez/Documents/nyu/homeworks/nyu_homeworks/Homework5/session_5_working_files/session_5.db')
        cursor = conn.cursor()
        query = "SELECT * FROM product WHERE product_id = '{}';".format(prod_id)
        rows = cursor.execute(query)
        return rows.fetchall()

    def __str__(self):
        return 'Product(id={}, brand={}, sale_price={})'.format(self.id, self.brand, self.sale_price)

    def get_savings_pct(self):
        return int(((self.list_price - self.sale_price)/self.list_price)*100)



prod_id = sys.argv[1]
this_product = Product(prod_id)
temp_dir = '/Users/jadyrodriguez/Documents/nyu/homeworks/nyu_homeworks/Homework5/session_5_working_files/templates'
env = jinja2.Environment()
env.loader = jinja2.FileSystemLoader(temp_dir)

template = env.get_template('product.html')
completed_page = template.render(product=this_product)

wfh = open(prod_id + '.html', 'w')
wfh.write(completed_page)
wfh.close()

