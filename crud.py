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

co = "carlos@yahoo.com"

emails = []

for i in BD:
  eme = db.child(i.key()).child('EMAIL').get().val()
  emails.append(eme)

if co in emails:
  print("Si está")
else:
  print("no está")
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