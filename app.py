from ctypes import c_ssize_t
from click import style
from flask import Flask, render_template, request, redirect, url_for, session, make_response
import pyrebase
import os
from datetime import date

app = Flask(__name__)

app.secret_key = os.urandom(24)

firebaseConfig = {
  'apiKey': "AIzaSyD5mRUV08gkotpiTMoigFJd9Bfb9O8_hgQ",
  'authDomain': "cedem-db.firebaseapp.com",
  'databaseURL': "https://cedem-db-default-rtdb.firebaseio.com/",
  'projectId': "cedem-db",
  'storageBucket': "cedem-db.appspot.com",
  'messagingSenderId': "272607335771",
  'appId': "1:272607335771:web:dff8951eb8e08f8eef367e",
  'measurementId': "G-ZT3V8MY4NC"
  }


#Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
#authentication
auth = firebase.auth()
#Storage
storage = firebase.storage()
#Database
db=firebase.database()

@app.route('/registro', methods = ['POST', 'GET'])
def registro():

    nombre = ''
    correo = ''
    password = ''
    nivel = 5
    mensaje = ''
    exist = 0
    
    if request.method == "POST":
        nombre = str(request.form.get('nombre'))
        correo = str(request.form.get('correo'))
        password = str(request.form.get('password'))
        #búsqueda
        try:
            #Registro#
            user = auth.create_user_with_email_and_password(correo,password)
            #Sign in #
            user = auth.sign_in_with_email_and_password(correo, password)
            db.child(user['localId']).child('ID').set(user['localId'])
            db.child(user['localId']).child('NAME').set(nombre)
            db.child(user['localId']).child('EMAIL').set(correo)
            db.child(user['localId']).child('NIVEL').set(nivel)
            user = auth.refresh(user['refreshToken'])
            user_id = user['idToken']
            session['user'] = user_id
            return redirect(url_for('.home'))
        except:
            exist = 1
            mensaje = 'Este correo ya está registrado! Da click en Ingresa o registrate con otro correo.'
            return render_template('registro.html', mensaje=mensaje, exist=exist)

    return render_template('registro.html')

#########################################################################################
@app.route('/', methods= ['POST', 'GET'])
def index():

    correo = ''
    password = ''
    message = ''
    try:
        session['usr']
        return redirect(url_for('.home'))
    except KeyError:
        if request.method == "POST":
            correo = str(request.form.get('correo'))
            password = str(request.form.get('password'))
            try:
                user = auth.sign_in_with_email_and_password(correo, password)
                user = auth.refresh(user['refreshToken'])
                user_id = user['idToken']
                session['user'] = user_id
                return redirect(url_for('.home'))
            except:
                message = '¡Correo o contraseña incorrectos!, intenta nuevamente.'
                return render_template('index.html', message=message)

    return render_template('index.html')

#########################################################################################
@app.route('/resetpassword', methods= ['POST', 'GET'])
def resetpassword():

    correo = ''
    mensaje = ''

    if request.method == "POST":
        correo = str(request.form.get('correo'))
        auth.send_password_reset_email(correo)
        mensaje = 'Se ha enviado un correo para cambiar tu contraseña, sigue las instrucciones e ingresa nuevamente. En caso de no velor en tu bandeja revisa en tu apartado de SPAM'

        return render_template('resetpassword.html', correo=correo, mensaje=mensaje)

    return render_template('resetpassword.html')

##############################################################################################
@app.route('/home', methods= ['POST', 'GET'])
def home():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    a = db.child(localId).child('NAME').get().val()
    lvl = db.child(localId).child('NIVEL').get().val()

    if lvl == 3:
        lvl = 3
    elif lvl == 4:
        lvl = 4
    else:
        lvl = 5

    return render_template('home.html', a=a, lvl=lvl)

######################################################################################################
@app.route('/asignar', methods=['GET', 'POST'])
def asignar():

    token = session['user']
    user = auth.get_account_info(token)

    nada = ['No hay registro']
    listaregistros = []
    nama = ''
    cdc = db.get()
    identificacion = ''
    nom = request.form.get('sele')

    change = 0
    namae = ''

    for i in cdc:
        nivel = db.child(i.key()).child('NIVEL').get().val()
        if nivel == 4:
            nama = db.child(i.key()).child('NAME').get().val()
            listaregistros.append(nama)

    if nom == None:
        change

    else:
        for a in cdc:
            ident = db.child(a.key()).child('NAME').get().val()
            if ident == nom:
                identificacion = a.key()


        
        namae = db.child(identificacion).child('NAME').get().val()

        change = 1

    return render_template('asignar.html', listaregistros=listaregistros, identificacion=identificacion, nom=nom, change=change, namae=namae, nama=nama)


