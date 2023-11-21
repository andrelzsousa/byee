from put import upd_usr
from utils import create_connection


def delete_addr(addr_id):
    print(addr_id)
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    upd_usr(addr_id)
    query = 'DELETE FROM endereco WHERE endereco_pk = %s'
    values = (addr_id,)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

def remove_product_from_cart(cart_id, product_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = 'DELETE FROM Contem WHERE fk_Carrinho_id = %s AND fk_Produto_id = %s'
    values = (cart_id, product_id)

    try:
        cursor.execute(query, values)
        connection.commit()
        result = True
    except Exception as e:
        print("Erro ao remover produto do carrinho:", e)
        result = False

    cursor.close()
    connection.close()
    return result