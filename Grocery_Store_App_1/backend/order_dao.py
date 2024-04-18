from sql_connection import get_sql_connection
from datetime import datetime

def insert_order(connection, order):
    # Insert order, then insert order_details for each product in the order
    cursor = connection.cursor()
    query = ("INSERT INTO orders (customer_name, total, datetime)"
            "VALUES (%s, %s, %s)")
    order_data = (order['customer_name'], order['grand_total'], datetime.now())
    cursor.execute(query, order_data)
    order_id = cursor.lastrowid

    order_details_query = ("INSERT INTO order_details"
                           "(order_id, product_id, quantity, total_price)"
                           "VALUES (%s, %s, %s, %s)")
    order_details_data = []

    for order_detail_record in order['order_details']:
        # Insert every product in the order (dictionary)
        order_details_data.append([
            order_id,
            int(order_detail_record['product_id']),
            float(order_detail_record['quantity']),
            float(order_detail_record['total_price'])
        ])
    
    cursor.executemany(order_details_query, order_details_data)

    connection.commit()

    return order_id

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)

    response = []
    for (order_id, customer_name, total, datetime) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': datetime
        })
    
    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    print(insert_order(connection, {
        'customer_name': 'John Doe',
        'grand_total': '100',
        'order_details': [
            {
                'product_id': 1,
                'quantity': 2,
                'price_per_unit': 50
            },
            {
                'product_id': 3,
                'quantity': 1,
                'price_per_unit': 30
            }
        ]
    }))