from negocio.negocio import Negocio
from data.data_insumo import DatosInsumo
from data.data_cant_material import DatosCantMaterial
from data.data_articulo import DatosArticulo
from negocio.negocio_articulo import NegocioArticulo
from data.data_material import DatosMaterial
import custom_exceptions

class NegocioInsumo(Negocio):

    @classmethod
    def get_by_id(cls,id):
        """
        Obtiene un insumo de la BD a partir de su id.
        """
        try:
            insumo = DatosInsumo.get_by_id(id)
            return insumo

        except Exception as e:
            raise e


    @classmethod
    def get_by_id_array(cls,ids):
        """
        Obtiene insumos de la BD a partir de un arreglo de ids.
        """
        try:
            insumos = []
            for id in ids:
                insumos.append(DatosInsumo.get_by_id(id))
            return insumos

        except Exception as e:
            raise e
    
    
    @classmethod
    def get_all(cls,noFilter=False):
        """
        Obtiene todos los insumos de la BD.
        """
        try:
            insumos = DatosInsumo.get_all(noFilter)
            return insumos

        except Exception as e:
            raise e


    @classmethod
    def add(cls,nombre,unidad,costoMateriales,costoProduccion,otrosCostos,color,cants,desc):
        """
        Agrega un insumo a la BD
        """
        try:
            costoTotal = float(costoMateriales)+float(costoProduccion)+float(otrosCostos)
            idIns = DatosInsumo.add(nombre,unidad,costoMateriales,costoProduccion,otrosCostos,costoTotal,color,desc)
            for c in cants:
                DatosCantMaterial.addComponente(c["idMat"],idIns,c["cantidad"])
        except Exception as e:
            raise(e)


    @classmethod
    def update(cls,idIns,nombre,unidad,costoMateriales,costoProduccion,otrosCostos,color,mats):
        """
        Actualiza un insumo en la BD
        """
        try:
            materiales = cls.get_by_id(int(idIns)).materiales
            for m in mats:
                if m.idMaterial in [i.idMaterial for i in materiales]:
                    if m.cantidad == 0:
                        # delete
                        DatosCantMaterial.deleteComponente(m.idMaterial,idIns)
                        print("Delete mat: " + str(m.idMaterial))
                    elif m.cantidad != [i.cantidad for i in materiales if i.idMaterial == m.idMaterial ][0]:
                            # update
                            DatosCantMaterial.updateComponente(m.idMaterial,idIns,m.cantidad)
                            print("Update mat: " + str(m.idMaterial))
                elif m.cantidad > 0:
                        # add
                        DatosCantMaterial.addComponente(m.idMaterial,idIns,m.cantidad)
                        print("Add mat: " + str(m.idMaterial))




            costoTotal = float(costoMateriales)+float(costoProduccion)+float(otrosCostos)
            DatosInsumo.update(idIns,nombre,unidad,costoMateriales,costoProduccion,otrosCostos,costoTotal,color)

            arts_afectados = DatosArticulo.get_arts_afectados(idIns)
            for idArt in arts_afectados:
                print("corrigiendo valor de articulo: ",str(idArt))
                NegocioArticulo.calcular_costos(idArt)
            
        except Exception as e:
            raise(e)


    @classmethod
    def delete(cls,id):
        """
        Elimina un insumo de la BD a partir de su id
        """
        try:
            DatosInsumo.delete(id)
        except Exception as e:
            raise e

    
    @classmethod
    def get_nombres_by_idMat(cls,idMat):
        try:
            return DatosInsumo.get_nombres_by_idMat(idMat)
        except Exception as e:
            raise e

    @classmethod
    def update_desc(cls,idIns,desc):
        try:
            DatosInsumo.update_desc(idIns,desc)
        except Exception as e:
            raise e

    @classmethod
    def get_movimientos_stock(cls,id,stock):
        """
        Obtiene los movimientos de stock de un insumo durante el último año en base a su ID, recibiendo stock actual como parámetro.
        """
        try:
            return DatosInsumo.get_movimientos_stock(id,stock)[::-1]
        except Exception as e:
            raise custom_exceptions.ErrorDeNegocio(origen="negocio_material.get_movimientos_stock()",
                                                   msj=str(e),
                                                   msj_adicional="Error en la capa de Negocio obteniendo los movimientos de stock de la base de Datos")



    @classmethod
    def calcular_costos(cls,id):
        """
        Recalcula los costos de un insumo
        """
        #Obtiene el insumo
        ins = cls.get_by_id(id)

        #Calcula el nuevo costo de Materiales
        nuevoCostoMat = 0
        for mat in ins.materiales:
            nuevoCostoMat += DatosMaterial.get_costo_rec(mat.idMaterial)*mat.cantidad
        
        #Si el nuevo costo de insumos es distinto al anterior
        if nuevoCostoMat != ins.costoMateriales:
            ins.costoTotal -= ins.costoMateriales
            ins.costoTotal += nuevoCostoMat
            ins.costoMateriales = nuevoCostoMat

            #Se actualizan los costos de insumos y el total
            DatosInsumo.updateCostos(ins.id,ins.costoMateriales,ins.costoTotal)

            #Y se actualizan los arts afectados
            arts_afectados = DatosArticulo.get_arts_afectados(ins.id)
            for idArt in arts_afectados:
                print("corrigiendo valor de articulo: ",str(idArt))
                NegocioArticulo.calcular_costos(idArt)