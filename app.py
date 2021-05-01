from flask import json
from flask.json import JSONEncoder
from classes import Horario, CantArticulo
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, redirect, session
from negocio.capa_negocio import *
import custom_exceptions
from classes import CantMaterial, CantInsumo
import traceback
from flask_session import Session 
from utils import Utils
from werkzeug.utils import secure_filename
from pathlib import Path
import mail
import os


#app
app = Flask(__name__)
app.secret_key = 'SecretKeyForSigningCookies'
app.config['SESSION_TYPE'] = 'filesystem'

#Session
app.secret_key = 'myscretkey'
Session(app)

@app.route('/perfil/usrimg',methods=["GET","POST"])
def upload_user_img():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            p = Path('static') / 'img' / 'users' / str(session["usuario"].id) / "profile"
            try:
                os.makedirs(p)
            except:
                pass
            filename = secure_filename(file.filename)
            dir = os.path.join(p, filename)
            file.save(dir)
            NegocioUsuario.update_img(session["usuario"].id,"/"+dir)
            session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
            session.modified = True
    return redirect(url_for('perfil'))


@app.route('/', methods = ['GET','POST'])
def start():
    return render_template('start-page.html')

@app.route('/main', methods = ['GET','POST'])
def main():
    if valida_session(): return redirect(url_for('login'))
    else:
        if session["usuario"].estado == "no-activo":
            tipos_doc = NegocioTipoDocumento.get_all()
            return render_template('datos-personales.html', tipos_doc=tipos_doc,user=session["usuario"])
        
        elif session["usuario"].estado == "no-verificado":
            return render_template('email-sent.html',email=session["usuario"].email) 
        else:
            nivel = NegocioNivel.get_nivel_id(session["usuario"].idNivel, True)
            if len(session["usuario"].pedidos) >= 5:
                pedidos = session["usuario"].pedidos[:5]
            else:
                pedidos = session["usuario"].pedidos
            puntosRetiro = NegocioPuntoRetiro.get_all()
            if len(session["usuario"].depositos) >= 5:
                depositos = session["usuario"].depositos[:5]
            else:
                depositos = session["usuario"].depositos
            puntosDep = NegocioPuntoDeposito.get_all_sin_filtro()
            materiales = NegocioMaterial.get_all()
            max_level = NegocioNivel.get_min_max_niveles()[1]
            tipoUsuario = NegocioTipoUsuario.get_by_id(session["usuario"].idTipoUsuario)
            return render_template('main.html',pedidos = pedidos,puntosRetiro=puntosRetiro,usuario=session["usuario"],
    nivel=nivel, depositos = depositos, puntosDep = puntosDep, materiales = materiales, max_level = max_level, tipoUsuario = tipoUsuario)


@app.route('/layout/datos-usuario')
def get_datos_usuario():
    if "carrito" in session.keys():
        carrito = session["carrito"]
    else:
        carrito = False
    return jsonify({"nombre":session["usuario"].nombre + " " + session["usuario"].apellido, "totalEP":session["usuario"].totalEcopuntos, "img":session["usuario"].img,"carrito": carrito,"modulos": NegocioTipoUsuario.get_by_id(session["usuario"].idTipoUsuario).modulosAcceso})

''' 
    -----------------
    Login
    -----------------
'''

@app.route('/login', methods = ['GET','POST'])
def login():
    try: 
        session["usuario"]
        return redirect(url_for('main'))
    except:
        return render_template('login.html')

@app.route('/login/auth/<email>/<password>', methods = ['GET','POST'])
def authentication(email, password):
    try:
        session["usuario"] = NegocioUsuario.login(email, password)
        session["light-mode"] = 'day'
        session.modified = True
        return jsonify({"login-state":True})
    except:
        return jsonify({"login-state":False})

@app.route('/logout/<val>', methods = ['GET','POST'])
def logout(val):
    if valida_session(): return redirect(url_for('login'))
    if val == "true":
        del session["usuario"]
        return redirect(url_for('login'))
    return render_template('login.html')

''' 
    -----------------
    Registro
    -----------------
'''

@app.route('/register', methods = ['GET','POST'])
def register():
    try:
        session["usuario"]
        return redirect(url_for('main'))
    except:
        return render_template('register.html')

@app.route('/register/alta-usuario/<email>/<passwd>', methods = ['GET','POST'])
def register_alta(email,passwd):
    try: 
        if not NegocioUsuario.check_email(email): 
            return jsonify("Email")
        elif not NegocioUsuario.check_password(passwd):
            return jsonify("Password")
        alta_result = NegocioUsuario.alta(email,passwd) 
        if not alta_result:
            return jsonify("Email")
        else:
            code = alta_result
        html_str = (render_template("mail.html"))
        mail.send_mail(email, passwd, html_str, code)
        return jsonify(True)
    except Exception as e:
        raise e
    return redirect(url_for('register'))

@app.route('/register/emails', methods = ['GET','POST'])
def register_all_emails():
    try: 
        return jsonify(NegocioUsuario.get_all_emails())

    except:
        return render_template('register.html')

@app.route('/datos-personales', methods = ['GET','POST'])
def datos_personales():
    try:
        if valida_session(): return redirect(url_for('login'))
        else:
            if session["usuario"].estado == "no-activo":
                tipos_doc = NegocioTipoDocumento.get_all()
                return render_template('datos-personales.html', tipos_doc=tipos_doc,user=session["usuario"])
            
            elif session["usuario"].estado == "habilitado":
                return redirect(url_for('main'))
            
            elif session["usuario"].estado == "no-verificado":
                return render_template('email-sent.html',email=session["usuario"].email) 
    except:
        return redirect(url_for('login'))

@app.route('/verificacion/<codigo>')
def verificacion(codigo):
    verificacion_res = NegocioUsuario.verificacion(codigo)
    if verificacion_res != False:
        session["usuario"] = NegocioUsuario.login(verificacion_res["email"],verificacion_res["password"])
        return redirect(url_for('datos_personales'))
    else:
        return redirect(url_for('start'))

@app.route('/datos-personales/activacion', methods = ['GET','POST'])
def activacion():
    if request.method == 'POST':
        email = request.form['email']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        ciudad = request.form['ciudad']
        calle = request.form['calle']
        altura = request.form['altura']
        pais = request.form['pais']
        provincia = request.form['provincia']
        documento = request.form['documento']
        tipo_doc = request.form['tipo_doc']
        if NegocioUsuario.activacion(email,nombre,apellido,calle,altura,ciudad,provincia,pais,documento,tipo_doc):
            session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
            return redirect(url_for('main'))
        else:
            return redirect(url_for('datos_personales'))

''' 
    ------------------
    Perfil de usuario
    ------------------
'''

@app.route('/perfil', methods = ['GET','POST'])
def perfil():
    if valida_session(): return redirect(url_for('login'))
    nivel = NegocioNivel.get_nivel_id(session["usuario"].idNivel)
    tipoDoc = NegocioTipoDocumento.get_by_id(session["usuario"].tipoDoc)
    password = '*' * len(session["usuario"].password)
    tipoUsuario = NegocioTipoUsuario.get_by_id(session["usuario"].idTipoUsuario)
    tiposDoc = NegocioTipoDocumento.get_all()
    emails = NegocioUsuario.get_all_emails(session["usuario"].id)
    return render_template('perfil.html',usuario = session["usuario"], nivel = nivel, tipoDoc = tipoDoc, 
    password = password, tipoUsuario = tipoUsuario, tiposDoc = tiposDoc, emails = emails)


@app.route('/perfil/actualizar-direccion', methods = ['GET','POST'])
def actualizar_direccion():
    if request.method == 'POST':
        try:
            calle = request.form['callePD']
            altura = request.form['alturaPD']
            ciudad = request.form['ciudadPD']
            provincia = request.form['provinciaPD']
            pais = request.form['paisPD']
            NegocioDireccion.mod_direccion(session["usuario"].direccion.id, calle,altura,ciudad,provincia,pais,True)
            session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
            session.modified = True
        except Exception as e:
            return error(e,"perfil")
    return redirect(url_for('perfil'))

@app.route('/perfil/actualizar-documento', methods = ['GET','POST'])
def actualizar_documento():
    if request.method == 'POST':
        try:
            nro = request.form['documentoInput']
            tipo = request.form['tipoDocSelect']
            NegocioUsuario.update_documento(nro,tipo,session["usuario"].id)
            session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
            session.modified = True
        except Exception as e:
            return error(e,"perfil")
    return redirect(url_for('perfil'))

@app.route('/perfil/actualizar-email', methods = ['GET','POST'])
def actualizar_email():
    if request.method == 'POST':
        try:
            email = request.form['email']
            NegocioUsuario.update_email(email,session["usuario"].id)
            session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
            session.modified = True
        except Exception as e:
            return error(e,"perfil")
    return redirect(url_for('perfil'))

@app.route('/perfil/actualizar-password', methods = ['GET','POST'])
def actualizar_password():
    if request.method == 'POST':
        try:
            psswd1 = request.form['newPassword1']
            psswd2 = request.form['newPassword2']
            NegocioUsuario.update_password(psswd1,psswd2,session["usuario"].id)
            session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
            session.modified = True
        except Exception as e:
            return error(e,"perfil")
    return redirect(url_for('perfil'))

