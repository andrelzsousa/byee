from utils import create_connection


def create_product(product_data):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = '''INSERT INTO Produto 
               (nome, tipo, preco, SKU, fk_Usuario_vendedor_fk) 
               VALUES (%s, %s, %s, %s, %s)'''
    values = (
        product_data["nome"], 
        product_data["tipo"], 
        product_data["preco"], 
        product_data["SKU"], 
        product_data["fk_Usuario_vendedor_fk"]
    )
    
    cursor.execute(query, values)
    connection.commit()
    product_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return product_id

def create_invoice(sale_data):
    connection = create_connection()
    cursor = connection.cursor()
    query = '''INSERT INTO Nota_fiscal_Envio_Venda 
               (valor, cnpj_emissor, codigo, data_geracao, status, transportadora, data_envio, data_venda, valor_frete, fk_id_comprador) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    values = (
        sale_data["valor"],
        sale_data["cnpj_emissor"],
        sale_data["codigo"],
        sale_data["data_geracao"],
        sale_data["status"],
        sale_data["transportadora"],
        sale_data["data_envio"],
        sale_data["data_venda"],
        sale_data["valor_frete"],
        sale_data["fk_id_comprador"]
    )

    cursor.execute(query, values)
    connection.commit()
    invoice_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return invoice_id

def create_cart(user_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = 'INSERT INTO Carrinho_Usuario_Comprador (fk_Usuario_id) VALUES (%s)'
    values = (user_id)
    
    cursor.execute(query, values)

    connection.commit()
    cursor.close()
    connection.close()
    return True

def add_product_to_cart(cart_id, product_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = 'INSERT INTO Contem (fk_Carrinho_id, fk_Produto_id) VALUES (%s, %s)'
    values = (cart_id, product_id)

    try:
        cursor.execute(query, values)
        connection.commit()
        result = True
    except Exception as e:
        print("Erro ao adicionar produto ao carrinho:", e)
        result = False

    cursor.close()
    connection.close()
    return result