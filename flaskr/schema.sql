DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS pedido;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE pedido (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre_cliente TEXT UNIQUE NOT NULL,
  estado_cocina BOOLEAN,
  estado_entrega BOOLEAN,
  forma_de_pago TEXT UNIQUE NOT NULL,
  fecha_de_pedido TEXT UNIQUE NOT NULL
);

INSERT INTO pedido(nombre_cliente,estado_cocina, estado_entrega, forma_de_pago, fecha_de_pedido) 
VALUES ('Juan',true,false,'Efectivo','2020-01-01');