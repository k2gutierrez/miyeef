from flask import Flask, render_template, request, redirect, url_for, session
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

BD = db.get()

hoy = date.today()

print(hoy)
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