##############################################################################################
@app.route('/mcymd', methods= ['POST', 'GET'])
def mcymd():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = ''
    mdisc = ''
    mensaje = ''
    hoy = date.today()

    fecha = db.child(localId).child('MASTER').child("mejora continua y mejora discontinua").child('fecha').get().val()
    mc = db.child(localId).child('MASTER').child("mejora continua y mejora discontinua").child('mejora continua').get().val()
    md = db.child(localId).child('MASTER').child("mejora continua y mejora discontinua").child('mejora discontinua').get().val()

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if mc == None:
        mc = ''
    else:
        mc
        
    if md == None:
        md = ''
    else:
        md

    

    if request.method == 'POST':
        mcont = request.form.get('t1')
        mdisc = request.form.get('t2')

        if len(mcont) == 0:
            mcont = ['No hay registros']
        else:
            mcont

        if len(mdisc) == 0:
            mdisc = ['No hay registros']
        else:
            mdisc

        
        mc = db.child(localId).child('MASTER').child("mejora continua y mejora discontinua").child('mejora continua').set(mcont)
        mc
        md = db.child(localId).child('MASTER').child("mejora continua y mejora discontinua").child('mejora discontinua').set(mdisc)
        md
        fecha = db.child(localId).child('MASTER').child("mejora continua y mejora discontinua").child('fecha').set(str(hoy))
        fecha
        mensaje = 'Los registros han quedado guardados'

    return render_template('mcymd.html', mdisc=mdisc, mcont=mcont, mensaje=mensaje, mc=mc, md=md, nombre=nombre, fecha=fecha)

##############################################################################################
@app.route('/decgv', methods= ['POST', 'GET'])
def decgv():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = ''
    mensaje = ''
    hoy = date.today()

    fecha = db.child(localId).child('MASTER').child("enfoque competitivo y generacion de valor").child('fecha').get().val()
    mc = db.child(localId).child('MASTER').child("enfoque competitivo y generacion de valor").child('respuesta').get().val()

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if mc == None:
        mc = ''
    else:
        mc

    if request.method == 'POST':
        mcont = request.form.get('t1')

        if len(mcont) == 0:
            mcont = ['No hay registros']
        else:
            mcont

        
        mc = db.child(localId).child('MASTER').child("enfoque competitivo y generacion de valor").child('respuesta').set(mcont)
        mc
        fecha = db.child(localId).child('MASTER').child("enfoque competitivo y generacion de valor").child('fecha').set(str(hoy))
        fecha
        mensaje = 'Los registros han quedado guardados'

    return render_template('decgv.html', mcont=mcont, mensaje=mensaje, mc=mc, nombre=nombre, fecha=fecha)

##############################################################################################
@app.route('/dsomv', methods= ['POST', 'GET'])
def dsomv():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = ''
    mensaje = ''
    hoy = date.today()

    fecha = db.child(localId).child('MASTER').child("sinergia organizacional y multiplicacion de valor").child('fecha').get().val()
    mc = db.child(localId).child('MASTER').child("sinergia organizacional y multiplicacion de valor").child('respuesta').get().val()

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if mc == None:
        mc = ''
    else:
        mc

    if request.method == 'POST':
        mcont = request.form.get('t1')

        if len(mcont) == 0:
            mcont = ['No hay registros']
        else:
            mcont

        
        mc = db.child(localId).child('MASTER').child("sinergia organizacional y multiplicacion de valor").child('respuesta').set(mcont)
        mc
        fecha = db.child(localId).child('MASTER').child("sinergia organizacional y multiplicacion de valor").child('fecha').set(str(hoy))
        fecha
        mensaje = 'Los registros han quedado guardados'

    return render_template('dsomv.html', mcont=mcont, mensaje=mensaje, mc=mc, nombre=nombre, fecha=fecha)

##############################################################################################
@app.route('/daecv', methods= ['POST', 'GET'])
def daecv():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = ''
    mensaje = ''
    hoy = date.today()

    fecha = db.child(localId).child('MASTER').child("alineacion estrategica y captura de valor").child('fecha').get().val()
    mc = db.child(localId).child('MASTER').child("alineacion estrategica y captura de valor").child('respuesta').get().val()

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if mc == None:
        mc = ''
    else:
        mc

    if request.method == 'POST':
        mcont = request.form.get('t1')

        if len(mcont) == 0:
            mcont = ['No hay registros']
        else:
            mcont

        
        mc = db.child(localId).child('MASTER').child("alineacion estrategica y captura de valor").child('respuesta').set(mcont)
        mc
        fecha = db.child(localId).child('MASTER').child("alineacion estrategica y captura de valor").child('fecha').set(str(hoy))
        fecha
        mensaje = 'Los registros han quedado guardados'

    return render_template('daecv.html', mcont=mcont, mensaje=mensaje, mc=mc, nombre=nombre, fecha=fecha)