@app.route('/perfil/get-list/<type>', methods = ['GET','POST'])
def perfil_listas(type):
    try:
        if type == 'emails':
            return jsonify(NegocioUsuario.get_all_emails(session["usuario"].id))
        if type == 'documentos':
            return jsonify(NegocioUsuario.get_all_documentos(session["usuario"].id))
        if type == 'documentos_no_filter':
            return jsonify(NegocioUsuario.get_all_documentos())
    except Exception as e:
        return error(e,"perfil")
    return render_template('login.html')

''' 
    -----------------
    Encontrar Puntos de Depósito y Puntos de Retiro
    -----------------
'''

@app.route('/encontrar-punto-deposito', methods = ['GET','POST'])
def encontrar_pd():
    puntos_dep = NegocioPuntoDeposito.get_all(filterInactivos=True)
    return render_template('encontrar-pd.html', puntos_dep = puntos_dep)

@app.route('/encontrar-punto-retiro', methods = ['GET','POST'])
def encontrar_pr():
    puntos_ret = NegocioPuntoRetiro.get_all(filterInactivos=True)
    return render_template('encontrar-pr.html', puntos_ret = puntos_ret)




''' 
    -------
    EcoTienda
    -------
'''

@app.route('/eco-tienda')
def eco_tienda():
    try:
        if valida_session(): return redirect(url_for('login'))
        articulos = NegocioArticulo.get_all()
        count = sum(art.stock > 0 for art in articulos)
        if count > 0:
            show_no_stock_letter = False 
        else:
            show_no_stock_letter = True
        print(show_no_stock_letter)
        nivel = NegocioNivel.get_nivel_id(session["usuario"].idNivel)
        valor_ep = NegocioEcoPuntos.get_valor_EP()
    except Exception as e:
        return error(e, "eco-tienda")
    return render_template('eco-tienda.html', articulos = articulos, usuario = session["usuario"], nivel = nivel, valor_ep = valor_ep, show_no_stock_letter = show_no_stock_letter)


@app.route('/eco-tienda/producto/<id>')
def product_page(id):
    try:
        id = int(id)
        producto = NegocioArticulo.get_by_id(id)

        if "carrito" in session.keys():
            carrito = session["carrito"]
        else:
            carrito = {}
            session["carrito"] = carrito
        nivel = NegocioNivel.get_nivel_id(session["usuario"].idNivel)
        recomendaciones = NegocioArticulo.get_recommendations(id,Utils.carrito_to_list(session["carrito"]))
        demora_prom = NegocioPuntoRetiro.get_demora_promedio()
        valor_ep = NegocioEcoPuntos.get_valor_EP()
        return render_template('product-page.html',producto=producto, recomendaciones=recomendaciones, nivel = nivel, usuario = session["usuario"], valor_ep = valor_ep, demora_prom  = demora_prom, carrito=Utils.carrito_to_list(session["carrito"]))
    except Exception as e:
        return error(e, "eco-tienda")


@app.route('/eco-tienda/producto/agregar', methods = ['GET','POST'])
def agregar_carrito():
    try:
        if request.method == "POST":
            cantidad = int(request.form['cantProd'])
            id = str(request.form['idProd'])

            if "carrito" not in session.keys():
                session["carrito"] = {}

            if id not in session["carrito"].keys():
                session["carrito"][str(id)] = cantidad
            
            else:
                session["carrito"][str(id)] = int(cantidad + session["carrito"][str(id)])

            return redirect(url_for("carrito"))
    except Exception as e:
        return error(e, "eco-tienda")

@app.route('/eco-tienda/producto/eliminar', methods = ['GET','POST'])
def eliminar_carrito():
    try:
        if request.method == "POST":
            id = str(request.form['idEliminacion'])

            if "carrito" not in session.keys():
                raise Exception("La variable de sesión carrito no existe")

            if id not in session["carrito"].keys():
                raise Exception("Se eliminó un articulo que no estaba en el carrito")
            
            else:
                del session["carrito"][str(id)]

            return redirect(url_for("carrito"))
    except Exception as e:
        return error(e, "eco-tienda")

@app.route('/eco-tienda/carrito')
def carrito():
    try:
        if "carrito" not in session.keys():
            session["carrito"] = {}
        articulos = NegocioArticulo.get_by_id_array(session["carrito"].keys())
        articulos_erroneos = []
        for i in range(len(articulos)):
            if articulos[i] == False:
                del session["carrito"][list(session["carrito"].keys())[i]]
                articulos_erroneos.append(i)
        for ae in articulos_erroneos:
            del articulos[ae]
        valor = 0
        for articulo in articulos:
              valor += int(session["carrito"][str(articulo.id)]) * articulo.valor
        valor_ep = NegocioEcoPuntos.get_valor_EP()
        demora_prom = NegocioPuntoRetiro.get_demora_promedio()
        nivel = NegocioNivel.get_nivel_id(session["usuario"].idNivel)
        usuario = session["usuario"]
        val_tot_ep = round(valor * valor_ep * (1-nivel.descuento/100))
        if val_tot_ep == 0: 
            val_tot_ep = 1
        step = 100/(val_tot_ep)
        puntos_retiro = NegocioPuntoRetiro.get_all(filterInactivos=True)
        carrito=Utils.carrito_to_list(session["carrito"])
        cant_ventas_mes = []
        for item in carrito:
            cant_ventas_mes.append(CantArticulo(NegocioArticulo.cant_vendidos_mes_actual(item.idTipoArticulo),item.idTipoArticulo))
        
        return render_template('carrito.html',carrito=carrito,articulos=articulos, cant_ventas_mes = cant_ventas_mes, 
                                valor_ep = valor_ep, demora_prom = demora_prom, valor = valor, nivel=nivel, 
                                usuario = usuario, val_tot_ep = val_tot_ep, step = step, puntos_retiro = puntos_retiro)
    except Exception as e:
        return error(e, "eco-tienda")


@app.route('/eco-tienda/checkout/confirmar/<idPR>/<totalEP>/<totalARS>')
def confirmar_checkout(idPR, totalEP, totalARS):
    dic = {"estado": "ok", "codigo": None,"demora": None}
    try:
        if "carrito" in session.keys() and session["carrito"] != {}:
            dic["codigo"] = NegocioPedido.add(Utils.carrito_to_list(session["carrito"]),session["usuario"],idPR,float(totalEP),float(totalARS))
            dic["demora"] = NegocioPuntoRetiro.get_by_id(int(idPR)).demoraFija
            session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
            session["carrito"] = {}
            session.modified = True
            return dic
        else:
            raise Exception("Carrito vacio")
    except custom_exceptions.ErrorDeNegocio as e:
        dic["estado"] = e.msj
        return dic
    except Exception as e:
        return dic






''' 
    -------
    EcoTips
    -------
'''
@app.route('/eco-tips')
def ecotips():
    return render_template('eco-tips.html',usuario = session["usuario"])





''' 
    -------
    Niveles
    -------
'''

@app.route('/gestion-niveles')
def gestion_niveles():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(3): return redirect(url_for("error_auth"))
    try:
        niveles = NegocioNivel.get_niveles()
        min_max_nivel = NegocioNivel.get_min_max_niveles()
        maxEP = NegocioNivel.get_max_ecoPuntos()
        maxDescuento = NegocioNivel.get_max_descuento()
    except Exception as e:
        return error(e, "gestion_niveles")
    return render_template('gestion-niveles.html', niveles = niveles, min_nivel = min_max_nivel[0],max_level = min_max_nivel[1], maxEP = maxEP, maxDescuento = maxDescuento, usuario=session["usuario"])

@app.route('/gestion-niveles/alta', methods = ['GET','POST'])
def alta_nivel():
    if request.method == 'POST':
        try:
            numeroNivel = request.form['numeroNivel']
            descuento = request.form['descuento']
            minEcoPuntos = request.form['minEcoPuntos']
            maxEcoPuntos = request.form['maxEcoPuntos']
            NegocioNivel.alta_nivel(numeroNivel, descuento, minEcoPuntos, maxEcoPuntos)
            session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
            session.modified = True
        except Exception as e:
            return error(e,"gestion_niveles")
    return redirect(url_for('gestion_niveles'))

@app.route('/gestion-niveles/mod/<id>/<desc>/<min>/<max>')
def mod_nivel(id, desc, min, max):
    try:
        numero = int(id)
        desc = float(desc)
        minEP = float(min)
        maxEP = float(max)
        NegocioNivel.modifica_nivel(numero,desc,minEP,maxEP)
        print(session["usuario"].idNivel)
        session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
        session.modified = True
        print(session["usuario"].idNivel)
    except Exception as e:
        return error(e,"gestion_niveles")
    return redirect(url_for('gestion_niveles'))
  
@app.route('/gestion-niveles/baja/<int:id>')
def baja_nivel(id):
    try:
        id = int(id)
        NegocioNivel.baja_nivel(id)
        session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
        session.modified = True
    except Exception as e:
        return error(e,"gestion_niveles")
    return redirect(url_for('gestion_niveles'))

@app.route('/gestion-niveles/modificacion/<int:id>')
def mod_nivel_request(id):
    try:
        id = int(id)
        desc_ant_post = NegocioNivel.getDescuentosAntPost(id)
        return jsonify(desc_ant_post)
    except Exception as e:
        return error(e,"gestion_niveles")

@app.route('/info-niveles')
def info_niveles():
    try:
        if valida_session(): return redirect(url_for('login'))
        niveles = NegocioNivel.get_niveles()
    except Exception as e:
        return error(e, "info_niveles")
    return render_template('info-niveles.html', niveles = niveles)

