from data.data import Datos
from data.data_direccion import DatosDireccion
from data.data_deposito import DatosDeposito
from data.data_pedido import DatosPedido
from classes import Usuario
import custom_exceptions

class DatosUsuario(Datos):
    
    @classmethod
    def login(cls, email, password, noClose = False):
        """
        Busca un usuario en la BD que tenga el email y la contraseña que recibe como parámetro. Si no hay ninguno, devuelve False.
        """
        cls.abrir_conexion()
        try:
            sql = ("SELECT usuarios.idUsuario, \
                usuarios.nroDoc, \
                usuarios.nombre, \
                usuarios.apellido, \
                usuarios.email, \
                usuarios.password, \
                usuarios.idTipoUsuario, \
                usuarios.idTipoDoc, \
                usuarios.idDireccion, \
                usuarios.idNivel \
                from usuarios where email = %s and password = %s")
            values = (email, password)
            cls.cursor.execute(sql,values)
            usuarios = cls.cursor.fetchall()
            if len(usuarios) > 0:
                usu = usuarios[0]
                direc = DatosDireccion.get_one_id(usu[8])
                depositos = DatosDeposito.get_by_user_id(usu[0])
                da = [d for d in depositos if d.isActivo()]
                dv = [d for d in depositos if not(d.isActivo())]
                ped = DatosPedido.get_by_user_id(usu[0])
                usuario = Usuario(usu[0],usu[1],usu[7],usu[2],usu[3],usu[5],usu[6],direc,da,dv,ped,usu[9])
                usuario.calcularTotalEcopuntos()
                return usuario
            else:
                raise custom_exceptions.ErrorDeConexion(origen="data_usuario.login()",
                                                        msj_adicional = "Usuario inexistente")

        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_usuario.login()",
                                                    msj=str(e),
                                                    msj_adicional="Error buscando usuario en la BD para realizar el login.")
        finally:
            if not(noClose):
                cls.cerrar_conexion()


    @classmethod
    def get_by_id(cls, id, noClose = False):
        """
        Busca un usuario en la BD segun su id.
        """
        try:
            cls.abrir_conexion()
            sql = ("SELECT usuarios.idUsuario, \
                usuarios.nroDoc, \
                usuarios.nombre, \
                usuarios.apellido, \
                usuarios.email, \
                usuarios.password, \
                usuarios.idTipoUsuario, \
                usuarios.idTipoDoc, \
                usuarios.idDireccion, \
                usuarios.idNivel \
                from usuarios where usuarios.idUsuario = {}").format(id)
            cls.cursor.execute(sql)
            usuarios = cls.cursor.fetchall()
            if len(usuarios) > 0:
                usu = usuarios[0]
                direc = DatosDireccion.get_one_id(usu[8])
                depositos = DatosDeposito.get_by_user_id(usu[0])
                da = [d for d in depositos if d.isActivo()]
                dv = [d for d in depositos if not(d.isActivo())]
                ped = DatosPedido.get_by_user_id(usu[0])
                usuario = Usuario(usu[0],usu[1],usu[7],usu[2],usu[3],usu[5],usu[6],direc,da,dv,ped,usu[9])
                usuario.calcularTotalEcopuntos()
                return usuario
            else:
                raise custom_exceptions.ErrorDeConexion(origen="data_usuario.get_by_id()",
                                                        msj_adicional = "Usuario inexistente")

        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_usuario.get_by_id()",
                                                    msj=str(e),
                                                    msj_adicional="Error buscando usuario en la BD.")
        finally:
            if not(noClose):
                cls.cerrar_conexion()


    @classmethod
    def update_nivel(cls,uid,id_nivel):
        """
        Asigna un nuevo nivel a un usuario
        """
        try:
            cls.abrir_conexion()
            sql = ("UPDATE usuarios SET idNivel={} WHERE idUsuario={}").format(id_nivel,uid)
            cls.cursor.execute(sql)
            cls.db.commit()
            return True
        except Exception as e:
            raise custom_exceptions.ErrorDeConexion(origen="data_usuario.update_nivel()",
                                                    msj=str(e),
                                                    msj_adicional="Error actualizando un nivel de un usuario en la BD.")
        finally:
            cls.cerrar_conexion()