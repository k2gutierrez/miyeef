from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase
import os
from datetime import date
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

BD = db.get()

'''
cliente = db.child("8L7kQVOg5CgPmFiYbADTMK5Edhb2").child('dolencias').child('lista total').get().val()

listo = db.child('dolencias').get().val()

DB = db.get().val()'''

'''for i in listo:
  a = i.get('lastre')
  if 'Desenfoque' in a:
    b = i.get('dolencia')
    print(b)'''
'''
nivel = db.child(i.key()).child('NAME').get().val()

for user in DB:
  db.child(user.key()).child()
  if 'cgutierrez@cedem.com.mx' in a:
    n = a.get('NAME')
    print(str(n))'''
localId = "oweTEae2NsN5e0g9vo1bb8fRK5M2"
sele = "programar blockchain"
fecha = db.child(localId).child('MASTER').child("proyecto detonador").child(sele).child('fecha').get().val()
lider = db.child(localId).child('MASTER').child("proyecto detonador").child(sele).child('lider').get().val()
equipo = db.child(localId).child('MASTER').child("proyecto detonador").child(sele).child('equipo').get().val()
proyecto = db.child(localId).child('MASTER').child("proyecto detonador").child(sele).child('proyecto').get().val()
plan = db.child(localId).child('MASTER').child("proyecto detonador").child(sele).child('plan').get().val()
cumplimiento = db.child(localId).child('MASTER').child("proyecto detonador").child(sele).child('cumplimiento').get().val()

print(lider)