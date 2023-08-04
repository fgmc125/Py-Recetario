-- CREATE DATABASE recetario;

USE recetario;

CREATE TABLE IF NOT EXISTS recetas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    tiempo_preparacion TINYINT NOT NULL,
    tiempo_coccion TINYINT NOT NULL,
    instrucciones TEXT,
    creacion  DATETIME NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ingredientes (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre varchar(255) NOT NULL,
  unidad varchar(150) DEFAULT NULL,
  cantidad decimal(10,2) DEFAULT NULL,
  id_receta int DEFAULT NULL,
  KEY id_recipe (id_receta),
  FOREIGN KEY (id_receta) REFERENCES recetas(id)
);