@app.route('/gestion-niveles/get-name/<int:id>')
def get_nivel_name_request(id):
    try:
        id = int(id)
        return jsonify(NegocioNivel.get_nivel_id(id).nombre)
    except Exception as e:
        return error(e,"gestion_niveles")

''' 
    -----------------
    Entidades Destino
    -----------------
'''

@app.route('/gestion-ed', methods = ['GET','POST'])
def gestion_ed():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(6): return redirect(url_for("error_auth"))
    try:
        entidades = NegocioEntidadDestino.get_all()
    except Exception as e:
        return error(e,"gestion_ed")
    return render_template('gestion-entidades-destino.html', entidades = entidades, usuario=session["usuario"])


@app.route('/gestion-ed/editdesc',methods=["POST","GET"])
def edit_desc_ed():
    if request.method == "POST":
        idED = int(request.form["idED"])
        desc = request.form["desc"]
        NegocioEntidadDestino.update_desc(idED,desc)
        return redirect(url_for('gestion_ed'))


@app.route('/gestion-ed/articulos', methods = ['GET','POST'])
def get_articulos():
    try:
        articulos = NegocioArticulo.get_all()
        arts_json = [{"nombre":         a.nombre,
                      "unidadmedida":   a.unidadMedida,
                      "id":             a.id,
                      "stock":          a.stock,
                      "valor":          a.valor.valor}
                      for a in articulos]
        return jsonify(arts_json)
    except Exception as e:
        return error(e,"gestion_ed")

@app.route('/gestion-ed/salidas/<id>')
def devolver_salidas(id):
    try:
        e = NegocioEntidadDestino.get_one(id)
        a = NegocioArticulo.get_by_id_array([i.articulos.idTipoArticulo for i in e.salidas])
        salidas_present =  [{"nombre":         s[1].nombre,
                            "cantidad":        s[0].articulos.cantidad, 
                            "unidadmedida":    s[1].unidadMedida,
                            "fecha":           s[0].fecha.strftime("%d/%m/%Y")}
                            for s in list(zip(e.salidas,a))]
        return jsonify(salidas_present)
    except Exception as e:
        return error(e,"gestion_ed")   


@app.route('/gestion-ed/alta', methods = ['GET','POST'])
def alta_entidad_destino():
    if request.method == 'POST':
        nombre = request.form['nombre']
        try:
            NegocioEntidadDestino.add(nombre)
        except Exception as e:
            return error(e,"gestion_ed")
        return redirect(url_for('gestion_ed'))


@app.route('/gestion-ed/edit', methods = ['GET','POST'])
def edit_entidad_destino():
    if request.method == 'POST':
        nombre = request.form['nombre']
        idEnt = request.form['id']
        try:
            NegocioEntidadDestino.update(idEnt,nombre)
        except Exception as e:
            return error(e,"gestion_ed")
        return redirect(url_for('gestion_ed'))


@app.route('/gestion-ed/baja/<id>')
def baja_entidad_destino(id):
    id = int(id)
    try:
        NegocioEntidadDestino.delete(id)
    except Exception as e:
        return error(e,"gestion_ed")
    return redirect(url_for('gestion_ed'))

''' 
    -----------------
    Error Page
    -----------------
'''


@app.route('/error', methods = ['GET','POST'])
def error(err="", url_redirect="/main"):
    if err=="":
        err = "Ha habido un error inesperado. Por favor vuelva a intentarlo. \nSi el problema persiste, contacte a un administrador."
    else:
        ad = traceback.format_tb(err.__traceback__)
    return render_template('error.html', err = err, aditional = ad,url_redirect=url_redirect)


''' 
    ---------------------------
    Puntos de Deposito
    ---------------------------
'''

@app.route('/elegir-tipo-punto', methods = ['GET','POST'])
def selection():
    if valida_session(): return redirect(url_for('login'))
    if not (valida_permiso(7) or valida_permiso(15)): return redirect(url_for("error_auth"))
    return render_template('elegir-tipo-punto.html', usuario = session["usuario"])


@app.route('/gestion-puntos-deposito', methods = ['GET','POST'])
def gestion_pd():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(15): return redirect(url_for("error_auth"))
    try:
        materiales = NegocioMaterial.get_all()
        puntos_deposito = NegocioPuntoDeposito.get_all()
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    except Exception as e:
        return error(e,"gestion_pd") 
    return render_template('gestion-puntos-deposito.html', puntos_deposito = puntos_deposito, dias = dias, materiales = materiales, usuario = session["usuario"])

@app.route('/gestion-puntos-deposito/horarios/<int:id>')
def horarios_pd(id):
    try:
        id = int(id)
        horarios = NegocioPuntoDeposito.get_horarios_id(id)
        return jsonify(horarios)
    except Exception as e:
        return error(e,"gestion_pd")
    
@app.route('/gestion-puntos-deposito/materiales/<int:id>')
def materiales_pd(id):
    try:
        id = int(id)
        materiales = NegocioPuntoDeposito.get_materialesPd_by_id(id)
        return jsonify(materiales)
    except Exception as e:
        return error(e,"gestion_pd")

@app.route('/gestion-puntos-deposito/nombres-pd/')
def nombres_pd():
    try:
        nombres = NegocioPuntoDeposito.get_all_names()
        return jsonify(nombres)
    except Exception as e:
        return error(e,"gestion_pd")


@app.route('/gestion-puntos-deposito/alta', methods = ['GET','POST'])
def alta_pd():
    
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    horarios = []
    
    if request.method == 'POST':
        try:
            nombre = request.form['nombrePD']
            estado = request.form['switch-value']
            calle = request.form['callePD']
            altura = request.form['alturaPD']
            ciudad = request.form['ciudadPD']
            provincia = request.form['provinciaPD']
            pais = request.form['paisPD']
            for dia in dias:
                horaDesde = request.form[dia + '-horaDesde']
                horaHasta = request.form[dia + '-horaHasta']
                horarios.append([horaDesde,horaHasta, dia])
            materiales = request.form['materiales-altaPD']
            
            NegocioPuntoDeposito.alta_pd(nombre, estado, calle, altura, ciudad, provincia, pais, horarios, materiales)
        except Exception as e:
            return error(e,"gestion-puntos-deposito")
    return redirect(url_for('gestion_pd'))

@app.route('/gestion-puntos-deposito/modificacion', methods = ['GET','POST'])
def mod_pd():
    
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    horarios = []
    
    if request.method == 'POST':
        nombre = request.form['nombrePDMod']
        nombre_ant = request.form['nombrePDModAnt']
        estado = request.form['switch-value-mod']
        calle = request.form['callePDMod']
        altura = request.form['alturaPDMod']
        ciudad = request.form['ciudadPDMod']
        provincia = request.form['provinciaPDMod']
        pais = request.form['paisPDMod']
        id_direccion = request.form['idDireccionPD']
        id_punto = request.form['idPDMod']
        for dia in dias:
            horaDesde = request.form[dia + '-horaDesde-mod']
            horaHasta = request.form[dia + '-horaHasta-mod']
            horarios.append([horaDesde,horaHasta, dia])
        materiales = request.form['materiales-modPD']
        NegocioPuntoDeposito.mod_pd(nombre, estado, calle, altura, ciudad, provincia, pais, horarios,materiales,id_direccion, id_punto, nombre_ant)
        
    return redirect(url_for('gestion_pd'))

@app.route('/gestion-puntos-deposito/baja', methods = ['GET','POST'])
def baja_pd():
    
    if request.method == 'POST':
        id = request.form['idPuntoBaja']
        print(id)
        NegocioPuntoDeposito.baja_pd(id)
        
    return redirect(url_for('gestion_pd'))

''' 
    -----------------
    Puntos de Retiro
    -----------------
'''
@app.route('/gestion-puntos-retiro', methods = ['GET','POST'])
def gestion_pr():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(7): return redirect(url_for("error_auth"))
    try:
        puntos_retiro = NegocioPuntoRetiro.get_all()
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    except Exception as e:
        return error(e,"gestion_pr") 
    return render_template('gestion-puntos-retiro.html', puntos_retiro = puntos_retiro, dias = dias, usuario = session["usuario"])

@app.route('/gestion-puntos-retiro/horarios/<int:id>')
def horarios_pr(id):
    try:
        id = int(id)
        horarios = NegocioPuntoRetiro.get_horarios_id(id)
        return jsonify(horarios)
    except Exception as e:
        return error(e,"gestion_pr")

@app.route('/gestion-puntos-retiro/pedidos/<int:id>')
def pedidos_pr(id):
    try:
        id = int(id)
        pedidos = NegocioPedido.get_by_idPR(id,10)
        pedidos_ = []
        for pedido in pedidos:
            ped = {"id":pedido.id,"estado":pedido.estado,"fechaEnc":pedido.fechaEncargo,"fechaRet":pedido.fechaRetiro,"totalARS":pedido.totalARS,"totalEP":pedido.totalEP}
            pedidos_.append(ped)
        return jsonify(pedidos_)
    except Exception as e:
        return error(e,"gestion_pr")

@app.route('/gestion-puntos-retiro/nombres-pr')
def nombres_pr():
    try:
        nombres = NegocioPuntoRetiro.get_all_names()
        demora_prom = NegocioPuntoRetiro.get_demora_promedio()
        return jsonify([nombres,demora_prom])
    except Exception as e:
        return error(e,"gestion_pr")

