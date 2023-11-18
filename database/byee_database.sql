CREATE DATABASE byee_database;
USE byee_database;

CREATE TABLE endereco (
    endereco_PK INT AUTO_INCREMENT PRIMARY key ,
    rua VARCHAR(255),
    numero VARCHAR(255),
    bairro VARCHAR(255),
    cidade VARCHAR(255)
);

CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    telefone VARCHAR(50),
    endereco_FK INT,
    fk_usuario_presente INT,
    is_del BOOL DEFAULT False,
    FOREIGN KEY (endereco_FK) REFERENCES endereco(endereco_PK),
    FOREIGN KEY (fk_usuario_presente) REFERENCES Usuario(id)
);

CREATE TABLE Carrinho_Usuario_Comprador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fk_Usuario_id INT,
    FOREIGN KEY (fk_Usuario_id) REFERENCES Usuario(id)
);

CREATE TABLE Produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    tipo VARCHAR(255),
    preco INT,
    SKU VARCHAR(255),
    fk_Usuario_vendedor_fk INT,
    is_del BOOL DEFAULT False,
    FOREIGN KEY (fk_Usuario_vendedor_fk) REFERENCES Usuario(id)
);

CREATE TABLE Contem (
    fk_Carrinho_id INT,
    fk_Produto_id INT,
    PRIMARY KEY (fk_Carrinho_id, fk_Produto_id),
    FOREIGN KEY (fk_Carrinho_id) REFERENCES Carrinho_Usuario_Comprador(id),
    FOREIGN KEY (fk_Produto_id) REFERENCES Produto(id)
);

CREATE TABLE Nota_fiscal_Envio_Venda (
    valor INT,
    cnpj_emissor VARCHAR(50),
    codigo INT,
    data_geracao DATE,
    status VARCHAR(255),
    transportadora VARCHAR(255),
    data_envio DATE,
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_venda DATE,
    valor_frete INT,
    fk_id_comprador INT,
    FOREIGN KEY (fk_id_comprador) REFERENCES Carrinho_Usuario_Comprador(fk_Usuario_id)
);

CREATE TABLE Brecho (
    cnpj VARCHAR(50) PRIMARY KEY,
    fk_Usuario_vendedor_fk INT,
    FOREIGN KEY (fk_Usuario_vendedor_fk) REFERENCES Usuario(id)
);

CREATE TABLE Pessoa_fisica (
    cpf VARCHAR(50) PRIMARY KEY,
    fk_Usuario_vendedor_fk INT,
    FOREIGN KEY (fk_Usuario_vendedor_fk) REFERENCES Usuario(id)
);


-- Script de inserção de valores

INSERT INTO endereco (endereco_PK, rua, numero, bairro, cidade) VALUES 
(1, 'Rua das Flores', '123', 'Jardim das Acácias', 'São Paulo'),
(2, 'Avenida Brasil', '500', 'Centro', 'Rio de Janeiro'),
(3, 'Rua das Palmeiras', '321', 'Vila Mariana', 'São Paulo'),
(4, 'Avenida das Nações', '250', 'Funcionários', 'Belo Horizonte'),
(5, 'Rua dos Limoeiros', '87', 'São Pedro', 'Porto Alegre'),
(6, 'Avenida dos Estados', '1010', 'Água Verde', 'Curitiba');


INSERT INTO Usuario (id, nome, telefone, endereco_FK, fk_usuario_presente) VALUES 
(1, 'João Silva', "11999998888", 1, NULL),
(2, 'Maria Oliveira', "21999997777", 2, 1),
(3, 'Pedro Santos', "31999996666", 3, NULL),
(4, 'Ana Costa', "41999995555", 4, NULL),
(5, 'Luiz Souza', "51999994444", 5, 2),
(6, 'Camila Gomes', "61999993333", 6, NULL);

INSERT INTO Carrinho_Usuario_Comprador (id, fk_Usuario_id) VALUES 
(1, 2),
(2, 4),
(3, 5),
(4, 6),
(5, 3),
(6, 1);


INSERT INTO Produto (id, nome, tipo, preco, SKU, fk_Usuario_vendedor_fk) VALUES 
(1, 'Camiseta', 'Roupa', 5000, 'CT123', 1),
(2, 'Calça Jeans', 'Roupa', 8000, 'CJ456', 2),
(3, 'Tênis de Corrida', 'Calçado', 12000, 'TC789', 3),
(4, 'Jaqueta', 'Roupa', 15000, 'JKT321', 4),
(5, 'Vestido Floral', 'Roupa', 9500, 'VF654', 5),
(6, 'Chapéu', 'Acessório', 3000, 'CHP987', 6);

INSERT INTO Contem (fk_Carrinho_id, fk_Produto_id) VALUES 
(1, 2),
(1, 3),
(2, 1),
(3, 4),
(4, 5),
(5, 6),
(6, 1),
(6, 2),
(6, 3);

INSERT INTO Nota_fiscal_Envio_Venda (valor, cnpj_emissor, codigo, data_geracao, status, transportadora, data_envio, id, data_venda, valor_frete, fk_id_comprador) VALUES 
(20000, "12345678901234", 10001, '2023-05-01', 'Enviado', 'TranspExpress', '2023-05-02', 1, '2023-04-30', 1500, 1),
(30000, "23456789012345", 10002, '2023-05-10', 'Pendente', 'Rapidão Cometa', NULL, 2, '2023-05-09', 2000, 2),
(25000, "34567890123456", 10003, '2023-05-15', 'Entregue', 'TranspRápido', '2023-05-16', 3, '2023-05-14', 1000, 3),
(15000, "45678901234567", 10004, '2023-05-20', 'Cancelado', NULL, NULL, 4, '2023-05-18', 0, 4),
(22000, "56789012345678", 10005, '2023-05-25', 'Enviado', 'VoeTransportes', '2023-05-26', 5, '2023-05-24', 1200, 5),
(28000, "67890123456789", 10006, '2023-05-30', 'Pendente', 'Entrega Ninja', NULL, 6, '2023-05-29', 1800, 6);

INSERT INTO Brecho (cnpj, fk_Usuario_vendedor_fk) VALUES 
("87654321000123", 1),
("98765432000123", 2),
("87654321000234", 3),
("98765432000234", 4),
("87654321000345", 5),
("98765432000345", 6);

INSERT INTO Pessoa_fisica (cpf, fk_Usuario_vendedor_fk) VALUES 
("12345678901", 1),
("23456789012", 2),
("34567890123", 3),
("45678901234", 4),
("56789012345", 5),
("67890123456", 6);