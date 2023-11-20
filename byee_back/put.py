from utils import create_connection


def update_product(updated_data):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = '''UPDATE Produto
               SET nome = %s, tipo = %s, preco = %s, SKU = %s, fk_Usuario_vendedor_fk = %s
               WHERE id = %s'''
    values = (
        updated_data["nome"],
        updated_data["tipo"],
        updated_data["preco"],
        updated_data["SKU"],
        updated_data["fk_Usuario_vendedor_fk"],
        updated_data["id"]
    )
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

def send_sale(invoice_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = "UPDATE Nota_fiscal_Envio_Venda SET status = 'Enviada' WHERE id = %s"
    cursor.execute(query, (invoice_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return True

def upd_usr(addr_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = 'UPDATE Usuario SET endereco_FK = NULL WHERE endereco_FK = %s'
    values = (addr_id,)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

def delete_user(data):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = 'UPDATE Usuario SET is_del = 1 WHERE id = %s'
    values = (data,)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

def delete_product(product_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = 'UPDATE Produto SET is_del = 1 WHERE id = %s'
    values = (product_id['id'],)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()