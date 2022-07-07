from flask import Flask, render_template, request, redirect, url_for, session, Response
import pyrebase
import os
from datetime import date
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import config

plt.rcParams["figure.figsize"] = [7.50, 7.50]
plt.rcParams["figure.autolayout"] = True

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
    nombre = str(db.child(localId).child('NAME').get().val())
    a = nombre.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
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
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
    mcont = {}
    r1 = ''
    r2 = ''
    r3 = ''
    r4 = ''
    r5 = ''
    r6 = ''
    r7 = ''
    r8 = ''
    mensaje = ''
    hoy = date.today()
    fig = None

    r1 = db.child(localId).child('MASTER').child("radar de armonia").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("radar de armonia").child('r2').get().val()
    r3 = db.child(localId).child('MASTER').child("radar de armonia").child('r3').get().val()
    r4 = db.child(localId).child('MASTER').child("radar de armonia").child('r4').get().val()
    r5 = db.child(localId).child('MASTER').child("radar de armonia").child('r5').get().val()
    r6 = db.child(localId).child('MASTER').child("radar de armonia").child('r6').get().val()
    r7 = db.child(localId).child('MASTER').child("radar de armonia").child('r7').get().val()
    r8 = db.child(localId).child('MASTER').child("radar de armonia").child('r8').get().val()
    fecha = db.child(localId).child('MASTER').child("radar de armonia").child('fecha').get().val()
    
    if r1 is None:
        r1 = 0
    
    if r2 is None:
        r2 = 0
    
    if r3 is None:
        r3 = 0
    
    if r4 is None:
        r4 = 0

    if r5 is None:
        r5 = 0
    
    if r6 is None:
        r6 = 0

    if r7 is None:
        r7 = 0
    
    if r8 is None:
        r8 = 0

    if fecha is None:
        fecha = hoy
    else:
        fecha

    #Chart#
    data = [
        ['Querencia Familiar-Empresarial', r1],
        ['Actitudes Fundamentales', r2],
        ['Calidad de Diálogo', r3],
        ['Manejo de Conflictos', r4],
        ['Gobernabilidad', r5],
        ['Cultura y Reglas Familiares', r6],
        ['Sucesión', r7],
        ['Herencia', r8]
        ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')
        r3 = request.form.get('r3')
        r4 = request.form.get('r4')
        r5 = request.form.get('r5')
        r6 = request.form.get('r6')
        r7 = request.form.get('r7')
        r8 = request.form.get('r8')

        mcont = {
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "r4": r4,
            "r5": r5,
            "r6": r6,
            "r7": r7,
            "r8": r8,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("radar de armonia").set(mcont)
        mc
        r1
        r2
        r3
        r4
        r5
        r6
        r7
        r8
        data = [
            ['Querencia Familiar-Empresarial', r1],
            ['Actitudes Fundamentales', r2],
            ['Calidad de Diálogo', r3],
            ['Manejo de Conflictos', r4],
            ['Gobernabilidad', r5],
            ['Cultura y Reglas Familiares', r6],
            ['Sucesión', r7],
            ['Herencia', r8]
            ]
        labels = [row[0] for row in data]
        values = [row[1] for row in data]
        mensaje = 'Los registros han quedado guardados'

    return render_template('radararmonia.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2, 
    r3=r3, r4=r4, r5=r5, r6=r6, r7=r7, r8=r8, labels=labels, values=values)

###############################################################################################
@app.route('/sucesion', methods= ['POST', 'GET'])
def sucesion():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
    mcont = {}
    r1 = ''
    r2 = ''
    r3 = ''
    r4 = ''
    r5 = ''
    r6 = ''
    r7 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("sucesion").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("sucesion").child('r2').get().val()
    r3 = db.child(localId).child('MASTER').child("sucesion").child('r3').get().val()
    r4 = db.child(localId).child('MASTER').child("sucesion").child('r4').get().val()
    r5 = db.child(localId).child('MASTER').child("sucesion").child('r5').get().val()
    r6 = db.child(localId).child('MASTER').child("sucesion").child('r6').get().val()
    r7 = db.child(localId).child('MASTER').child("sucesion").child('r7').get().val()
    fecha = db.child(localId).child('MASTER').child("sucesion").child('fecha').get().val()
    
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

    if r7 is None:
        r7 = ''

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
        r7 = request.form.get('r7')

        mcont = {
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "r4": r4,
            "r5": r5,
            "r6": r6,
            "r7": r7,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("sucesion").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('sucesion.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2, 
    r3=r3, r4=r4, r5=r5, r6=r6, r7=r7)

###############################################################################################
@app.route('/diagnosticointernacionalizacion', methods= ['POST', 'GET'])
def diagnosticointernacionalizacion():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
    mcont = {}
    r1 = ''
    r2 = ''
    r3 = ''
    r4 = ''
    r5 = ''
    r6 = ''
    r7 = ''
    r8 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("diagnostico del proceso de internacionalizacion").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("diagnostico del proceso de internacionalizacion").child('r2').get().val()
    r3 = db.child(localId).child('MASTER').child("diagnostico del proceso de internacionalizacion").child('r3').get().val()
    r4 = db.child(localId).child('MASTER').child("diagnostico del proceso de internacionalizacion").child('r4').get().val()
    r5 = db.child(localId).child('MASTER').child("diagnostico del proceso de internacionalizacion").child('r5').get().val()
    r6 = db.child(localId).child('MASTER').child("diagnostico del proceso de internacionalizacion").child('r6').get().val()
    r7 = db.child(localId).child('MASTER').child("diagnostico del proceso de internacionalizacion").child('r7').get().val()
    r8 = db.child(localId).child('MASTER').child("diagnostico del proceso de internacionalizacion").child('r8').get().val()
    fecha = db.child(localId).child('MASTER').child("diagnostico del proceso de internacionalizacion").child('fecha').get().val()
    
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

    if r7 is None:
        r7 = ''

    if r8 is None:
        r8 = ''

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
        r7 = request.form.get('r7')
        r8 = request.form.get('r8')

        mcont = {
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "r4": r4,
            "r5": r5,
            "r6": r6,
            "r7": r7,
            "r8": r8,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("diagnostico del proceso de internacionalizacion").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('diagnosticointernacionalizacion.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2, 
    r3=r3, r4=r4, r5=r5, r6=r6, r7=r7, r8=r8)

###############################################################################################
@app.route('/mapaformulanegocio', methods= ['POST', 'GET'])
def mapaformulanegocio():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
    mcont = {}
    r1 = ''
    r2 = ''
    r3 = ''
    r4 = ''
    r5 = ''
    r6 = ''
    r7 = ''
    r8 = ''
    r9 = ''
    r10 = ''
    r11 = ''
    r12 = ''
    r13 = ''
    mensaje = ''
    hoy = date.today()

    r1 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r2').get().val()
    r3 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r3').get().val()
    r4 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r4').get().val()
    r5 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r5').get().val()
    r6 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r6').get().val()
    r7 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r7').get().val()
    r8 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r8').get().val()
    r9 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r9').get().val()
    r10 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r10').get().val()
    r11 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r11').get().val()
    r12 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r12').get().val()
    r13 = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('r13').get().val()
    fecha = db.child(localId).child('MASTER').child("mapa de la formula de negocio").child('fecha').get().val()
    
    if r1 is None: r1 = ''
    if r2 is None: r2 = ''
    if r3 is None: r3 = '' 
    if r4 is None: r4 = ''
    if r5 is None: r5 = '' 
    if r6 is None: r6 = ''
    if r7 is None: r7 = ''
    if r8 is None: r8 = ''
    if r9 is None: r9 = ''
    if r10 is None: r10 = ''
    if r11 is None: r11 = ''
    if r12 is None: r12 = ''
    if r13 is None: r13 = ''

    if fecha is None: fecha = hoy 
    else: fecha

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')
        r3 = request.form.get('r3')
        r4 = request.form.get('r4')
        r5 = request.form.get('r5')
        r6 = request.form.get('r6')
        r7 = request.form.get('r7')
        r8 = request.form.get('r8')
        r9 = request.form.get('r9')
        r10 = request.form.get('r10')
        r11 = request.form.get('r11')
        r12 = request.form.get('r12')
        r13 = request.form.get('r13')

        mcont = {
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "r4": r4,
            "r5": r5,
            "r6": r6,
            "r7": r7,
            "r8": r8,
            "r9": r9,
            "r10": r10,
            "r11": r11,
            "r12": r12,
            "r13": r13,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("mapa de la formula de negocio").set(mcont)
        mc
        mensaje = 'Los registros han quedado guardados'

    return render_template('mapaformulanegocio.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1=r1, r2=r2, 
    r3=r3, r4=r4, r5=r5, r6=r6, r7=r7, r8=r8, r9=r9, r10=r10, r11=r11, r12=r12, r13=r13)

###############################################################################################
@app.route('/evaluandoduenezcompartida', methods= ['POST', 'GET'])
def evaluandoduenezcompartida():

    token = session['user']
    user = auth.get_account_info(token)
    localId = user['users'][0]['localId']
    n = str(db.child(localId).child('NAME').get().val())
    nombre = n.title()
    mcont = {}
    r11 = ''
    mensaje = ''
    hoy = date.today()
    sele = 'checked'
    nosele = 'unchecked'

    r1a = nosele
    r1b = nosele
    r1c = nosele
     
    r2a = nosele
    r2b = nosele
    r2c = nosele
     
    r3a = nosele
    r3b = nosele
    r3c = nosele
     
    r4a = nosele
    r4b = nosele
    r4c = nosele
    
    r5a = nosele
    r5b = nosele
    r5c = nosele
     
    r6a = nosele
    r6b = nosele
    r6c = nosele
     
    r7a = nosele
    r7b = nosele
    r7c = nosele

    r8a = nosele
    r8b = nosele
    r8c = nosele

    r9a = nosele
    r9b = nosele
    r9c = nosele

    r10a = nosele
    r10b = nosele
    r10c = nosele

    r1 = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('r1').get().val()
    r2 = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('r2').get().val()
    r3 = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('r3').get().val()
    r4 = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('r4').get().val()
    r5 = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('r5').get().val()
    r6 = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('r6').get().val()
    r7 = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('r7').get().val()
    r8 = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('r8').get().val()
    r9 = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('r9').get().val()
    r10 = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('r10').get().val()
    r11 = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('r11').get().val()
    fecha = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").child('fecha').get().val()
    
    if r11 is None: r11 = ''

    if fecha is None: fecha = hoy 
    else: fecha

    if r1 == 'SI': r1a = sele
    elif r1 == 'NO': r1b = sele
    elif r1 == '?': r1c = sele

    if r2 == 'SI': r2a = sele
    elif r2 == 'NO': r2b = sele
    elif r2 == '?': r2c = sele

    if r3 == 'SI': r3a = sele
    elif r3 == 'NO': r3b = sele
    elif r3 == '?': r3c = sele

    if r4 == 'SI': r4a = sele
    elif r4 == 'NO': r4b = sele
    elif r4 == '?': r4c = sele

    if r5 == 'SI': r5a = sele
    elif r5 == 'NO': r5b = sele
    elif r5 == '?': r5c = sele

    if r6 == 'SI': r6a = sele
    elif r6 == 'NO': r6b = sele
    elif r6 == '?': r6c = sele

    if r7 == 'SI': r7a = sele
    elif r7 == 'NO': r7b = sele
    elif r7 == '?': r7c = sele

    if r8 == 'SI': r8a = sele
    elif r8 == 'NO': r8b = sele
    elif r8 == '?': r8c = sele

    if r9 == 'SI': r9a = sele
    elif r9 == 'NO': r9b = sele
    elif r9 == '?': r9c = sele
    
    if r10 == 'SI': r10a = sele
    elif r10 == 'NO': r10b = sele
    elif r10 == '?': r10c = sele

    if request.method == 'POST':
        r1 = request.form.get('r1')
        r2 = request.form.get('r2')
        r3 = request.form.get('r3')
        r4 = request.form.get('r4')
        r5 = request.form.get('r5')
        r6 = request.form.get('r6')
        r7 = request.form.get('r7')
        r8 = request.form.get('r8')
        r9 = request.form.get('r9')
        r10 = request.form.get('r10')
        r11 = request.form.get('r11')

        mcont = {
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "r4": r4,
            "r5": r5,
            "r6": r6,
            "r7": r7,
            "r8": r8,
            "r9": r9,
            "r10": r10,
            "r11": r11,
            "fecha": str(hoy)
        }
        
        mc = db.child(localId).child('MASTER').child("evaluando la dueñez compartida").set(mcont)
        mc
        if r1 == 'SI': r1a = sele
        elif r1 == 'NO': r1b = sele
        elif r1 == '?': r1c = sele

        if r2 == 'SI': r2a = sele
        elif r2 == 'NO': r2b = sele
        elif r2 == '?': r2c = sele

        if r3 == 'SI': r3a = sele
        elif r3 == 'NO': r3b = sele
        elif r3 == '?': r3c = sele

        if r4 == 'SI': r4a = sele
        elif r4 == 'NO': r4b = sele
        elif r4 == '?': r4c = sele

        if r5 == 'SI': r5a = sele
        elif r5 == 'NO': r5b = sele
        elif r5 == '?': r5c = sele

        if r6 == 'SI': r6a = sele
        elif r6 == 'NO': r6b = sele
        elif r6 == '?': r6c = sele

        if r7 == 'SI': r7a = sele
        elif r7 == 'NO': r7b = sele
        elif r7 == '?': r7c = sele

        if r8 == 'SI': r8a = sele
        elif r8 == 'NO': r8b = sele
        elif r8 == '?': r8c = sele

        if r9 == 'SI': r9a = sele
        elif r9 == 'NO': r9b = sele
        elif r9 == '?': r9c = sele
        
        if r10 == 'SI': r10a = sele
        elif r10 == 'NO': r10b = sele
        elif r10 == '?': r10c = sele
        mensaje = 'Los registros han quedado guardados'

    return render_template('evaluandoduenezcompartida.html', mcont=mcont, mensaje=mensaje, nombre=nombre, fecha=fecha, r1a=r1a, 
    r1b=r1b, r1c=r1c, r2a=r2a, r2b=r2b, r2c=r2c, r3a=r3a, r3b=r3b, r3c=r3c, r4a=r4a, r4b=r4b, r4c=r4c, r5a=r5a, r5b=r5b, r5c=r5c, 
    r6a=r6a, r6b=r6b, r6c=r6c, r7a=r7a, r7b=r7b, r7c=r7c, r8a=r8a, r8b=r8b, r8c=r8c, r9a=r9a, r9b=r9b, r9c=r9c, r10a=r10a, r10b=r10b, 
    r10c=r10c, r11=r11)

###############################################################################################



if __name__ == "__main__":
    app.run(threaded=True, debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))