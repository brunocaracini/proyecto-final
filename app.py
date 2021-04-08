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
            NegocioUsuario.update_img(session["usuario"].id,dir)
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
            puntosDep = NegocioPuntoDeposito.get_all()
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
    return jsonify({"nombre":session["usuario"].nombre + " " + session["usuario"].apellido, "totalEP":session["usuario"].totalEcopuntos, "img":session["usuario"].img,"carrito": carrito})

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
        session.modified = True
        return jsonify({"login-state":True})
    except Exception as e:
        return error(e,"gestion-puntos-deposito")
    return render_template('login.html')

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
        nivel = NegocioNivel.get_nivel_id(session["usuario"].idNivel)
        valor_ep = NegocioEcoPuntos.get_valor_EP()
    except Exception as e:
        return error(e, "eco-tienda")
    return render_template('eco-tienda.html', articulos = articulos, usuario = session["usuario"], nivel = nivel, valor_ep = valor_ep)


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
        return render_template('product-page.html',producto=producto, recomendaciones=recomendaciones, nivel = nivel, usuario = session["usuario"], valor_ep = valor_ep, demora_prom  = demora_prom)
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
        print(step)
        puntos_retiro = NegocioPuntoRetiro.get_all(filterInactivos=True)
        
        return render_template('carrito.html',carrito=Utils.carrito_to_list(session["carrito"]),articulos=articulos, 
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
    Niveles
    -------
'''

@app.route('/gestion-niveles')
def gestion_niveles():
    try:
        if valida_session(): return redirect(url_for('login'))
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


''' 
    -----------------
    Entidades Destino
    -----------------
'''

@app.route('/gestion-ed', methods = ['GET','POST'])
def gestion_ed():
    try:
        if valida_session(): return redirect(url_for('login'))
        entidades = NegocioEntidadDestino.get_all()
    except Exception as e:
        return error(e,"gestion_ed")
    return render_template('gestion-entidades-destino.html', entidades = entidades, usuario=session["usuario"])


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
    return render_template('elegir-tipo-punto.html', usuario = session["usuario"])


@app.route('/gestion-puntos-deposito', methods = ['GET','POST'])
def gestion_pd():
    try:
        if valida_session(): return redirect(url_for('login'))
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
    try:
        if valida_session(): return redirect(url_for('login'))
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
        print(id)
        #NegocioPuntoRetiro.baja_pr(id)
        
    return redirect(url_for('gestion_pr'))


''' 
    -----------------
    Articulos
    -----------------
'''

@app.route('/articulos', methods = ['GET','POST'])
def gestion_articulos():
    try:
        if valida_session(): return redirect(url_for('login'))
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


        #INSUMOS
        cants = []
        for key in request.form.keys():
            if "id-" in key:
                id = request.form[key]
                cant = float(request.form["cantidad-"+id])
                if cant > 0:
                    cants.append({"idIns":id,"cantidad":cant})

        try:
            idNuevoArt = NegocioArticulo.add(nombre,unidad,ventaUsuario,costoInsumos,costoProduccion,otrosCostos,costoObtencionAlt,margen,valor,cants)
        
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
                NegocioArticulo.update_img(idNuevoArt,imagen)

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
                NegocioArticulo.update_img(idArt,imagen)
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




''' 
    -----------------
    Insumos
    -----------------
'''

@app.route('/insumos', methods = ['GET','POST'])
def gestion_insumos():
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
        cants = []
        for key in request.form.keys():
            if "id-" in key:
                id = request.form[key]
                cant = float(request.form["cantidad-"+id])
                if cant > 0:
                    cants.append({"idMat":id,"cantidad":cant})
        try:
            NegocioInsumo.add(nombre,unidad,costoMateriales,costoProduccion,otrosCostos,color,cants)
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
        try:
            NegocioMaterial.add(nombre,unidad,costoRecoleccion,color,estado)
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
  
  
def valida_session():
    return "usuario" not in session.keys()


'''
    -----------------
    Gestion de Pedidos
    -----------------
'''

@app.route('/elegir-PR')
def elegirPR():
    try:
        puntosRetiro = NegocioPuntoRetiro.get_all()
        return render_template('elegir-PR.html',puntosRetiro = puntosRetiro, usuario=session["usuario"])
    except Exception as e:
        return error(e,"pedidos")

@app.route('/gestion-pedidos/deposito')
def deposito():
    try:
        pedidos = NegocioPedido.get_all()
        puntosRetiro = NegocioPuntoRetiro.get_all(True)
        return render_template('deposito.html',pedidos = pedidos,puntosRetiro=puntosRetiro, usuario=session["usuario"])
    except Exception as e:
        return error(e,"pedidos")

@app.route('/gestion-pedidos/pr/<id>')
def pedidosPR(id):
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
        return render_template('pedidosUser.html',pedidos = pedidos_ordenados,puntosRetiro=puntosRetiro, usuario=session["usuario"])
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
    try:
        puntosDeposito = NegocioPuntoDeposito.get_all()
        return render_template('elegir-PD.html',puntosDeposito = puntosDeposito, usuario=session["usuario"])
    except Exception as e:
        return error(e,"depositos")

@app.route('/gestion-depositos/admin')
def allDepositos():
    try:
        materiales = NegocioMaterial.get_all()
        depositos = NegocioDeposito.get_all()
        puntosDeposito = NegocioPuntoDeposito.get_all()
        return render_template('depositosAdmin.html',materiales=materiales,depositos = depositos,puntosDeposito=puntosDeposito, usuario=session["usuario"])
    except Exception as e:
        return error(e,"pedidoss")

@app.route('/gestion-depositos/pd/<id>')
def pedidosPD(id):
    try:
        materiales = NegocioMaterial.get_all()
        deposito = NegocioDeposito.get_by_id_PD(int(id))
        puntoDeposito = NegocioPuntoDeposito.get_by_id(int(id))
        return render_template('depositosPD.html',materiales=materiales,deposito = deposito,puntoDeposito=puntoDeposito, usuario=session["usuario"])
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
                session["usuario"] = NegocioUsuario.get_by_id(session["usuario"].id)
                session.modified = True
                

            elif estado == "acreditado":
                uid = int(request.form["idUser"])
                #NegocioDeposito.acreditar(id,uid)

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
    -----------------------
    Quienes somos
    -----------------------
'''
@app.route('/quienes-somos', methods = ['GET','POST'])
def nosotros():
    return render_template('quienes-somos.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)