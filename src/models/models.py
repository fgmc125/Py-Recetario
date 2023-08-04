from src.models.conector import Conector

class Ingrediente:
    def __init__(self, nombre, unidad, cantidad, id=None):
        self.id = id
        self.nombre = nombre
        self.unidad = unidad
        self.cantidad = cantidad

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'unidad': self.unidad,
            'cantidad': self.cantidad
        }

    def to_list(self):
        return [self.nombre, self.cantidad, self.unidad]

class Receta:
    def __init__(self, nombre, tiempo_preparacion, tiempo_coccion, instrucciones, id=None, creacion=None, ingredientes=[]):
        self.id = id
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.tiempo_preparacion = tiempo_preparacion
        self.tiempo_coccion = tiempo_coccion
        self.instrucciones = instrucciones
        self.creacion = creacion

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'ingredientes': [ingrediente.to_dict() for ingrediente in self.ingredientes],
            'tiempo_preparacion': self.tiempo_preparacion,
            'tiempo_coccion': self.tiempo_coccion,
            'instrucciones': self.instrucciones,
            'creacion': self.creacion
        }


class Model:
    def __init__(self):
        self.conexion = None
        self.__ejecutar_script_sql()

    def __ejecutar_script_sql(self):
        self.conexion = Conector()
        try:
            with open('src/models/script_database.sql', 'r') as sql_file:
                script = sql_file.read()

            queries = script.split(';')

            for query in queries:
                query = query.strip()
                if query:
                    self.conexion.run_query(query)

            print("¡Script SQL ejecutado exitosamente!")
        except FileNotFoundError:
            print("ERROR: No se encontró el archivo 'script_database.sql'")
        except Exception as e:
            print(f"ERROR AL EJECUTAR EL SCRIPT SQL: {e}")
        finally:
            self.conexion = None

    def nueva_receta(self, receta):
        self.conexion = Conector()
        sql = "INSERT INTO recetas (nombre, tiempo_coccion, tiempo_preparacion, instrucciones, creacion) " \
              "VALUES (%s, %s, %s, %s, NOW())"
        data = (receta.nombre, receta.tiempo_coccion, receta.tiempo_preparacion, receta.instrucciones)
        id_receta = self.conexion.run_query(sql, data)

        self.conexion.close()
        self.conexion = Conector()
        for ingrediente in receta.ingredientes:
            sql = "INSERT INTO ingredientes (nombre, cantidad, unidad, id_receta) " \
                  "VALUES (%s, %s, %s, %s)"
            data = (ingrediente.nombre, ingrediente.cantidad, ingrediente.unidad, id_receta)
            self.conexion.run_query(sql, data)

        self.conexion.close()
        return id_receta

    def obtener_todas_recetas(self):
        try:
            self.conexion = Conector()
            sql = "SELECT * FROM recetas"
            data = self.conexion.run_query(sql)

            lista_de_recetas = []

            for row in data:
                receta = Receta(
                    nombre=row[1],
                    tiempo_preparacion=row[2],
                    tiempo_coccion=row[3],
                    instrucciones=row[4],
                    creacion=row[5],
                    id=row[0],
                    ingredientes=[Ingrediente(i[0], i[1], i[2], i[3]) for i in self.__obtener_ingredientes_de_receta(row[0])]
                )
                lista_de_recetas.append(receta)

            return lista_de_recetas
        finally:
            self.conexion.close()

    def __obtener_ingredientes_de_receta(self, recipe_id):
        try:
            self.conexion = Conector()
            sql = "SELECT id, nombre, cantidad, unidad FROM ingredientes WHERE id_receta = %s"
            ingredientes = self.conexion.run_query(sql, (recipe_id,))
            #ingredientes = [list(ingredient) for ingredient in ingredients_data]
            return ingredientes
        finally:
            self.conexion.close()

    def actualizar_receta(self, recipe_id, name, preparation_time, cooking_time, description, ingredients):
        self.conexion = Conector()
        sql = "UPDATE recetas SET nombre = %s, tiempo_preparacion = %s, tiempo_coccion = %s, " \
              "instrucciones = %s WHERE id = %s"
        data = (name, preparation_time, cooking_time, description, recipe_id)
        self.conexion.run_query(sql, data)

        # Eliminar los ingredientes asociados a la receta
        sql = "DELETE FROM ingredientes WHERE id_receta = %s"
        data = (recipe_id,)
        self.conexion.run_query(sql, data)

        # Agregar los nuevos ingredients
        self.conexion.close()
        self.conexion = Conector()
        for ingrediente in ingredients:
            if isinstance(ingrediente, Ingrediente):
                ingrediente = ingrediente.to_dict()

            sql = "INSERT INTO ingredientes (nombre, cantidad, unidad, id_receta) " \
                  "VALUES (%s, %s, %s, %s)"
            data = (ingrediente['nombre'], ingrediente['cantidad'], ingrediente['unidad'], recipe_id)
            self.conexion.run_query(sql, data)

        self.conexion.close()
