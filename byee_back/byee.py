import http.server
import socketserver
import json
import mysql.connector

PORT = 8000

def create_conection():
    connection = mysql.connector.connect(
        host='localhost',
        user='luis',
        password='71063699La*#',
        database="byee_database"
    )
    return connection

def get_all_users():
    connection = create_conection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Usuario')
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

def get_all_products():
    connection = create_conection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Produto')
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

def create_product(product_data):
    connection = create_conection()
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
    connection = create_conection()
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

def send_sale(invoice_id):
    connection = create_conection()
    cursor = connection.cursor()

    query = "UPDATE Nota_fiscal_Envio_Venda SET status = 'Enviada' WHERE id = %s"
    cursor.execute(query, (invoice_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return True

def get_invoices_by_comprador(comprador_id):
    connection = create_conection()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM Nota_fiscal_Envio_Venda WHERE fk_id_comprador = %s'
    cursor.execute(query, (comprador_id,))
    invoices = cursor.fetchall()

    cursor.close()
    connection.close()
    return invoices

def create_cart(user_id):
    connection = create_conection()
    cursor = connection.cursor(dictionary=True)

    query = 'INSERT INTO Carrinho_Usuario_Comprador (fk_Usuario_id) VALUES (%s)'
    values = (user_id)
    
    cursor.execute(query, values)
    cart_id = cursor.lastrowid # Obtém o ID do carrinho criado

    connection.commit()
    cursor.close()
    connection.close()
    return True

def get_user_cart_id(user_id):
    connection = create_conection()
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
    connection = create_conection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT 
        Produto.id,
        Produto.nome,
        Produto.tipo,
        Produto.preco,
        Produto.SKU
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

def add_product_to_cart(cart_id, product_id):
    connection = create_conection()
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

def get_products_by_type(product_type):
    connection = create_conection()
    cursor = connection.cursor(dictionary=True)
    
    query = 'SELECT * FROM Produto WHERE tipo = %s'
    values = (product_type,)
    cursor.execute(query, values)
    products = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return products

def delete_product(data):
    connection = create_conection()
    cursor = connection.cursor(dictionary=True)
    query = 'DELETE FROM Produto WHERE id = %s'
    values = [data["id"]]
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

def update_product(updated_data):
    connection = create_conection()
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


class RequestHandler(http.server.BaseHTTPRequestHandler):

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/cart-items/'):
            try:
                # Extraindo o cart_id da URL
                cart_id = int(self.path.split('/')[-1])
                self._set_headers(200)
                cart_items = get_cart_items_by_cart_id(cart_id)
                print(cart_items)
                self.wfile.write(json.dumps(cart_items).encode())
            except Exception as e:
                # Tratamento de erro genérico, ajuste conforme necessárioALTER TABLE Nota_fiscal_Envio_Venda MODIFY id INT AUTO_INCREMENT;
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        elif self.path.startswith('/user-cart-id/'):
            try:
                # Extraindo o user_id da URL
                user_id = int(self.path.split('/')[-1])
                cart_id = get_user_cart_id(user_id)
                if cart_id is not None:
                    self._set_headers(200)
                    self.wfile.write(json.dumps({'cart_id': cart_id}).encode())
                else:
                    self._set_headers(404)  # Nenhum carrinho encontrado para o usuário
                    self.wfile.write(json.dumps({'error': 'Cart not found'}).encode())
            except ValueError:
                # Erro ao converter user_id para int
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Invalid user_id'}).encode())
            except Exception as e:
                # Outros erros
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': str(e)}).encode())

        elif self.path == '/users':
            self._set_headers(200)
            users = get_all_users()
            self.wfile.write(json.dumps(users).encode())
        elif self.path == '/products':
            self._set_headers(200)
            products = get_all_products()
            self.wfile.write(json.dumps(products).encode())
        elif self.path.startswith('/products_by_type'):
            self._set_headers(200)
            product_type = self.path.split('/')[-1]
            products = get_products_by_type(product_type)
            self.wfile.write(json.dumps(products).encode())
        else:
            self._set_headers(404)

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_POST(self):
        if self.path == '/create-cart':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            user_data = json.loads(post_data)

            cart_id = create_cart(user_data['user_id'])
            if cart_id:
                self._set_headers(201)
                self.wfile.write(json.dumps({'cart_id': cart_id}).encode())
            else:
                self._set_headers(400)

        elif self.path == '/create-product':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            product_data = json.loads(post_data)
            product_id = create_product(product_data)
            if product_id:
                self._set_headers(201)
                self.wfile.write(json.dumps({'id': product_id}).encode())
            else:
                self._set_headers(400)
        elif self.path == '/user-cart-id':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            user_data = json.loads(post_data)

            cart_id = get_user_cart_id(user_data['user_id'])
            if cart_id:
                self._set_headers(201)
                self.wfile.write(json.dumps(cart_id).encode())
            else:
                self._set_headers(400)
        elif self.path == '/add-product-to-cart':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            product_data = json.loads(post_data)

            result = add_product_to_cart(product_data['cart_id'], product_data['product_id'])
            if result:
                self._set_headers(201)
                self.wfile.write(json.dumps({'result': result}).encode())
            else:
                self._set_headers(400)
        elif self.path == '/payment-invoice':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            invoice_data = json.loads(post_data)
            invoice_id = create_invoice(invoice_data)
            if invoice_id:
                self._set_headers(201)
                self.wfile.write(json.dumps({'invoice_id': invoice_id}).encode()) #todo
            else:
                self._set_headers(400)
        else:
            self._set_headers(404)

    def do_PUT(self):
        if self.path.startswith('/update-product'):
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            update_data = json.loads(put_data)
            update_product(update_data)
            self._set_headers(200)
        else:
            self._set_headers(404)
    
    def do_DELETE(self):
        if self.path.startswith('/delete-product'):
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data)
            delete_product(data)
            self._set_headers(200)
        else:
            self._set_headers(404)

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Conectado na porta {PORT}")
    httpd.serve_forever()