import http.server
import socketserver
import json
import mysql.connector

PORT = 8000

def create_conection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
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
    cursor.close()
    connection.close()
    return True

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

class RequestHandler(http.server.BaseHTTPRequestHandler):

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
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
                # Tratamento de erro genérico, ajuste conforme necessário
                self._set_headers(500)
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
            print(cart_id)
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
        else:
            self._set_headers(404)

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Conectado na porta {PORT}")
    httpd.serve_forever()