@app.route('/gestion-puntos-retiro/alta', methods = ['GET','POST'])
def alta_pr():
    
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    horarios = []
    
    if request.method == 'POST':
        try:
            nombre = request.form['nombrePD']
            estado = request.form['switch-value']
            demora = request.form['demoraPR']
            calle = request.form['callePD']
            altura = request.form['alturaPD']
            ciudad = request.form['ciudadPD']
            provincia = request.form['provinciaPD']
            pais = request.form['paisPD']
            for dia in dias:
                horaDesde = request.form[dia + '-horaDesde']
                horaHasta = request.form[dia + '-horaHasta']
                horarios.append([horaDesde,horaHasta, dia])
            
            NegocioPuntoRetiro.alta_pr(nombre, estado, calle, altura, ciudad, provincia, pais, horarios, demora)
        except Exception as e:
            return error(e,"gestion-puntos-retiro")
    return redirect(url_for('gestion_pr'))

@app.route('/gestion-puntos-retiro/modificacion', methods = ['GET','POST'])
def mod_pr():
    
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    horarios = []
    
    if request.method == 'POST':
        nombre = request.form['nombrePDMod']
        nombre_ant = request.form['nombrePDModAnt']
        demora = request.form['demoraPRMod']
        estado = request.form['switch-value-mod']
        calle = request.form['callePDMod']
        altura = request.form['alturaPDMod']
        ciudad = request.form['ciudadPDMod']
        provincia = request.form['provinciaPDMod']
        pais = request.form['paisPDMod']
        id_direccion = request.form['idDireccionPD']
        id_punto = request.form['idPDMod']
        for dia in dias:
            horaDesde = request.form[dia + '-horaDesde-mod']
            horaHasta = request.form[dia + '-horaHasta-mod']
            horarios.append([horaDesde,horaHasta, dia])
        NegocioPuntoRetiro.mod_pr(nombre, estado, calle, altura, ciudad, provincia, pais, horarios,demora,id_direccion, id_punto, nombre_ant)
        
    return redirect(url_for('gestion_pr'))

@app.route('/gestion-puntos-retiro/baja', methods = ['GET','POST'])
def baja_pr():
    
    if request.method == 'POST':
        id = request.form['idPuntoBaja']
        NegocioPuntoRetiro.baja_pr(id)
        
    return redirect(url_for('gestion_pr'))


''' 
    -----------------
    Articulos
    -----------------
'''

@app.route('/articulos', methods = ['GET','POST'])
def gestion_articulos():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(2): return redirect(url_for("error_auth"))
    try:
        articulos = NegocioArticulo.get_all()
        insumos = NegocioInsumo.get_all()
        return render_template('gestion-articulos.html',articulos=articulos, usuario = session["usuario"],insumos=insumos)
    except Exception as e:
        return error(e,"articulos")

@app.route('/articulos/alta', methods = ['GET','POST'])
def alta_articulo():
    if request.method == 'POST':
        nombre =                request.form['nombre']
        unidad =                request.form['unidad']
        ventaUsuario = None
        try: 
            request.form['ventaUsuario']
            ventaUsuario = 1
        except:
            ventaUsuario = 0
        costoInsumos =          request.form['costoInsumos']
        costoProduccion =       request.form['costoProduccion']
        otrosCostos =           request.form['otrosCostos']
        costoObtencionAlt =     request.form['costoObtencionAlt']
        margen =                request.form['margen']
        valor =                 request.form['valor']
        desc =                  request.form['desc']


        #INSUMOS
        cants = []
        for key in request.form.keys():
            if "id-" in key:
                id = request.form[key]
                cant = float(request.form["cantidad-"+id])
                if cant > 0:
                    cants.append({"idIns":id,"cantidad":cant})

        try:
            idNuevoArt = NegocioArticulo.add(nombre,unidad,ventaUsuario,costoInsumos,costoProduccion,otrosCostos,costoObtencionAlt,margen,valor,cants,desc)
        
            #IMAGEN
            imagen = ""
            file = request.files['file']
            if file.filename != '' and file:
                p = Path('static') / 'img' / 'articulos' / str(idNuevoArt)
                try:
                    os.makedirs(p)
                except:
                    pass
                filename = secure_filename(file.filename)
                dir = os.path.join(p, filename)
                file.save(dir)
                imagen = dir
            if imagen != "":
                NegocioArticulo.update_img(idNuevoArt,"/"+imagen)

        except Exception as e:
            return error(e,"articulos")
        return redirect(url_for('gestion_articulos'))


@app.route('/articulos/edit', methods = ['GET','POST'])
def edit_articulo():
    if request.method == 'POST':
        idArt =                 request.form['idArticulo']
        nombre =                request.form['nombre']
        unidad =                request.form['unidad']
        ventaUsuario = None
        #Aparentemente cuando un input tipo checkbox está "no chequeado"
        #no se manda en el form, asi que chequeo si puedo leerlo, para
        #ver si esta activado
        try: 
            request.form['ventaUsuario']
            ventaUsuario = 1
        except:
            ventaUsuario = 0
        costoInsumos =          request.form['costoInsumos']
        costoProduccion =       request.form['costoProduccion']
        otrosCostos =           request.form['otrosCostos']
        costoObtencionAlt =     request.form['costoObtencionAlt']
        margen =                request.form['margen']
        valor =                 request.form['valor']
        cants = []
        for key in request.form.keys():
            if "id-" in key:
                id = request.form[key]
                cant = float(request.form["cantidad-"+id])
                cants.append(CantInsumo(cant,int(id)))

        try:
            NegocioArticulo.update(idArt,nombre,unidad,ventaUsuario,costoInsumos,costoProduccion,otrosCostos,costoObtencionAlt,margen,valor,cants)
            #IMAGEN
            imagen = ""
            file = request.files['file']
            if file.filename != '' and file:
                p = Path('static') / 'img' / 'articulos' / str(idArt)
                try:
                    os.makedirs(p)
                except:
                    pass
                filename = secure_filename(file.filename)
                dir = os.path.join(p, filename)
                file.save(dir)
                imagen = dir
            if imagen != "":
                NegocioArticulo.update_img(idArt,"/"+imagen)
        except Exception as e:
            return error(e,"articulos")
        return redirect(url_for('gestion_articulos'))


@app.route('/articulos/baja/<id>')
def baja_articulo(id):
    id = int(id)
    try:
        NegocioArticulo.delete(id)
    except Exception as e:
        return error(e,"articulos")
    return redirect(url_for('gestion_articulos'))

@app.route('/articulos/editdesc',methods=["POST","GET"])
def edit_desc_articulo():
    if request.method == "POST":
        idArt = int(request.form["idArt"])
        desc = request.form["desc"]
        NegocioArticulo.update_desc(idArt,desc)
        return redirect(url_for('gestion_articulos'))


@app.route('/articulos/insumos/<ids>')
def get_insumos(ids):
    # esto es probablemente lo mas inseguro que se puede hacer en un sistema web
    # basicamente el user podria poner codigo python en el url y hacer que lo corra el server
    # aca lo uso para convertir un string tipo "[1,2,3]" a un arreglo [1,2,3]
    #TODO: CAMBIAR ESTA LINEA:
    ids = eval("["+ids+"]")
    print(ids)
    if ids == [-1]:
        return jsonify(False)
    try:
        insumos = NegocioInsumo.get_by_id_array(ids)
        insumos_dic =     [{"nombre":          i.nombre,
                            "unidadmedida":    i.unidadMedida,
                            "color":           i.color}
                            for i in insumos]
        return jsonify(insumos_dic)
    except Exception as e:
        return error(e,"insumos")
    return redirect(url_for('gestion_articulos'))

@app.route('/articulos/get-stock/<id>', methods = ['GET','POST'])
def get_stock_art(id):
    try:
        art = NegocioArticulo.get_by_id(id)
        return jsonify(art.stock)
    except:
        return jsonify(False)


''' 
    -----------------
    Insumos
    -----------------
'''

@app.route('/insumos', methods = ['GET','POST'])
def gestion_insumos():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(1): return redirect(url_for("error_auth"))
    try:
        insumos = NegocioInsumo.get_all()
        materiales = NegocioMaterial.get_all()
        return render_template('gestion-insumos.html',insumos=insumos,materiales=materiales, usuario = session["usuario"])
    except Exception as e:
        return error(e,"insumos")


@app.route('/insumos/alta', methods = ['GET','POST'])
def alta_insumo():
    if request.method == 'POST':
        nombre =                request.form['nombre']
        unidad =                request.form['unidad']
        costoMateriales =       request.form['costoMateriales']
        costoProduccion =       request.form['costoProduccion']
        otrosCostos =           request.form['otrosCostos']
        color =                 request.form['color']
        desc =                  request.form['desc']
        cants = []
        for key in request.form.keys():
            if "id-" in key:
                id = request.form[key]
                cant = float(request.form["cantidad-"+id])
                if cant > 0:
                    cants.append({"idMat":id,"cantidad":cant})
        try:
            NegocioInsumo.add(nombre,unidad,costoMateriales,costoProduccion,otrosCostos,color,cants,desc)
        except Exception as e:
            return error(e,"insumos")
        return redirect(url_for('gestion_insumos'))


