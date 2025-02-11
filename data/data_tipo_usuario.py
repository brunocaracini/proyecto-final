from classes import TipoUsuario
from data.data import Datos
import custom_exceptions
from classes import TipoUsuario


class DatosTipoUsuario(Datos):
    
    @classmethod
    def get_by_id(cls, id, noClose = False):
        """
        Busca un tipo de usuario en la BD segun su id.
        """
        try:
            cls.abrir_conexion()
            sql = ("SELECT tiposUsuario.idTipoUsuario, \
                tiposUsuario.nombre \
                from tiposUsuario where tiposUsuario.idTipoUsuario = {} and estado != 'eliminado'").format(id)
            cls.cursor.execute(sql)
            tipoUsu = cls.cursor.fetchall()[0]
            if len(tipoUsu) > 0:
                modulos = cls.get_modulos(tipoUsu[0])
                return TipoUsuario(tipoUsu[0],tipoUsu[1],modulos)
            else:
                raise custom_exceptions.ErrorDeConexion(origen="data_tipo_usuario.get_by_id()",
                                                        msj_adicional = "Tipo de usuario inexistente")

        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_tipo_usuario.get_by_id()",
                                                    msj=str(e),
                                                    msj_adicional="Error buscando tipo de usuario en la BD.")
    
    @classmethod
    def add_one(cls, nombre, noClose = False):
        """
        Añade un nuevo Tipo de Usuario a la BD.
        """
        try:
            cls.abrir_conexion()
            sql = ("INSERT into tiposUsuario (nombre) values (%s)")
            values = (nombre,)
            cls.cursor.execute(sql,values)
            cls.db.commit()
        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_tipo_usuario.add_one()",
                                                    msj=str(e),
                                                    msj_adicional="Error añadiendo un nuevo Tipo de Usuario a la BD.")
    
    @classmethod
    def baja(cls, id_tu_baja, id_tu_reemplazo, noClose = False):
        """
        Elimina un Tipo de Usuario, sus permisos y asigna un Tipo de Usuario en reemplazo a los usuarios del tipo eliminado.
        """
        try:
            cls.abrir_conexion()

            #Elimino permisos de Acceso de este Tipo de Usuario.
            modulos = cls.get_modulos(id_tu_baja)
            for mod in modulos:
                sql = ("Delete from permisosAcceso where idTipoUsuario = %s and idModulo = %s")
                values = (id_tu_baja,mod)
                cls.cursor.execute(sql,values)

            #Actualizo el Tipo de Usuario de los usuarios con el tipo a eliminar
            sql = ("Update usuarios set idTipoUsuario = %s where idTipoUsuario = %s")
            values = (id_tu_reemplazo,id_tu_baja)
            cls.cursor.execute(sql,values)

            #Elimino el tipo de usuario de la BD.
            sql = ("Update tiposUsuario set estado = 'eliminado' where idTipoUsuario = %s")
            values = (id_tu_baja,)
            cls.cursor.execute(sql,values)
            
            cls.db.commit()
        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_tipo_usuario.baja()",
                                                    msj=str(e),
                                                    msj_adicional="Error eliminando un Tipo de Usuario a la BD.")

    @classmethod
    def get_all(cls, noClose = False):
        """
        Busca tosos los tipos de usuario en la BD.
        """
        try:
            cls.abrir_conexion()
            sql = ("SELECT tiposUsuario.idTipoUsuario, \
                tiposUsuario.nombre \
                from tiposUsuario where estado != 'eliminado'")
            cls.cursor.execute(sql)
            tiposUsu_ = cls.cursor.fetchall()
            tiposUsu = []
            for tu in tiposUsu_:
                modulos = cls.get_modulos(tu[0])
                tiposUsu.append(TipoUsuario(tu[0],tu[1],modulos))
            return tiposUsu

        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_tipo_usuario.get_all()",
                                                    msj=str(e),
                                                    msj_adicional="Error buscando todos los tipo de usuario en la BD.")
    
    @classmethod
    def add_permiso(cls, idTU, idMod, noClose = False):
        """
        Añade un permiso para un Tipo de Usuario
        """
        try:
            cls.abrir_conexion()
            sql = ("select idTipoUsuario from permisosAcceso where idTipoUsuario = %s and idModulo = %s")
            values = (idTU, idMod)
            cls.cursor.execute(sql, values)
            res = cls.cursor.fetchone()
            if res != None:
                return False
            else:
                sql = ("INSERT into permisosAcceso (idTipoUsuario, idModulo) VALUES (%s,%s)")
                values = (idTU, idMod)
                cls.cursor.execute(sql, values)
                cls.db.commit()
                return True

        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_tipo_usuario.add_permiso()",
                                                    msj=str(e),
                                                    msj_adicional="Error añadiendo un permiso para un Tipo de Usuario en la BD.")
    
    @classmethod
    def remove_permiso(cls, idTU, idMod, noClose = False):
        """
        Borra un permiso para un Tipo de Usuario
        """
        try:
            cls.abrir_conexion()
            sql = ("select idTipoUsuario from permisosAcceso where idTipoUsuario = %s and idModulo = %s")
            values = (idTU, idMod)
            cls.cursor.execute(sql, values)
            res = cls.cursor.fetchone()
            if res != None:
                sql = ("Delete from permisosAcceso where idTipoUsuario = %s and idModulo = %s")
                values = (idTU, idMod)
                cls.cursor.execute(sql, values)
                cls.db.commit()
                return True
            else:
                return False

        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_tipo_usuario.remove_permiso()",
                                                    msj=str(e),
                                                    msj_adicional="Error borrando un permiso para un Tipo de Usuario en la BD.")

    @classmethod
    def get_modulos(cls,idTipUsu,noClose = False):
        """
        Obtiene los modulos a los que puede acceder un tipo de usuario en base a su ID
        """
        try:
            cls.abrir_conexion()
            sql = ("SELECT idModulo from permisosAcceso where idTipoUsuario = %s")
            values = (idTipUsu,)
            cls.cursor.execute(sql,values)
            mods = cls.cursor.fetchall()
            modulos = []
            for mod in mods:
                modulos.append(mod[0])
            return modulos

        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_tipo_usuario.get_modulos()",
                                                    msj=str(e),
                                                    msj_adicional="Error obteniendo los modulos a los que puede acceder un tipo de usuario en base a su IDD.")