##############################################################################################
@app.route('/impeinh', methods= ['POST', 'GET'])
def impeinh():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = ''
    mdisc = ''
    mensaje = ''
    hoy = date.today()

    fecha = db.child(localId).child('MASTER').child("impulsores e inhibidores de valor").child('fecha').get().val()
    mc = db.child(localId).child('MASTER').child("impulsores e inhibidores de valor").child('impulsores').get().val()
    md = db.child(localId).child('MASTER').child("impulsores e inhibidores de valor").child('inhibidores').get().val()

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if mc == None:
        mc = ''
    else:
        mc
        
    if md == None:
        md = ''
    else:
        md

    

    if request.method == 'POST':
        mcont = request.form.get('t1')
        mdisc = request.form.get('t2')

        if len(mcont) == 0:
            mcont = ['No hay registros']
        else:
            mcont

        if len(mdisc) == 0:
            mdisc = ['No hay registros']
        else:
            mdisc

        
        mc = db.child(localId).child('MASTER').child("impulsores e inhibidores de valor").child('impulsores').set(mcont)
        mc
        md = db.child(localId).child('MASTER').child("impulsores e inhibidores de valor").child('inhibidores').set(mdisc)
        md
        fecha = db.child(localId).child('MASTER').child("impulsores e inhibidores de valor").child('fecha').set(str(hoy))
        fecha
        mensaje = 'Los registros han quedado guardados'

    return render_template('impeinh.html', mdisc=mdisc, mcont=mcont, mensaje=mensaje, mc=mc, md=md, nombre=nombre, fecha=fecha)


##############################################################################################
@app.route('/diques', methods= ['POST', 'GET'])
def diques():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont1 = ''
    mcont2 = ''
    mcont3 = ''
    mensaje = ''
    hoy = date.today()

    fecha = db.child(localId).child('MASTER').child("diques").child('fecha').get().val()
    mc = db.child(localId).child('MASTER').child("diques").child('respuesta').get().val()
    if mc is None:
        mc1 = ''
        mc2 = ''
        mc3 = ''
    else:
        mc1 = mc[0]
        mc2 = mc[1]
        mc3 = mc[2]

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if len(mc1) == 0:
        mc1 = ''
    else:
        mc1
    
    if len(mc2) == 0:
        mc2 = ''
    else:
        mc2

    if len(mc3) == 0:
        mc3 = ''
    else:
        mc3

    if request.method == 'POST':
        mcont1 = request.form.get('text1')
        mcont2 = request.form.get('text2')
        mcont3 = request.form.get('text3')

        mcont = []


        if len(mcont1) == 0:
            mcont1 = ['No hay registros']
        else:
            mcont1

        if len(mcont2) == 0:
            mcont2 = ['No hay registros']
        else:
            mcont2

        if len(mcont3) == 0:
            mcont3 = ['No hay registros']
        else:
            mcont3

        mcont.append(mcont1)
        mcont.append(mcont2)
        mcont.append(mcont3)
        
        mc = db.child(localId).child('MASTER').child("diques").child('respuesta').set(mcont)
        mc
        mc1 = mc[0]
        mc2 = mc[1]
        mc3 = mc[2]
        fecha = db.child(localId).child('MASTER').child("diques").child('fecha').set(str(hoy))
        fecha
        mensaje = 'Los registros han quedado guardados'

    return render_template('diques.html', mcont1=mcont1, mcont2=mcont2, mcont3=mcont3, mensaje=mensaje, mc=mc, nombre=nombre, fecha=fecha, mc1=mc1, mc2=mc2, mc3=mc3)

##############################################################################################
@app.route('/proyectodetonador', methods= ['POST', 'GET'])
def proyectodetonador():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    d = db.child(localId).child('MASTER').child("diques").child('respuesta').get().val()
    diques = []
    for i in d:
        if i != '':
            diques.append(i)

    nombre = db.child(localId).child('NAME').get().val()
    mcont = ''
    mensaje = ''
    hoy = date.today()

    fecha = db.child(localId).child('MASTER').child("proyecto detonador").child('fecha').get().val()
    mc = db.child(localId).child('MASTER').child("proyecto detonador").child('respuesta').get().val()

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if mc == None:
        mc = ''
    else:
        mc

    if request.method == 'POST':
        mcont = request.form.get('t1')

        if len(mcont) == 0:
            mcont = ['No hay registros']
        else:
            mcont

        
        mc = db.child(localId).child('MASTER').child("proyecto detonador").child('respuesta').set(mcont)
        mc
        fecha = db.child(localId).child('MASTER').child("proyecto detonador").child('fecha').set(str(hoy))
        fecha
        mensaje = 'Los registros han quedado guardados'

    return render_template('proyectodetonador.html', mcont=mcont, mensaje=mensaje, mc=mc, nombre=nombre, fecha=fecha, diques=diques)