@app.route('/insumos/edit', methods = ['GET','POST'])
def edit_insumo():
    if request.method == 'POST':
        idIns =                 request.form["id"]
        nombre =                request.form['nombre']
        unidad =                request.form['unidad']
        costoMateriales =       request.form['costoMateriales']
        costoProduccion =       request.form['costoProduccion']
        otrosCostos =           request.form['otrosCostos']
        color =                 request.form['color']
        cants = []
        for key in request.form.keys():
            if "id-" in key:
                id = request.form[key]
                cant = float(request.form["cantidad-"+id])
                cants.append(CantMaterial(cant,int(id)))

        try:
            NegocioInsumo.update(idIns,nombre,unidad,costoMateriales,costoProduccion,otrosCostos,color,cants)
        except Exception as e:
            return error(e,"insumos")
        return redirect(url_for('gestion_insumos'))


@app.route('/insumos/editdesc',methods=["POST","GET"])
def edit_desc_insumo():
    if request.method == "POST":
        idIns = int(request.form["idIns"])
        desc = request.form["desc"]
        NegocioInsumo.update_desc(idIns,desc)
        return redirect(url_for('gestion_insumos'))




@app.route('/insumos/baja/<id>')
def baja_insumo(id):
    id = int(id)
    try:
        NegocioInsumo.delete(id)
    except Exception as e:
        return error(e,"insumos")
    return redirect(url_for('gestion_insumos'))



@app.route('/insumos/materiales/<ids>')
def get_materiales(ids):
    # esto es probablemente lo mas inseguro que se puede hacer en un sistema web
    # basicamente el user podria poner codigo python en el url y hacer que lo corra el server
    # aca lo uso para convertir un string tipo "[1,2,3]" a un arreglo [1,2,3]
    #TODO: CAMBIAR ESTA LINEA:
    ids = eval("["+ids+"]")
    print(ids)
    if ids == [-1]:
        return jsonify(False)
    try:
        materiales = NegocioMaterial.get_by_id_array(ids)
        materiales_dic =  [{"nombre":          m.nombre,
                            "unidadmedida":    m.unidadMedida,
                            "color":           m.color}
                            for m in materiales]
        return jsonify(materiales_dic)
    except Exception as e:
        return error(e,"materiales")
    return redirect(url_for('gestion_materiales'))


@app.route('/insumos/val_delete/<idIns>')
def get_recetas_articulos(idIns):
    try:
        arr = NegocioArticulo.get_nombres_by_idIns(idIns)
        print(arr)
        return jsonify(arr)
    except Exception as e:
        return error(e,"insumos")

  
''' 
    -----------------
    Materiales
    -----------------
'''

@app.route('/materiales', methods = ['GET','POST'])
def gestion_materiales():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(16): return redirect(url_for("error_auth"))
    try:
        materiales = NegocioMaterial.get_all()
        return render_template('gestion-materiales.html',materiales=materiales, usuario = session["usuario"])
    except Exception as e:
        return error(e,"materiales")


@app.route('/materiales/alta', methods = ['GET','POST'])
def alta_material():
    if request.method == 'POST':
        nombre =                request.form['nombre']
        unidad =                request.form['unidad']
        costoRecoleccion =      request.form['costoRecoleccion']
        color =                 request.form['color']
        estado =                request.form['estado']
        desc =                  request.form['desc']
        try:
            NegocioMaterial.add(nombre,unidad,costoRecoleccion,color,estado,desc)
        except Exception as e:
            return error(e,"materiales")
        return redirect(url_for('gestion_materiales'))


@app.route('/materiales/edit', methods = ['GET','POST'])
def edit_material():
    if request.method == 'POST':
        idMat =                 request.form["id"]
        nombre =                request.form['nombre']
        unidad =                request.form['unidad']
        costoRecoleccion =      request.form['costoRecoleccion']
        color =                 request.form['color']
        estado =                request.form['estado']
        try:
            NegocioMaterial.update(idMat,nombre,unidad,costoRecoleccion,color,estado)
        except Exception as e:
            return error(e,"materiales")
        return redirect(url_for('gestion_materiales'))


@app.route('/materiales/baja/<id>')
def baja_material(id):
    id = int(id)
    try:
        NegocioMaterial.delete(id)
    except Exception as e:
        return error(e,"materiales")
    return redirect(url_for('gestion_materiales'))


@app.route('/materiales/val_delete/<idMat>')
def get_recetas_insumos(idMat):
    try:
        arr = NegocioInsumo.get_nombres_by_idMat(idMat)
        print(arr)
        return jsonify(arr)
    except Exception as e:
        return error(e,"materiales")


@app.route('/materiales/editdesc',methods=["POST","GET"])
def edit_desc_material():
    if request.method == "POST":
        idMat = int(request.form["idMat"])
        desc = request.form["desc"]
        NegocioMaterial.update_desc(idMat,desc)
        return redirect(url_for('gestion_materiales'))


'''
    -----------------
    Gestion de Pedidos
    -----------------
'''

@app.route('/elegir-PR')
def elegirPR():
    if valida_session(): return redirect(url_for('login'))
    if not (valida_permiso(8) or valida_permiso(12)): return redirect(url_for("error_auth"))
    try:
        puntosRetiro = NegocioPuntoRetiro.get_all()
        return render_template('elegir-PR.html',puntosRetiro = puntosRetiro, usuario=session["usuario"])
    except Exception as e:
        return error(e,"pedidos")

@app.route('/gestion-pedidos/deposito')
def deposito():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(8): return redirect(url_for("error_auth"))
    try:
        pedidos = NegocioPedido.get_all()
        puntosRetiro = NegocioPuntoRetiro.get_all(True)
        return render_template('deposito.html',pedidos = pedidos,puntosRetiro=puntosRetiro, usuario=session["usuario"])
    except Exception as e:
        return error(e,"pedidos")

@app.route('/gestion-pedidos/pr/<id>')
def pedidosPR(id):
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(12): return redirect(url_for("error_auth"))
    try:
        pedidos = NegocioPedido.get_by_idPR(int(id))
        puntoRetiro = NegocioPuntoRetiro.get_by_id(int(id))
        return render_template('pedidosPR.html',pedidos = pedidos,puntoRetiro=puntoRetiro, usuario=session["usuario"])
    except Exception as e:
        return error(e,"pedidos")

@app.route('/gestion-pedidos/usuario')
def pedidosUser():
    try:
        pedidos = NegocioPedido.get_by_user_id(session["usuario"].id)
        orden = {"listo":0,"preparado":1,"pendiente":2,"retirado":3,"cancelado":4,"devuelto":5}
        pedidos_ordenados = sorted(pedidos, key=lambda x: orden[x.estado])
        puntosRetiro = NegocioPuntoRetiro.get_all(True)
        return render_template('pedidosUser.html',pedidos = pedidos_ordenados,puntosRetiro=puntosRetiro, idPed =0,usuario=session["usuario"])
    except Exception as e:
        return error(e,"pedidos")


@app.route('/gestion-pedidos/usuario/<id>')
def pedidosUser_articulos(id):
    try:
        id=int(id)
        pedidos = NegocioPedido.get_by_user_id(session["usuario"].id)
        orden = {"listo":0,"preparado":1,"pendiente":2,"retirado":3,"cancelado":4,"devuelto":5}
        pedidos_ordenados = sorted(pedidos, key=lambda x: orden[x.estado])
        puntosRetiro = NegocioPuntoRetiro.get_all(True)
        return render_template('pedidosUser.html',pedidos = pedidos_ordenados,puntosRetiro=puntosRetiro, idPed=id,usuario=session["usuario"])
    except Exception as e:
        return error(e,"pedidos")


@app.route('/pedidos/articulos/<ids>')
def get_articulos_pedido(ids):
    # esto es probablemente lo mas inseguro que se puede hacer en un sistema web
    # basicamente el user podria poner codigo python en el url y hacer que lo corra el server
    # aca lo uso para convertir un string tipo "[1,2,3]" a un arreglo [1,2,3]
    #TODO: CAMBIAR ESTA LINEA:
    try:
        ids = eval("["+ids+"]")
        print(ids)
        articulos = NegocioArticulo.get_by_id_array(ids)
        articulos_dic =  [{"nombre":          a.nombre,
                            "unidadmedida":    a.unidadMedida}
                            for a in articulos]
        return jsonify(articulos_dic)
    except Exception as e:
        return error(e,"pedidos")


@app.route('/gestion-pedidos/actualizar', methods = ['GET','POST'])
def update_estado_pedido():
    try:
        if request.method == 'POST':
            id = int(request.form["idInput"])
            estado = request.form["estadoInput"]
            pr = int(request.form["idPRInput"])
            NegocioPedido.update_estado(id,estado)
            session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
            session.modified = True
            if pr == 0:
                return redirect(url_for("deposito"))
            else:
                return redirect("/gestion-pedidos/pr/"+str(pr))
    except Exception as e:
        return error(e,"pedidos")

