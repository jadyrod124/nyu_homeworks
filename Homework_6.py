import flask
import sqlite3


app = flask.Flask(__name__)   # a Flask object


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
        conn = sqlite3.connect(
            '/Users/jadyrodriguez/Documents/nyu/homeworks/nyu_homeworks/Homework5/session_5_working_files/session_5.db')
        cursor = conn.cursor()
        query = "SELECT * FROM product WHERE product_id = '{}';".format(prod_id)
        rows = cursor.execute(query)
        return rows.fetchall()

    def __str__(self):
        return 'Product(id={}, brand={}, sale_price={})'.format(self.id, self.brand, self.sale_price)

    def get_savings_pct(self):
        return int(((self.list_price - self.sale_price) / self.list_price) * 100)


@app.route('/')                          # called when visiting web URL 127.0.0.1:8000/
def list_products():
    conn = sqlite3.connect(
        '/Users/jadyrodriguez/Documents/nyu/homeworks/nyu_homeworks/Homework5/session_5_working_files/session_5.db')
    cursor = conn.cursor()
    query = "SELECT product_id FROM product;"
    rows = cursor.execute(query)
    product_list = []
    for row in rows:
        product_list.append(Product(row[0]))
    return flask.render_template('product_list.html',
                                 product_list=product_list)


@app.route('/product')
def view_product():
    prod_id = flask.request.args.get('product_id')
    product = Product(prod_id)
    # return '<H1>Hello Product {}...</H1>'.format(prod_id)
    return flask.render_template('product_view.html',
                                 product=product,
                                 image_path='images/{}.jpg'.format(product.id))

if __name__ == '__main__':
    app.run(debug=True, port=8002)