import http.server
import socketserver
import json
from urllib.parse import unquote
from delete import delete_addr, remove_product_from_cart
from get import get_all_products, get_all_users, get_cart_items_by_cart_id, get_cart_total, get_invoices_by_comprador, get_products_by_type, get_user_average_purchase_price, get_user_cart_id, get_user_cheapest_purchase, get_user_most_expensive_purchase
from post import add_product_to_cart, create_cart, create_invoice, create_product
from put import delete_product, delete_user, update_product
from utils import PORT

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
                self.wfile.write(json.dumps(cart_items).encode())
            except Exception as e:
                # Tratamento de erro genérico, ajuste conforme necessárioALTER TABLE Nota_fiscal_Envio_Venda MODIFY id INT AUTO_INCREMENT;
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        elif self.path.startswith('/cart-total/'):
            try:
                # Extraindo o cart_id da URL
                cart_id = int(self.path.split('/')[-1])
                self._set_headers(200)
                cart_total = get_cart_total(cart_id)
                self.wfile.write(json.dumps(cart_total).encode())
            except Exception as e:
                # Tratamento de erro genérico, ajuste conforme necessárioALTER TABLE Nota_fiscal_Envio_Venda MODIFY id INT AUTO_INCREMENT;
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        elif self.path.startswith('/get-user-invoices/'):
            try:
                user_id = int(self.path.split('/')[-1])
                self._set_headers(200)
                cart_total = get_invoices_by_comprador(user_id)
                self.wfile.write(json.dumps(cart_total).encode())
            except Exception as e:
                # Tratamento de erro genérico, ajuste conforme necessárioALTER TABLE Nota_fiscal_Envio_Venda MODIFY id INT AUTO_INCREMENT;
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        elif self.path.startswith('/get-user-invoices-average/'):
            try:
                user_id = int(self.path.split('/')[-1])
                self._set_headers(200)
                average = get_user_average_purchase_price(user_id)
                self.wfile.write(json.dumps(average).encode())
            except Exception as e:
                # Tratamento de erro genérico, ajuste conforme necessárioALTER TABLE Nota_fiscal_Envio_Venda MODIFY id INT AUTO_INCREMENT;
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        elif self.path.startswith('/get-user-most-expensive-invoice/'):
            try:
                user_id = int(self.path.split('/')[-1])
                self._set_headers(200)
                expensive = get_user_most_expensive_purchase(user_id)
                self.wfile.write(json.dumps(expensive).encode())
            except Exception as e:
                # Tratamento de erro genérico, ajuste conforme necessárioALTER TABLE Nota_fiscal_Envio_Venda MODIFY id INT AUTO_INCREMENT;
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        elif self.path.startswith('/get-user-cheapest-invoice/'):
            try:
                user_id = int(self.path.split('/')[-1])
                self._set_headers(200)
                cheapest = get_user_cheapest_purchase(user_id)
                self.wfile.write(json.dumps(cheapest).encode())
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
            product_type = unquote(product_type)
            products = get_products_by_type(product_type)
            self.wfile.write(json.dumps(products).encode())
        else:
            self._set_headers(404)

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
        elif self.path.startswith('/delete-product'):
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data)
            delete_product(data)
            self._set_headers(200)
            self._set_headers(200)
        elif self.path.startswith('/delete-user'):
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data)
            delete_user(data)
            self._set_headers(200)
        else:
            self._set_headers(404)
    
    def do_OPTIONS(self):
        self._set_headers()

    def do_DELETE(self):

        if self.path.startswith('/delete-addr'):
            addr_id = self.path.split('/')[-1]
            delete_addr(addr_id)
            self._set_headers(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
        elif self.path.startswith('/remove-product-from-cart/'):
            try:
                cart_id, product_id = map(int, self.path.split('/')[-2:])
                self._set_headers(200)
                result = remove_product_from_cart(cart_id, product_id)
                self.wfile.write(json.dumps({'result': result}).encode())
            except Exception as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self._set_headers(404)


with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Conectado na porta {PORT}")
    httpd.serve_forever()