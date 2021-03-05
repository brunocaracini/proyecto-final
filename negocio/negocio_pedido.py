from negocio.negocio import Negocio
from data.data_pedido import DatosPedido
from data.data_usuario import DatosUsuario
from data.data_punto_retiro import DatosPuntoRetiro
from data.data_cant_articulo import DatosCantArticulo
from negocio.negocio_articulo import NegocioArticulo
from negocio.negocio_usuario import NegocioUsuario
from datetime import datetime, timedelta
import custom_exceptions

class NegocioPedido(Negocio):
    @classmethod
    def add(cls,carrito,usuario,idPR,totalEP,totalARS):
        #verificaciones
        for art in carrito:
            NegocioArticulo.checkStock(art.idTipoArticulo,art.cantidad)
        NegocioUsuario.checkEP(usuario.id,totalEP)

        #Pedido
        puntoRetiro = DatosPuntoRetiro.get_by_id(idPR)
        fechaEnc = datetime.now()
        fechaRet = fechaEnc + timedelta(days=puntoRetiro.demoraFija)
        idPedido = DatosPedido.add(fechaEnc,fechaRet,totalEP,totalARS,idPR,usuario.id)

        
        #EcoPuntos
        nuevos_ep = NegocioUsuario.useEP(usuario.id,totalEP)

        #Nivel
        NegocioUsuario.update_nivel(usuario.id,nuevos_ep)
        
        #Articulos y Stock
        for art in carrito:
            NegocioArticulo.disminuirStock(art.idTipoArticulo,art.cantidad)
            DatosCantArticulo.addArticuloPedido(art.idTipoArticulo,idPedido,art.cantidad)

        return idPedido
            
    @classmethod
    def get_all(cls):
        try:
            return DatosPedido.get_all()
        except Exception as e:
            raise e

    @classmethod
    def get_by_idPR(cls,id):
        try:
            return DatosPedido.get_by_idPR(id)
        except Exception as e:
            raise e

    @classmethod
    def update_estado(cls,id,estado):
        try:
            DatosPedido.update_estado(id,estado)
        except Exception as e:
            raise e

    @classmethod
    def get_by_user_id(cls,uid, limit=False):
        try:
            return DatosPedido.get_by_user_id(uid, limit)
        except Exception as e:
            raise e