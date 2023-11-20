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