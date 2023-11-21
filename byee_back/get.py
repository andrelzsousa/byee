
from utils import create_connection
from datetime import datetime, date

def get_all_users():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT Usuario.id, Usuario.nome, Usuario.telefone, Usuario.is_del, Usuario.endereco_FK, endereco.rua, endereco.numero, endereco.bairro, endereco.cidade FROM Usuario LEFT JOIN endereco ON Usuario.endereco_FK = endereco.endereco_PK')
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users


def get_all_products():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Produto')
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

def get_invoices_by_comprador(comprador_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM Nota_fiscal_Envio_Venda WHERE fk_id_comprador = %s'
    cursor.execute(query, (comprador_id,))
    invoices = cursor.fetchall()

    # Converter campos de data/hora em strings
    for invoice in invoices:
        for key, value in invoice.items():
            if isinstance(value, (datetime, date)):
                invoice[key] = value.isoformat()

    cursor.close()
    connection.close()
    return invoices

def get_user_cart_id(user_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT id FROM Carrinho_Usuario_Comprador WHERE fk_Usuario_id = %s'
    cursor.execute(query, (user_id,))
    cart_ids = cursor.fetchall()

    cursor.close()
    connection.close()

    if len(cart_ids) == 0:
        return "Nenhum carrinho associado"
    else:
        return cart_ids[0]['id']
    
def get_cart_items_by_cart_id(cart_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT 
        Produto.id,
        Produto.nome,
        Produto.tipo,
        Produto.preco,
        Produto.SKU,
        Produto.is_del
    FROM 
        Contem
    JOIN 
        Produto ON Contem.fk_Produto_id = Produto.id
    WHERE 
        Contem.fk_Carrinho_id = %s;
    '''

    cursor.execute(query, (cart_id,))
    cart_items = cursor.fetchall()

    cursor.close()
    connection.close()
    return cart_items

def get_products_by_type(product_type):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = 'SELECT * FROM Produto WHERE tipo = %s'
    values = (product_type,)
    cursor.execute(query, values)
    products = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return products

def get_cart_total(cart_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = '''SELECT SUM(Produto.preco) AS total
               FROM Produto
               INNER JOIN Contem ON Produto.id = Contem.fk_Produto_id
               WHERE Contem.fk_Carrinho_id = %s AND Produto.is_del <> 1'''
    values = (cart_id,)

    cursor.execute(query, values)
    cart_total = cursor.fetchone()
    
    cursor.close()
    connection.close()
    return float(cart_total['total']) if cart_total['total'] is not None else 0.0

def get_user_average_purchase_price(user_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT AVG(valor) AS media_precos_compras
    FROM Nota_fiscal_Envio_Venda
    WHERE fk_id_comprador = %s
    '''
    cursor.execute(query, (user_id,))
    average_price = cursor.fetchone()['media_precos_compras']

    cursor.close()
    connection.close()

    return float(average_price) if average_price is not None else 0.0


def get_user_cheapest_purchase(user_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT id, valor
    FROM Nota_fiscal_Envio_Venda
    WHERE fk_id_comprador = %s
    ORDER BY valor ASC
    LIMIT 1
    '''
    cursor.execute(query, (user_id,))
    cheapest_purchase = cursor.fetchone()

    cursor.close()
    connection.close()

    return cheapest_purchase


def get_user_most_expensive_purchase(user_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT id, valor
    FROM Nota_fiscal_Envio_Venda
    WHERE fk_id_comprador = %s
    ORDER BY valor DESC
    LIMIT 1
    '''
    cursor.execute(query, (user_id,))
    most_expensive_purchase = cursor.fetchone()

    cursor.close()
    connection.close()

    return most_expensive_purchase

def find_most_expensive_products():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT *
    FROM Produto
    WHERE preco = (SELECT MAX(preco) FROM Produto)
    '''

    cursor.execute(query)
    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products

def calculate_average_prices_by_type():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT tipo, AVG(preco) AS media_precos
    FROM Produto
    GROUP BY tipo
    '''

    cursor.execute(query)
    average_prices = cursor.fetchall()

    cursor.close()
    connection.close()

    return average_prices

def find_users_with_items_in_cart():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT DISTINCT Usuario.*
    FROM Usuario
    INNER JOIN Carrinho_Usuario_Comprador ON Usuario.id = Carrinho_Usuario_Comprador.fk_Usuario_id
    INNER JOIN Contem ON Carrinho_Usuario_Comprador.id = Contem.fk_Carrinho_id
    '''

    cursor.execute(query)
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users

def calculate_average_products_per_cart():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT AVG(quantidade_produtos) AS media_produtos_por_carrinho
    FROM (SELECT fk_Carrinho_id, COUNT(*) AS quantidade_produtos FROM Contem GROUP BY fk_Carrinho_id) AS carrinho_info
    '''

    cursor.execute(query)
    average_products = cursor.fetchone()['media_produtos_por_carrinho']

    cursor.close()
    connection.close()

    return average_products