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

emails = ['hola', 'adios', 'otro', 'prueba']

'''for i in BD:
  eme = db.child(i.key()).child('EMAIL').get().val()
  emails.append(eme)

if co in emails:
  print("Si está")
else:
  print("no está")'''

mc = db.child('oweTEae2NsN5e0g9vo1bb8fRK5M2').child('MASTER').child("impulsores e inhibidores de valor").child('impulsores').get().val()
md = db.child('oweTEae2NsN5e0g9vo1bb8fRK5M2').child('MASTER').child("impulsores e inhibidores de valor").child('inhibidores').get().val()



print(mc.get('imp1'))