@app.route('/pedidos/info/<id>')
def pedidos_info(id):
    try:
        res = NegocioPedido.get_one(id,True)
        ped = res[0]
        user = res[1]
        pr = NegocioPuntoRetiro.get_by_id(ped.idPuntoRetiro)
        td = NegocioTipoDocumento.get_by_id(user.tipoDoc)
        pedido = {"id":ped.id,"totalEP":ped.totalEP,"totalARS":ped.totalARS,"estado":ped.estado,"fecha_enc":ped.fechaEncargo,"fecha_ret":ped.fechaRetiro}
        usuario = {"id":user.id,"nombre":user.nombre,"apellido":user.apellido,"tipoDoc":td.nombre,"nroDoc":user.nroDoc,"email":user.email}
        punto_retiro = {"id":pr.id,"nombre":pr.nombre,"calle":pr.direccion.calle,"altura":pr.direccion.altura,"ciudad":pr.direccion.ciudad,"provincia":pr.direccion.provincia,"pais":pr.direccion.pais}
        return jsonify([pedido, usuario, punto_retiro])
    except Exception as e:
        return error(e,"pedidos")







'''
    -----------------
    Gestion de Depósitos
    -----------------
'''

@app.route('/elegir-PD')
def elegirPD():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(9): return redirect(url_for("error_auth"))
    try:
        puntosDeposito = NegocioPuntoDeposito.get_all()
        return render_template('elegir-PD.html',puntosDeposito = puntosDeposito, usuario=session["usuario"])
    except Exception as e:
        return error(e,"depositos")

@app.route('/gestion-depositos/admin')
def allDepositos():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(9): return redirect(url_for("error_auth"))
    try:
        materiales = NegocioMaterial.get_all()
        depositos = NegocioDeposito.get_all()
        return render_template('depositosAdmin.html',materiales=materiales,depositos = depositos, usuario=session["usuario"])
    except Exception as e:
        return error(e,"pedidoss")

@app.route('/gestion-depositos/pd/<id>')
def pedidosPD(id):
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(9): return redirect(url_for("error_auth"))
    try:
        materiales = NegocioMaterial.get_all()
        depositos = NegocioDeposito.get_by_id_PD(int(id))
        puntoDeposito = NegocioPuntoDeposito.get_by_id(int(id))
        return render_template('depositosPD.html',materiales=materiales,depositos = depositos,puntoDeposito=puntoDeposito, usuario=session["usuario"])
    except Exception as e:
        return error(e,"depositos")

@app.route('/gestion-depositos/materiales/<ids>')
def get_materiales_deposito(ids):
    # esto es probablemente lo mas inseguro que se puede hacer en un sistema web
    # basicamente el user podria poner codigo python en el url y hacer que lo corra el server
    # aca lo uso para convertir un string tipo "[1,2,3]" a un arreglo [1,2,3]
    #TODO: CAMBIAR ESTA LINEA:
    try:
        ids = eval("["+ids+"]")
        print(ids)
        materiales = NegocioMaterial.get_by_id_array(ids)
        mat_dic =  [{"nombre":          m.nombre,
                     "unidadmedida":    m.unidadMedida}
                     for m in materiales]
        return jsonify(mat_dic)
    except Exception as e:
        return error(e,"depositos")


@app.route('/gestion-depositos/actualizar', methods = ['GET','POST'])
def update_estado_deposito():
    try:
        if request.method == 'POST':
            id = int(request.form["idDep"])
            estado = request.form["estado"]
            pd = int(request.form["idPD"])

            if estado == "cancelado":
                NegocioDeposito.cancelar(id)
                NegocioNivel.actualiza_nivel_all()
                session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
                session.modified = True
                

            elif estado == "acreditado":
                uid = int(request.form["idUser"])
                NegocioDeposito.acreditar(id,uid)
                NegocioNivel.actualiza_nivel_all()
                session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
                session.modified = True

            if pd == 0:
                return redirect(url_for("allDepositos"))
            else:
                return redirect("/gestion-depositos/pd/"+str(pd))
    except Exception as e:
        return error(e,"pedidos")


@app.route('/gestion-depositos/cancelar/<id>')
def get_info_cancelar(id):
    return jsonify(NegocioDeposito.get_info_cancelar(id))

@app.route('/gestion-depositos/info/<id>')
def deposito_info(id):
    try:
        dep = NegocioDeposito.get_by_id(id)

        usuario = {}
        if dep.isAcreditado():
            user_id = NegocioDeposito.get_user_id(id)
            user = NegocioUsuario.get_by_id(user_id)
            td = NegocioTipoDocumento.get_by_id(user.tipoDoc)
            usuario = {"id":user.id,"nombre":user.nombre,"apellido":user.apellido,"tipoDoc":td.nombre,"nroDoc":user.nroDoc,"email":user.email}
        
        pd = NegocioPuntoDeposito.get_by_id(dep.idPuntoDeposito)
        deposito = {"id":dep.id,"codigo":dep.codigo,"fechaDeposito":dep.fechaDeposito,"fechaRegistro":dep.fechaRegistro,"ecoPuntos":dep.ecoPuntos.cantidad}
        punto_deposito = {"id":pd.id,"nombre":pd.nombre,"calle":pd.direccion.calle,"altura":pd.direccion.altura,"ciudad":pd.direccion.ciudad,"provincia":pd.direccion.provincia,"pais":pd.direccion.pais}
        return jsonify([deposito, usuario, punto_deposito])
    except Exception as e:
        return error(e,"pedidos")


@app.route('/gestion-depositos/buscar-info-user/<busqueda>')
def buscar_info_user(busqueda):
    try:
        users = NegocioUsuario.buscar_info_user(busqueda)
        users_dic =  [{"id":      u.id,
                     "nombre":    u.nombre+" "+u.apellido,
                     "tiponroDoc":   u.nroDoc + " ("+u.tipoDoc.nombre+")",
                     "email":     u.email}
                     for u in users]
        return jsonify(users_dic)
    except Exception as e:
        return jsonify(str(e))


@app.route('/depositos/usuario', methods = ['GET','POST'])
def depositos():
    try:
        depositos = NegocioDeposito.get_by_id_usuario(session["usuario"].id)
        puntosDep = NegocioPuntoDeposito.get_all()
        materiales = NegocioMaterial.get_all()
        return render_template('depositosUser.html',usuario = session["usuario"],depositos = depositos, puntosDep = puntosDep, materiales = materiales)  
    except Exception as e:
        return error(e,"depositos")

'''
    -----------------------
    Simulador de Depósitos
    -----------------------
'''

@app.route('/simulador', methods = ['GET','POST'])
def simulador_depositos():
    try:
        if request.method == 'POST':
            pass
        pds = NegocioPuntoDeposito.get_all()
        return render_template('simulador-depositos.html', puntos_deposito = pds)  
    except Exception as e:
        return error(e,"simulador_depositos")

@app.route('/simulador/alta-deposito/<idmat>/<idpd>/<cantidad>', methods = ['GET','POST'])
def alta_deposito(idmat,idpd,cantidad):
    try:
        material = NegocioMaterial.get_by_id(idmat)
        factor_conversion = NegocioEcoPuntos.get_factor_recompensa_EP()
        valor_ep = NegocioEcoPuntos.get_valor_EP()
        cant_EP = round(float(material.costoRecoleccion * factor_conversion * float(cantidad) * float(valor_ep)),0)
        codigo = NegocioDeposito.alta(idmat,idpd,cantidad,cant_EP)
        return jsonify(codigo, cant_EP)
    except Exception as e:
        return error(e,"simulador_depositos")


@app.route('/codigo')
def canjear_codigo():
    try:
        return render_template('codigo.html', usuario = session["usuario"])
    except Exception as e:
        return error(e,"codigo")

@app.route('/codigo/<cod>')
def verificar_codigo(cod):
    try:
        response = NegocioDeposito.verificar_codigo(cod,session["usuario"])
        nuevos_ep = response + session["usuario"].totalEcopuntos
        NegocioUsuario.update_nivel(session["usuario"].id,nuevos_ep)
        session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
        session.modified = True
        return jsonify(response)
    except Exception as e:
        return error(e,"codigo")

''' 
    -----------------
    Gestión de Stock
    -----------------
'''

@app.route('/gestion-stock', methods = ['GET','POST'])
def gestion_stock():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(11): return redirect(url_for("error_auth"))
    try:
        articulos = NegocioArticulo.get_all()
        materiales = NegocioMaterial.get_all()
        entidades = NegocioEntidadDestino.get_all()
        insumos = NegocioInsumo.get_all()

        return render_template('gestion-stock.html', materiales = materiales, articulos=articulos, entidades = entidades, insumos = insumos)  
    except Exception as e:
        return error(e,"gestion_stock")

@app.route('/gestion-stock/ver-stock', methods = ['GET','POST'])
def ver_stock():
    try:
        materiales = NegocioMaterial.get_all()
        insumos = NegocioInsumo.get_all()
        articulos = NegocioArticulo.get_all()
        return render_template('niveles-stock.html',materiales = materiales, insumos = insumos, articulos = articulos)  
    except Exception as e:
        return error(e,"ver_stock")

@app.route('/gestion-stock/historial-movimientos', methods = ['GET','POST'])
def historial_movimientos():
    try:
        salidasStock = NegocioSalidaStock.get_all()
        salidasMun = NegocioSalidaMun.get_all()
        articulos = NegocioArticulo.get_all(True)
        materiales = NegocioMaterial.get_all(True)
        insumos = NegocioInsumo.get_all(True)
        depositos = NegocioDeposito.get_all()
        pedidos = NegocioPedido.get_all_historial_mov()
        entradas = NegocioEntradaExterna.get_all()
        produccionIns = NegocioProduccion.get_all_insumos()
        produccionArt = NegocioProduccion.get_all_articulos()
        return render_template('movimientos-stock.html', salidasStock=salidasStock, salidasMun = salidasMun, 
                                articulos = articulos, depositos = depositos, materiales = materiales, pedidos = pedidos, 
                                entradas = entradas,produccionIns=produccionIns,produccionArt = produccionArt, insumos=insumos)  
    except Exception as e:
        return error(e,"historial_movimientos")