###############################################################################################

@app.route('/resultado', methods=['GET', 'POST'])
def resultado():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']

    nada = ['No hay registro']

    listaCausas = db.child(localId).child('dolencias').child("Causas").get().val()
    if listaCausas is None:
        listaCausas = nada
    else:
        listaCausas

    listaEfectos = db.child(localId).child('dolencias').child("Efectos").get().val()
    if listaEfectos is None:
        listaEfectos = nada
    else:
        listaEfectos

    listaNoP = db.child(localId).child('dolencias').child("NoProblemas").get().val()
    if listaNoP is None:
        listaNoP = nada
    else:
        listaNoP

    c1 = db.child(localId).child('dolencias').child('CausasDeCausas').child('Contexto').child(0).child('causa').get().val()
    c2 = db.child(localId).child('dolencias').child('CausasDeCausas').child('Contexto').child(1).child('causa').get().val()
    c3 = db.child(localId).child('dolencias').child('CausasDeCausas').child('Contexto').child(2).child('causa').get().val()

    k1 = db.child(localId).child('dolencias').child('CausasDeCausas').child('Contexto').child(0).child('contexto').get().val()
    k2 = db.child(localId).child('dolencias').child('CausasDeCausas').child('Contexto').child(1).child('contexto').get().val()
    k3 = db.child(localId).child('dolencias').child('CausasDeCausas').child('Contexto').child(2).child('contexto').get().val()

    return render_template('resultado.html',k1=k1, k2=k2, k3=k3, c1=c1, c2=c2, c3=c3, listaCausas=listaCausas,
    listaEfectos=listaEfectos, listaNoP=listaNoP)

######################################################################################################
@app.route('/registros', methods=['GET', 'POST'])
def registros():

    token = session['user']
    user = auth.get_account_info(token)

    nada = ['No hay registro']
    listaregistros = []
    
    cdc = db.get()
    listaCausas = []
    listaEfectos = []
    listaNoP = []
    identificacion = ''
    nom = request.form.get('sele')
    k1 = ''
    k2 = ''
    k3 = ''
    c1 = ''
    c2 = ''
    c3 = ''
    change = 0
    namae = ''

    for i in cdc:
        nivel = db.child(i.key()).child('NAME').get().val()
        listaregistros.append(nivel)

    if nom == None:
        change

    else:
        for a in cdc:
            ident = db.child(a.key()).child('NAME').get().val()
            if ident == nom:
                identificacion = a.key()


        listaCausas = db.child(identificacion).child('dolencias').child("Causas").get().val()
        if listaCausas is None:
            listaCausas = nada
        else:
            listaCausas

        listaEfectos = db.child(identificacion).child('dolencias').child("Efectos").get().val()
        if listaEfectos is None:
            listaEfectos = nada
        else:
            listaEfectos

        listaNoP = db.child(identificacion).child('dolencias').child("NoProblemas").get().val()
        if listaNoP is None:
            listaNoP = nada
        else:
            listaNoP

        c1 = db.child(identificacion).child('dolencias').child('CausasDeCausas').child('Contexto').child(0).child('causa').get().val()
        c2 = db.child(identificacion).child('dolencias').child('CausasDeCausas').child('Contexto').child(1).child('causa').get().val()
        c3 = db.child(identificacion).child('dolencias').child('CausasDeCausas').child('Contexto').child(2).child('causa').get().val()

        k1 = db.child(identificacion).child('dolencias').child('CausasDeCausas').child('Contexto').child(0).child('contexto').get().val()
        k2 = db.child(identificacion).child('dolencias').child('CausasDeCausas').child('Contexto').child(1).child('contexto').get().val()
        k3 = db.child(identificacion).child('dolencias').child('CausasDeCausas').child('Contexto').child(2).child('contexto').get().val()
        namae = db.child(identificacion).child('NAME').get().val()

        change = 1

    return render_template('registros.html',k1=k1, k2=k2, k3=k3, c1=c1, c2=c2, c3=c3, listaCausas=listaCausas,
        listaEfectos=listaEfectos, listaNoP=listaNoP, listaregistros=listaregistros, identificacion=identificacion, nom=nom, change=change, namae=namae)


if __name__ == "__main__":
    app.run(threaded=True, debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))