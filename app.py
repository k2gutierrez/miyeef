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

###### date today
hoy = date.today()

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
    nivel = 1
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
    a = ''
    cdc = db.child(localId).child('dolencias').child('CausasDeCausas').get().val()
    lvl = db.child(localId).child('NIVEL').get().val()

    if lvl == 2:
        lvl == 2
    else:
        lvl == 1

    if cdc is not None:
        a = 'go'
    else:
        a = 'no'

    return render_template('home.html', cdc=cdc, a=a, lvl=lvl)

##############################################################################################
@app.route('/cuestionario0', methods= ['POST', 'GET'])
def cuestionario0():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']

    if request.method == 'POST':
        listp = request.form.getlist('t1')
        listatl = []
        for i in listp:
            if i != '':
                listatl.append(i)

        if len(listatl) == 0:
            listatl = ['No hay registros']
        else:
            listatl


        db.child(localId).child('dolencias').child("listaP").set(listatl)

        return redirect(url_for('.cuestionario1'))

    return render_template('cuestionario0.html')

###############################################################################################
@app.route('/cuestionario1', methods= ['POST', 'GET'])
def cuestionario1():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']

    if request.method == 'GET':

        token = session['user']
        user = auth.get_account_info(token)
        localId = user['users'][0]['localId']

        lista = listaC1
        return render_template('cuestionario1.html', lista=lista)

    elif request.method == "POST":
        select1 = request.form.getlist('check1')
        
        if len(select1) >= 1:
            select = select1
        else:
            select = ['No hay registros']

        db.child(localId).child('dolencias').child('lista seleccionada1').set(select)
        
        return redirect(url_for('.cuestionario2'))

######################################################################################################
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