@app.route('/gestion-stock/alta-entrada-mat', methods = ['GET','POST'])
def alta_entrada_mat():
    try:
        if request.method == 'POST':
            idMat = request.form["idMat"]
            cant = request.form["cantidad"]
            concepto = request.form["descripcion"]
            fecha = request.form["fecha"]
            NegocioEntradaExterna.add_one(idMat,cant,concepto, fecha)
        return redirect(url_for('gestion_stock'))  
    except Exception as e:
        return error(e,"gestion_stock")

@app.route('/gestion-stock/alta-salida-mun', methods = ['GET','POST'])
def alta_salida_mun():
    try:
        if request.method == 'POST':
            idArt = request.form["idArtSM"]
            cant = request.form["cantidadSM"]
            concepto = request.form["descripcionSM"]
            fecha = request.form["fechaSM"]
            NegocioSalidaMun.add_one(idArt,cant,concepto, fecha)
        return redirect(url_for('gestion_stock'))  
    except Exception as e:
        return error(e,"gestion_stock")

@app.route('/gestion-stock/alta-salida-ed', methods = ['GET','POST'])
def alta_salida_ed():
    try:
        if request.method == 'POST':
            idArt = request.form["idArtSE"]
            cant = request.form["cantidadSE"]
            concepto = request.form["descripcionSE"]
            fecha = request.form["fechaSE"]
            idEntidad = request.form["idEntidad"]
            valorTotal = request.form["totalValSE"]
            NegocioSalidaStock.add_one(idEntidad,idArt,cant,concepto,fecha,valorTotal)
        return redirect(url_for('gestion_stock'))  
    except Exception as e:
        return error(e,"gestion_stock")

@app.route('/gestion-depositos/chat-data-mat/<id>')
def get_chart_data_mat(id):
    stock = NegocioMaterial.get_by_id(id).stock
    return jsonify(NegocioMaterial.get_movimientos_stock(id,stock))

@app.route('/gestion-depositos/chat-data-ins/<id>')
def get_chart_data_ins(id):
    stock = NegocioInsumo.get_by_id(id).stock
    return jsonify(NegocioInsumo.get_movimientos_stock(id,stock))

@app.route('/gestion-depositos/chat-data-art/<id>')
def get_chart_data_art(id):
    stock = NegocioArticulo.get_by_id(id).stock
    return jsonify(NegocioArticulo.get_movimientos_stock(id,stock))



''' 
    ----------
    REPORTES
    ----------
'''


@app.route('/reportes-admin')
def reportes_admin():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(14): return redirect(url_for("error_auth"))
    materiales = NegocioMaterial.get_all()
    insumos = NegocioInsumo.get_all()
    articulos = NegocioArticulo.get_all()
    return render_template('reportes-admin.html', materiales = materiales, insumos=insumos, articulos=articulos)

@app.route('/reportes-admin/get-cant-usuarios/<meses>')
def get_cant_usuarios(meses):
    cants = NegocioReportes.get_cant_usuarios(meses)
    return jsonify(cants)

@app.route('/reportes-admin/get-cant-depositos/<meses>')
def get_cant_depositos(meses):
    cants = NegocioReportes.get_cant_depositos(meses)
    return jsonify(cants)

@app.route('/reportes-admin/get-cant-pedidos/<meses>')
def get_cant_pedidos(meses):
    cants = NegocioReportes.get_cant_pedidos(meses)
    return jsonify(cants)

@app.route('/reportes-admin/ganancias-art-eco-tienda/<meses>/<idArt>')
def ganancias_art(meses, idArt):
    cants = NegocioReportes.ganancias_art_eco_tienda(idArt,meses)
    return jsonify(cants)

@app.route('/reportes-admin/ganancias-por-art-totales/<meses>/<idArt>')
def ganancias_art_totales(meses, idArt):
    cants = NegocioReportes.ganancias_art_totales(idArt,meses)
    return jsonify(cants)

@app.route('/reportes-admin/ganancias-por-art-totales-globales/<meses>')
def ganancias_art_totales_generales(meses):
    cants = NegocioReportes.ganancias_art_totales_generales(meses)
    return jsonify(cants)

@app.route('/reportes-admin/movimientos-stock-mat/<meses>/<idMat>')
def get_movimientos_stock_materiales(meses, idMat):
    stock = NegocioMaterial.get_by_id(idMat).stock
    cants = NegocioReportes.get_movimientos_stock_materiales(idMat,stock,meses)
    return jsonify(cants)

@app.route('/reportes-admin/movimientos-stock-ins/<meses>/<idIns>')
def get_movimientos_stock_insumos(meses, idIns):
    stock = NegocioInsumo.get_by_id(idIns).stock
    cants = NegocioReportes.get_movimientos_stock_insumos(idIns,stock,meses)
    return jsonify(cants)

@app.route('/reportes-admin/movimientos-stock-art/<meses>/<idArt>')
def get_movimientos_stock_articulos(meses, idArt):
    stock = NegocioArticulo.get_by_id(idArt).stock
    cants = NegocioReportes.get_movimientos_stock_articulos(idArt,stock,meses)
    return jsonify(cants)

@app.route('/reportes-admin/porcentaje-dep-acreditados/')
def porcentaje_dep_acreditados():
    cants = NegocioReportes.porcentaje_dep_acreditados()
    return jsonify(cants)

@app.route('/reportes-admin/porcentaje-dep-pd/')
def porcentaje_dep_por_pd():
    cants = NegocioReportes.porcentaje_dep_por_pd()
    return jsonify(cants)

@app.route('/reportes-admin/porcentaje-ped-pr/')
def porcentaje_ped_por_pr():
    cants = NegocioReportes.porcentaje_ped_por_pr()
    return jsonify(cants)

@app.route('/reportes-admin/ingresos-egresos-globales/<meses>')
def ingresos_egresos_globales(meses):
    cants = NegocioReportes.ingresos_egresos_globales(meses)
    return jsonify(cants)

@app.route('/reportes-admin/ingresos-costos/<meses>')
def ingresos_globales(meses):
    ing = NegocioReportes.ingresos_globales(meses)
    egr = NegocioReportes.egresos_globales(meses)
    return jsonify({"ingresos":ing,"egresos":egr})

@app.route('/reportes-admin/cant-dep-por-mat/<meses>/<idMat>')
def cantidad_depositada_por_material(meses,idMat):
    cants = NegocioReportes.cantidad_depositada_por_material(idMat,meses)
    return jsonify(cants)

@app.route('/reportes-admin/cant-ped-por-art/<meses>/<idArt>')
def cantidad_pedida_por_articulo(meses,idArt):
    cants = NegocioReportes.cantidad_pedida_por_articulo(idArt,meses)
    return jsonify(cants)


''' 
    ----------
    PRODUCCION
    ----------
'''
@app.route('/produccion')
def gestion_prod():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(5): return redirect(url_for("error_auth"))
    return render_template('elegirProd.html',usuario=session["usuario"])

@app.route('/produccion/insumos')
def prod_Insumos():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(5): return redirect(url_for("error_auth"))
    insumos = NegocioInsumo.get_all()
    prods = NegocioProduccion.get_all_insumos()
    return render_template('insumosProd.html',insumos=insumos,prods=prods,usuario=session["usuario"])

@app.route('/produccion/articulos')
def prod_Articulos():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(5): return redirect(url_for("error_auth"))
    articulos = NegocioArticulo.get_all()
    prods = NegocioProduccion.get_all_articulos()
    return render_template('articulosProd.html', articulos=articulos,usuario=session["usuario"],prods=prods)


@app.route('/produccion/insumos/<id>')
def get_materiales_prod(id):
    ins = NegocioInsumo.get_by_id(id)
    ids = [i.idMaterial for i in ins.materiales]
    cants = [i.cantidad for i in ins.materiales]
    materiales = NegocioMaterial.get_by_id_array(ids)
    materiales_dic =  [{"nombre":   m.nombre,
                        "stock":    m.stock,
                        "cant":     c}
                        for m,c in list(zip(materiales,cants))]
    materiales_dic.append({"nombre": ins.nombre,"stock": ins.stock})
    return jsonify(materiales_dic)


@app.route('/produccion/articulos/<id>')
def get_insumos_prod(id):
    art = NegocioArticulo.get_by_id(id)
    ids = [i.idInsumo for i in art.insumos]
    cants = [i.cantidad for i in art.insumos]
    insumos = NegocioInsumo.get_by_id_array(ids)
    insumos_dic =  [{"nombre":   i.nombre,
                     "stock":    i.stock,
                     "cant":     c}
                     for i,c in list(zip(insumos,cants))]
    insumos_dic.append({"nombre": art.nombre,"stock": art.stock})
    return jsonify(insumos_dic)



@app.route('/produccion/insumos/confirmar',methods=["POST","GET"])
def confirmar_prod_ins():
    try:
        if request.method == 'POST':
            id = int(request.form["idIns"])
            cant = float(request.form["cantidad"])
            NegocioProduccion.confirmar_produccion(id,cant,"ins")
        return redirect(url_for('prod_Insumos'))
    except Exception as e:
        return error(e,"produccion-ins")


