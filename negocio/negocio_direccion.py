from negocio.negocio import Negocio
import custom_exceptions
from classes import Direccion
from data.data_direccion import DatosDireccion

class NegocioDireccion(Negocio):
    
    @classmethod
    def valida_direccion(cls, calle, altura, ciudad, provincia, pais):
        """
        Realiza las validaciones de negocio de una direccion.
        """
        #Conexión con el motor de BD.
        try:
            #Valida RN27
            if altura == "":
                raise custom_exceptions.ErrorDeNegocio(origen="neogocio_direccion.alta_pd()",
                                                        msj_adicional = "Error al validar una dirección. La altura no puede quedar vacía.")
            #Valida RN31
            elif not(isinstance(int(altura), int)):
                raise custom_exceptions.ErrorDeNegocio(origen="neogocio_direccion.alta_pd()",
                                                        msj_adicional = "Error al validar una dirección. La altura debe ser numérica.")
            #Valida RN26
            elif calle == "":
                raise custom_exceptions.ErrorDeNegocio(origen="neogocio_direccion.alta_pd()",
                                                        msj_adicional = "Error al validar una dirección. La calle no puede quedar vacía.")
            #Valida RN28
            elif ciudad == "":
                raise custom_exceptions.ErrorDeNegocio(origen="neogocio_direccion.alta_pd()",
                                                        msj_adicional = "Error al validar una dirección. La ciudad no puede quedar vacía.")
            #Valida RN29
            elif provincia == "":
                raise custom_exceptions.ErrorDeNegocio(origen="neogocio_direccion.alta_pd()",
                                                        msj_adicional = "Error al validar una dirección. La provincia no puede quedar vacía.")
            #Valida RN30
            elif pais == "":
                raise custom_exceptions.ErrorDeNegocio(origen="neogocio_direccion.alta_pd()",
                                                        msj_adicional = "Error al validar una dirección. El país no puede quedar vacío.")
            return True

        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeNegocio(origen="negocio_direccion.valida_direccion()",
                                                    msj=str(e),
                                                    msj_adicional="Error en la capa de Negocio validando las Reglas de Negocio de una direccion.")


    @classmethod
    def alta_direccion(cls, calle, altura, ciudad, provincia, pais, validar=False):
        """
        Añade una dirección a la BD.
        """
        #Conexión con el motor de BD.
        try:
            if validar:
                if NegocioDireccion.valida_direccion(calle, altura, ciudad, provincia, pais):
                    return DatosDireccion.alta_direccion(Direccion(None,calle, altura, ciudad, provincia, pais))
            else:
                return DatosDireccion.alta_direccion(Direccion(None,calle, altura, ciudad, provincia, pais))

        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeNegocio(origen="negocio_direccion.alta_direccion()",
                                                    msj=str(e),
                                                    msj_adicional="Error en la capa de Negocio dando de alta una direccion.")
    
    @classmethod
    def mod_direccion(cls, id_direccion, calle, altura, ciudad, provincia, pais, validar=False):
        """
        Modifica una dirección de la BD.
        """
        #Conexión con el motor de BD.
        try:
            if validar:
                if NegocioDireccion.valida_direccion(calle, altura, ciudad, provincia, pais):
                    return DatosDireccion.mod_direccion(Direccion(id_direccion,calle, altura, ciudad, provincia, pais))
            else:
                return DatosDireccion.mod_direccion(Direccion(id_direccion,calle, altura, ciudad, provincia, pais))

        except custom_exceptions.ErrorDeConexion as e:
            raise e
        except Exception as e:
            raise custom_exceptions.ErrorDeNegocio(origen="negocio_direccion.mod_direccion()",
                                                    msj=str(e),
                                                    msj_adicional="Error en la capa de Negocio modificando una direccion.")