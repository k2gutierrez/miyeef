from flask import Flask, render_template, request, redirect, url_for, session, make_response
import pyrebase
import os
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import config

app = Flask(__name__)

app.secret_key = os.urandom(24)

firebaseConfig = {
  'apiKey': config.apiKey,
  'authDomain': config.authDomain,
  'databaseURL': config.databaseURL,
  'projectId': config.projectId,
  'storageBucket': config.storageBucket,
  'messagingSenderId': config.messagingSenderId,
  'appId': config.appId,
  'measurementId': config.measurementId
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

    mcont = {}
    mensaje = ''
    hoy = date.today()
    fecha = str(hoy)
    lider = ''
    equipo = ''
    proyecto = ''
    plan = ''
    cumplimiento = ''

    if request.method == 'POST':
        
        sele = request.form.get('sele')

        lider = request.form.get('lider')

        equipo = request.form.get('equipo')

        proyecto = request.form.get('proyecto')

        plan = request.form.get('plan')

        cumplimiento = request.form.get('cumplimiento')
        
        mcont = {
            "lider": lider,
            "equipo": equipo,
            "proyecto": proyecto,
            "plan": plan,
            "cumplimiento": cumplimiento,
            "fecha": fecha
        }
        
        mc = db.child(localId).child('MASTER').child("proyecto detonador").child(sele).set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('proyectodetonador.html', mcont=mcont, mensaje=mensaje, diques=diques, lider=lider,
        equipo=equipo, proyecto=proyecto, plan=plan, cumplimiento=cumplimiento, fecha=fecha)

##############################################################################################
@app.route('/valordelaempresa', methods= ['POST', 'GET'])
def valordelaempresa():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    valor = ''
    capital = ''
    ventas = ''
    ebitda = ''
    multiplos = ''
    mensaje = ''
    hoy = date.today()

    valor = db.child(localId).child('MASTER').child("valor de la empresa").child('valor').get().val()
    capital = db.child(localId).child('MASTER').child("valor de la empresa").child('capital').get().val()
    ventas = db.child(localId).child('MASTER').child("valor de la empresa").child('ventas').get().val()
    ebitda = db.child(localId).child('MASTER').child("valor de la empresa").child('ebitda').get().val()
    multiplos = db.child(localId).child('MASTER').child("valor de la empresa").child('multiplos').get().val()
    fecha = db.child(localId).child('MASTER').child("valor de la empresa").child('fecha').get().val()
    
    if valor is None:
        valor = ''
    
    if capital is None:
        capital = ''
    
    if ventas is None:
        ventas = ''

    if ebitda is None:
        ebitda = ''
    
    if multiplos is None:
        multiplos = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        valor = request.form.get('valor')
        capital = request.form.get('capital')
        ventas = request.form.get('ventas')
        ebitda = request.form.get('ebitda')
        multiplos = request.form.get('multiplos')

        mcont = {
            "valor": valor,
            "capital": capital,
            "ventas": ventas,
            "ebitda": ebitda,
            "multiplos": multiplos,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("valor de la empresa").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('valordelaempresa.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, valor=valor, 
    capital=capital, ventas=ventas, ebitda=ebitda, multiplos=multiplos)

##############################################################################################
@app.route('/fusionesyadquisiciones', methods= ['POST', 'GET'])
def fusionesyadquisiciones():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("fusiones y adquisiciones").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("fusiones y adquisiciones").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("fusiones y adquisiciones").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("fusiones y adquisiciones").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('fusionesyadquisiciones.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

##############################################################################################
@app.route('/fertilidad', methods= ['POST', 'GET'])
def fertilidad():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("fertilidad").child('r1').get().val()
    fecha = db.child(localId).child('MASTER').child("fertilidad").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')

        mcont = {
            "r1": r1,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("fertilidad").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('fertilidad.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1)

##############################################################################################
@app.route('/mapacompetitivo', methods= ['POST', 'GET'])
def mapacompetitivo():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("mapa competitivo").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("mapa competitivo").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("mapa competitivo").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("mapa competitivo").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('mapacompetitivo.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

##############################################################################################
@app.route('/segmentaciondemercado', methods= ['POST', 'GET'])
def segmentaciondemercado():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("segmentacion de mercado").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("segmentacion de mercado").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("segmentacion de mercado").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("segmentacion de mercado").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('segmentaciondemercado.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

###############################################################################################
@app.route('/diferenciacion', methods= ['POST', 'GET'])
def diferenciacion():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("diferenciacion").child('r1').get().val()
    fecha = db.child(localId).child('MASTER').child("diferenciacion").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')

        mcont = {
            "r1": r1,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("diferenciacion").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('diferenciacion.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1)

###############################################################################################
@app.route('/managementvsmomentum', methods= ['POST', 'GET'])
def managementvsmomentum():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("management vs momentum").child('r1').get().val()
    fecha = db.child(localId).child('MASTER').child("management vs momentum").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')

        mcont = {
            "r1": r1,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("management vs momentum").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('managementvsmomentum.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1)

###############################################################################################
@app.route('/corebusiness', methods= ['POST', 'GET'])
def corebusiness():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("core business").child('r1').get().val()
    fecha = db.child(localId).child('MASTER').child("core business").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')

        mcont = {
            "r1": r1,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("core business").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('corebusiness.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1)

###############################################################################################
@app.route('/estrategiadeconcentracion', methods= ['POST', 'GET'])
def estrategiadeconcentracion():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("estrategia de concentracion").child('r1').get().val()
    fecha = db.child(localId).child('MASTER').child("estrategia de concentracion").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')

        mcont = {
            "r1": r1,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("estrategia de concentracion").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('estrategiadeconcentracion.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1)

###############################################################################################
@app.route('/fortalecimientocompetitivo', methods= ['POST', 'GET'])
def fortalecimientocompetitivo():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("fortalecimiento competitivo").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("fortalecimiento competitivo").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("fortalecimiento competitivo").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("fortalecimiento competitivo").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('fortalecimientocompetitivo.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

###############################################################################################
@app.route('/estrategiadeabandono', methods= ['POST', 'GET'])
def estrategiadeabandono():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("estrategia de abandono").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("estrategia de abandono").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("estrategia de abandono").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("estrategia de abandono").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('estrategiadeabandono.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

###############################################################################################
@app.route('/nueva-adyacencia', methods= ['POST', 'GET'])
def nuevaadyacencia():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    r3 = ''
    r4 = ''
    r5 = ''
    r6 = ''

    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("nueva adyacencia").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("nueva adyacencia").child('r2').get().val()
    r3 = db.child(localId).child('MASTER').child("nueva adyacencia").child('r3').get().val()
    r4 = db.child(localId).child('MASTER').child("nueva adyacencia").child('r4').get().val()
    r5 = db.child(localId).child('MASTER').child("nueva adyacencia").child('r5').get().val()
    r6 = db.child(localId).child('MASTER').child("nueva adyacencia").child('r6').get().val()
    fecha = db.child(localId).child('MASTER').child("nueva adyacencia").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''
    
    if r3 is None:
        r3 = ''

    if r4 is None:
        r4 = ''
    
    if r5 is None:
        r5 = ''
    
    if r6 is None:
        r6 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')
        r3 = request.form.get('r3')
        r4 = request.form.get('r4')
        r5 = request.form.get('r5')
        r6 = request.form.get('r6')

        mcont = {
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "r4": r4,
            "r5": r5,
            "r6": r6,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("nueva adyacencia").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('nueva-adyacencia.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2, r3=r3, r4=r4, 
    r5=r5, r6=r6)

###############################################################################################
@app.route('/querencia', methods= ['POST', 'GET'])
def querencia():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("querencia").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("querencia").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("querencia").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("querencia").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('querencia.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

###############################################################################################
@app.route('/talentograma', methods= ['POST', 'GET'])
def talentograma():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    r3 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("talentograma").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("talentograma").child('r2').get().val()
    r3 = db.child(localId).child('MASTER').child("talentograma").child('r3').get().val()
    fecha = db.child(localId).child('MASTER').child("talentograma").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if r3 is None:
        r3 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')
        r3 = request.form.get('r3')

        mcont = {
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("talentograma").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('talentograma.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2, r3=r3)


###############################################################################################
@app.route('/formuladegobierno', methods= ['POST', 'GET'])
def formuladegobierno():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("formula de gobierno").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("formula de gobierno").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("formula de gobierno").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("formula de gobierno").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('formuladegobierno.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)
###############################################################################################
@app.route('/formuladepropiedad', methods= ['POST', 'GET'])
def formuladepropiedad():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("formula de propiedad").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("formula de propiedad").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("formula de propiedad").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("formula de propiedad").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('formuladepropiedad.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)
###############################################################################################
@app.route('/alianzasestrategicas', methods= ['POST', 'GET'])
def alianzasestrategicas():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("alianzas estrategicas").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("alianzas estrategicas").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("alianzas estrategicas").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("alianzas estrategicas").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('alianzasestrategicas.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

###############################################################################################
@app.route('/talentoyestrategia', methods= ['POST', 'GET'])
def talentoyestrategia():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("talento y estrategia").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("talento y estrategia").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("talento y estrategia").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("talento y estrategia").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('talentoyestrategia.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

###############################################################################################
@app.route('/alineaciondelaorganizacion', methods= ['POST', 'GET'])
def alineaciondelaorganizacion():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("alineacion de la organizacion").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("alineacion de la organizacion").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("alineacion de la organizacion").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("alineacion de la organizacion").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('alineaciondelaorganizacion.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

###############################################################################################
@app.route('/recursosbasicos', methods= ['POST', 'GET'])
def recursosbasicos():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("recursos basicos").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("recursos basicos").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("recursos basicos").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("recursos basicos").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('recursosbasicos.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

###############################################################################################
@app.route('/procesocritico', methods= ['POST', 'GET'])
def procesocritico():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("proceso critico").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("proceso critico").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("proceso critico").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("proceso critico").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('procesocritico.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

###############################################################################################
@app.route('/alineaciondelainformacion', methods= ['POST', 'GET'])
def alineaciondelainformacion():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    r3 = ''
    r4 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("alineacion de la informacion").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("alineacion de la informacion").child('r2').get().val()
    r3 = db.child(localId).child('MASTER').child("alineacion de la informacion").child('r3').get().val()
    r4 = db.child(localId).child('MASTER').child("alineacion de la informacion").child('r4').get().val()
    fecha = db.child(localId).child('MASTER').child("alineacion de la informacion").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if r3 is None:
        r3 = ''
    
    if r4 is None:
        r4 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')
        r3 = request.form.get('r3')
        r4 = request.form.get('r4')

        mcont = {
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "r4": r4,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("alineacion de la informacion").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('alineaciondelainformacion.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2,
    r3=r3, r4=r4)

###############################################################################################
@app.route('/visioncomunvalor', methods= ['POST', 'GET'])
def visioncomunvalor():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    r3 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("vision comun de valor").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("vision comun de valor").child('r2').get().val()
    r3 = db.child(localId).child('MASTER').child("vision comun de valor").child('r3').get().val()
    fecha = db.child(localId).child('MASTER').child("vision comun de valor").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if r3 is None:
        r3 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')
        r3 = request.form.get('r3')

        mcont = {
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("vision comun de valor").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('visioncomunvalor.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2,
    r3=r3)

###############################################################################################
@app.route('/liderazgoduenez', methods= ['POST', 'GET'])
def liderazgoduenez():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("liderazgo de duenez").child('r1').get().val()
    fecha = db.child(localId).child('MASTER').child("liderazgo de duenez").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')

        mcont = {
            "r1": r1,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("liderazgo de duenez").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('liderazgoduenez.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1)

###############################################################################################
@app.route('/gobernabilidadliderazgo', methods= ['POST', 'GET'])
def gobernabilidadliderazgo():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("gobernabilidad y liderazgo").child('r1').get().val()
    fecha = db.child(localId).child('MASTER').child("gobernabilidad y liderazgo").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')

        mcont = {
            "r1": r1,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("gobernabilidad y liderazgo").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('gobernabilidadliderazgo.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1)

###############################################################################################
@app.route('/nuestrosistemagobierno', methods= ['POST', 'GET'])
def nuestrosistemagobierno():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    r3 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("nuestro sistema de gobierno").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("nuestro sistema de gobierno").child('r2').get().val()
    r3 = db.child(localId).child('MASTER').child("nuestro sistema de gobierno").child('r3').get().val()
    fecha = db.child(localId).child('MASTER').child("nuestro sistema de gobierno").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if r3 is None:
        r3 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')
        r3 = request.form.get('r3')

        mcont = {
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("nuestro sistema de gobierno").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('nuestrosistemagobierno.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2,
    r3=r3)

###############################################################################################
@app.route('/entendimientoprofundonegocio', methods= ['POST', 'GET'])
def entendimientoprofundonegocio():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("entendimiento profundo de cada negocio").child('r1').get().val()
    fecha = db.child(localId).child('MASTER').child("entendimiento profundo de cada negocio").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')

        mcont = {
            "r1": r1,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("entendimiento profundo de cada negocio").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('entendimientoprofundonegocio.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1)

###############################################################################################
@app.route('/conceptoduenezvalores', methods= ['POST', 'GET'])
def conceptoduenezvalores():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("concepto de dueñez valores").child('r1').get().val()
    fecha = db.child(localId).child('MASTER').child("concepto de dueñez valores").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')

        mcont = {
            "r1": r1,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("concepto de dueñez valores").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('conceptoduenezvalores.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1)

###############################################################################################
@app.route('/competenciasmetamanagement', methods= ['POST', 'GET'])
def competenciasmetamanagement():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("competencias de metamanagement").child('r1').get().val()
    fecha = db.child(localId).child('MASTER').child("competencias de metamanagement").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')

        mcont = {
            "r1": r1,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("competencias de metamanagement").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('competenciasmetamanagement.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1)

###############################################################################################
@app.route('/capacidadesinstitucionalizacion', methods= ['POST', 'GET'])
def capacidadesinstitucionalizacion():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("capacidades de institucionalizacion").child('r1').get().val()
    fecha = db.child(localId).child('MASTER').child("capacidades de institucionalizacion").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')

        mcont = {
            "r1": r1,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("capacidades de institucionalizacion").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('capacidadesinstitucionalizacion.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1)

###############################################################################################
@app.route('/radararmonia2', methods= ['POST', 'GET'])
def radararmonia2():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("radar de armonia 2").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("radar de armonia 2").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("radar de armonia 2").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("radar de armonia 2").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('radararmonia2.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

###############################################################################################
@app.route('/radararmonia', methods= ['POST', 'GET'])
def radararmonia():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    
    nombre = db.child(localId).child('NAME').get().val()
    mcont = {}
    r1 = ''
    r2 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("radar de armonia").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("radar de armonia").child('r2').get().val()
    fecha = db.child(localId).child('MASTER').child("radar de armonia").child('fecha').get().val()
    
    if r1 is None:
        r1 = ''
    
    if r2 is None:
        r2 = ''

    if fecha is None:
        fecha = hoy
    else:
        fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')

        mcont = {
            "r1": r1,
            "r2": r2,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("radar de armonia").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('radararmonia.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2)

###############################################################################################



if __name__ == "__main__":
    app.run(threaded=True, debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))