@app.route('/produccion/articulos/confirmar',methods=["POST","GET"])
def confirmar_prod_art():
    try:
        if request.method == 'POST':
            id = int(request.form["idArt"])
            cant = float(request.form["cantidad"])
            NegocioProduccion.confirmar_produccion(id,cant,"art")
        return redirect(url_for('prod_Articulos'))
    except Exception as e:
        return error(e,"produccion-art")


''' 
    ----------
    Gestión de Usuarios
    ----------
'''

@app.route('/elegir-tipo-gu', methods = ['GET','POST'])
def elegir_tipo_gu():
    if valida_session(): return redirect(url_for('login'))
    if not (valida_permiso(4) or valida_permiso(10)): return redirect(url_for("error_auth"))
    try:
        return render_template('elegir-tipo-gu.html')  
    except Exception as e:
        return error(e,"gestion_usuarios")

@app.route('/gestion-usuarios',methods=["POST","GET"])
def gestion_usuarios():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(4): return redirect(url_for("error_auth"))
    try:
        usuarios = NegocioUsuario.get_all(True)
        tiposDoc = NegocioTipoDocumento.get_all()
        tipos_usuario = NegocioTipoUsuario.get_all()
        return render_template('gestion-usuarios.html', usuarios = usuarios, tiposDoc=tiposDoc, tipos_usuario=tipos_usuario)  
    except Exception as e:
        return error(e,"gestion_usuarios")

@app.route('/gestion-usuarios/add-tu',methods=["POST","GET"])
def add_tipo_usuario():
    try:
        if request.method == 'POST':
            name = request.form["tuInput"]
            NegocioTipoUsuario.add_one(name)
        return redirect(url_for('permisos_acceso'))
    except Exception as e:
        return error(e,"gestion_usuarios")

@app.route('/gestion-usuarios/baja-tu',methods=["POST","GET"])
def baja_tipo_usuario():
    try:
        if request.method == 'POST':
            id_tu_baja = request.form["idTuBaja"]
            id_tu_reemplazo = request.form["idTuBajaRemplazo"]
            NegocioTipoUsuario.baja(id_tu_baja,id_tu_reemplazo)
        return redirect(url_for('permisos_acceso'))
    except Exception as e:
        return error(e,"gestion_usuarios")

@app.route('/permisos-acceso', methods = ['GET','POST'])
def permisos_acceso():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(10): return redirect(url_for("error_auth"))
    try:
        tiposUsuario = NegocioTipoUsuario.get_all()
        modulos = NegocioModulo.get_all()
        return render_template('permisos-usuarios.html', tipos_usuario = tiposUsuario, modulos = modulos)  
    except Exception as e:
        return error(e,"permisos_acceso")

@app.route('/permisos-acceso/modulos/<id>', methods = ['GET','POST'])
def get_modulos(id):
    try:
        return jsonify(NegocioTipoUsuario.get_by_id(id).modulosAcceso)
    except Exception as e:
        return error(e,"permisos_acceso")


@app.route('/permisos-acceso/modulos/all', methods = ['GET','POST'])
def get_modulos_all():
    try:
        modulos = []
        mods = NegocioModulo.get_all()
        for mod in mods:
            modulos.append(mod.id)
        return jsonify(modulos)
    except Exception as e:
        return error(e,"permisos_acceso")

@app.route('/permisos-acceso/add/<id_modulo>/<idTipoUsuario>', methods = ['GET','POST'])
def add_permiso(id_modulo,idTipoUsuario):
    try:
        
        return jsonify(NegocioTipoUsuario.add_permiso(idTipoUsuario, id_modulo))
    except Exception as e:
        return error(e,"permisos_acceso")

@app.route('/permisos-acceso/remove/<id_modulo>/<idTipoUsuario>', methods = ['GET','POST'])
def remove_permiso(id_modulo,idTipoUsuario):
    try:
        
        return jsonify(NegocioTipoUsuario.remove_permiso(idTipoUsuario, id_modulo))
    except Exception as e:
        return error(e,"permisos_acceso")

@app.route('/gestion-usuarios/tipos-usuario/', methods = ['GET','POST'])
def get_all_tipos():
    try:
        tipos_ = NegocioTipoUsuario.get_all()
        tipos = []
        for tu in tipos_:
            tipos.append(tu.nombre)
        return jsonify(tipos)
    except Exception as e:
        return error(e,"permisos_acceso")


@app.route('/gestion-usuarios/mod', methods = ['GET','POST'])
def mod_user():
    try:
        if request.method == 'POST':
            nombre = request.form["nombre"]
            apellido = request.form["apellido"]
            email = request.form["email"]
            id_direccion_gu = request.form["idDireccionUser"]
            calle = request.form['callePDMod']
            altura = request.form['alturaPDMod']
            ciudad = request.form['ciudadPDMod']
            provincia = request.form['provinciaPDMod']
            pais = request.form['paisPDMod']
            documento = request.form["documentoInput"]
            id_tipo_doc = request.form["tipoDocSelect"]
            id_tipo_usuario = request.form["id_tipo_usuario"]
            uid = request.form["idUsuario"]
            NegocioUsuario.update(nombre, apellido, email, id_direccion_gu, calle, altura, ciudad, provincia, pais, documento, id_tipo_doc, id_tipo_usuario,uid)
            session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
            session.modified = True
            return redirect(url_for('gestion_usuarios'))
    except Exception as e:
        return error(e,"gestion_usuarios")

@app.route('/gestion-usuarios/baja', methods = ['GET','POST'])
def baja_user():
    try:
        if request.method == 'POST':
            id_usuario = request.form["idUsuarioBaja"]
            NegocioUsuario.baja(id_usuario)
            return redirect(url_for('gestion_usuarios'))
    except Exception as e:
        return error(e,"gestion_usuarios")


@app.route('/gestion-usuarios/get-list/<type>', methods = ['GET','POST'])
def gu_listas(type):
    try:
        if type == 'emails':
            return jsonify(NegocioUsuario.get_all_emails())
        if type == 'documentos':
            return jsonify(NegocioUsuario.get_all_documentos())
        if type == 'documentos_no_filter':
            return jsonify(NegocioUsuario.get_all_documentos())
    except Exception as e:
        return error(e,"perfil")
    return render_template('login.html')

'''
    -----------------------
    Quienes somos
    -----------------------
'''
@app.route('/quienes-somos', methods = ['GET','POST'])
def nosotros():
    return render_template('quienes-somos.html')

'''
    -----------------------
    Documentación
    -----------------------
'''
@app.route('/documentacion', methods = ['GET','POST'])
def documentacion():
    return render_template('documentacion.html')

'''
    -----------------------
    Ayuda
    -----------------------
'''
@app.route('/ayuda-faq', methods = ['GET','POST'])
def help():
    return render_template('ayuda-usuario.html')

@app.route('/ayuda-admin', methods = ['GET','POST'])
def help_admin():
    if len(NegocioTipoUsuario.get_by_id(session["usuario"].idTipoUsuario).modulosAcceso) >= 1:
        return render_template('ayuda-admin.html')
    else:
        return redirect('/auth-error')


'''
    -----------------------
    Config
    -----------------------
'''
@app.route('/config', methods = ['GET','POST'])
def config():
    if valida_session(): return redirect(url_for('login'))
    if not valida_permiso(13): return redirect(url_for("error_auth"))
    EPs = NegocioEcoPuntos.get_valores_EP()
    EPs = [[i[0].strftime("%d/%m/%Y"),i[1]] for i in EPs]
    Recs = NegocioEcoPuntos.get_factores_recompensa()
    Recs = [[i[0].strftime("%d/%m/%Y"),i[1]] for i in Recs]
    return render_template('config.html',EPs=EPs,Recs=Recs)


@app.route('/config/confirmar', methods = ['GET','POST'])
def config_cambio():
    value = float(request.form["nuevoValor"])
    config = request.form["config"]
    try:
        NegocioEcoPuntos.updateConfig(config,value)
        return redirect(url_for('config'))
    except Exception as e:
        return error(e,"config")

@app.route('/config/get-light-mode', methods = ['GET','POST'])
def get_light_mode():
    try:
        return jsonify(session["light-mode"])
    except: 
        return jsonify('exeption')

@app.route('/config/set-light-mode', methods = ['GET','POST'])
def set_light_mode():
    try:
        print(session["light-mode"])
        if session["light-mode"] == 'day':
            session["light-mode"] = 'night'

        elif session["light-mode"] == 'night':
            session["light-mode"] = 'day'
        print(session["light-mode"])
        return jsonify(True)
    except:
        session["light-mode"] = 'day'
        return jsonify(False)

'''
    -----------------------
    Páginas de error
    -----------------------
'''

@app.route('/user-error', methods = ['GET','POST'])
def error_usuario():
    try:
        return render_template("user-error-page.html")
    except Exception as e:
        return error(e,"error")

@app.route('/auth-error', methods = ['GET','POST'])
def error_auth():
    try:
        return render_template("auth-error-page.html")
    except Exception as e:
        return error(e,"error")

  
def valida_session():
    return "usuario" not in session.keys()

def valida_permiso(idModulo):
    return idModulo in NegocioTipoUsuario.get_by_id(session["usuario"].idTipoUsuario).modulosAcceso



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
