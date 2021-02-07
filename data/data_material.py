from data.data import Datos
from classes import Material
import custom_exceptions

class DatosMaterial(Datos):
    @classmethod
    def get_all(cls):
        """
        Obtiene todos los materiales de la BD.
        """
        
        cls.abrir_conexion()
        try:
            sql = ("SELECT idMaterial, \
                           nombre, \
                           unidadMedida, \
                           costoRecoleccion, \
                           stock, \
                           color \
                           FROM materiales WHERE estado!=\"eliminado\";")
            cls.cursor.execute(sql)
            materiales_ = cls.cursor.fetchall()
            materiales = []
            for m in materiales_:
                material_ = Material(m[0],m[1],m[2],m[3],m[4],m[5])
                materiales.append(material_)
            return materiales
            
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_material.get_all()",
                                                    msj=str(e),
                                                    msj_adicional="Error obtieniendo los materiales desde la BD.")
        finally:
            cls.cerrar_conexion()

    
    @classmethod
    def add(cls,nombre,unidad,costoRecoleccion,color):
        """
        Agrega un material a la BD
        """
        cls.abrir_conexion()
        try:
            sql= ("INSERT INTO materiales (nombre,unidadMedida,costoRecoleccion,color,stock,estado) \
                   VALUES (\"{}\",\"{}\",{},\"{}\",0,\"disponible\");".format(nombre,unidad,costoRecoleccion,color))
            cls.cursor.execute(sql)
            cls.db.commit()
            return cls.cursor.lastrowid
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_material.add()",
                                                    msj=str(e),
                                                    msj_adicional="Error dando de alta un material en la BD.")
        finally:
            cls.cerrar_conexion()



    @classmethod
    def update(cls,idMat,nombre,unidad,costoRecoleccion,color):
        """
        Actualiza un material en la BD
        """
        cls.abrir_conexion()
        try:
            sql= ("UPDATE materiales SET nombre=\"{}\",unidadMedida=\"{}\",costoRecoleccion={},color=\"{}\",stock=0,estado=\"disponible\" WHERE idMaterial={};").format(nombre,unidad,costoRecoleccion,color,idMat)
            cls.cursor.execute(sql)
            cls.db.commit()
            return cls.cursor.lastrowid
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_material.update()",
                                                    msj=str(e),
                                                    msj_adicional="Error actualizando un material en la BD.")
        finally:
            cls.cerrar_conexion()

    
    @classmethod
    def delete(cls, id):
        """
        Elimina un material de la BD a partir de su id.
        """
        cls.abrir_conexion()
        try:
            sql = ("UPDATE materiales SET estado = \"eliminado\" WHERE idMaterial={}".format(id))
            cls.cursor.execute(sql)
            cls.db.commit()
            return True
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_material.delete()",
                                                    msj=str(e),
                                                    msj_adicional="Error eliminando un material en la BD.")
        finally:
            cls.cerrar_conexion()