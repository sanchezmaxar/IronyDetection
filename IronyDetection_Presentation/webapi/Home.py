from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
# from Predict import *
import json
import requests
from tensorflow.keras.preprocessing import sequence
app = Flask(__name__)
cors = CORS(app, resources={r"/postjson": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

#primero se debe ejecutar esta linea
# source IronyDetection_Presentation/webapi/bin/activate
# despues este 
# tensorflow_model_server  --rest_api_port=8501 --model_config_file=IronyDetection_Presentation/webapi/tensorflowServerconf.conf
# Despues se debe usar este comando en otra consola
# python3 IronyDetection_Presentation/webapi/Home.py 
# Comprobando el estado del api
#  curl http://localhost:8501/v1/models/Experimento1 

@app.route('/postjson', methods=['POST', 'OPTIONS'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def postJsonHandler():
    # print(request.is_json)
    content = request.get_json()
    # print(content)
    # print(content['cadena'])
    n=int(content['n'])
    oracion=content['cadena']
    preprocess=preps[n]
    maxlen=int(content['maxlen'])
    tV,frase=preprocess(oracion,dics[n],n)
    x_test=tV
    x_test =  [x_test[::-1]]
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
    # input(x_test[0].shape) 

    payload = {
        "inputs": x_test.tolist()
    }

    # sending post request to TensorFlow Serving server
    r = requests.post('http://localhost:8501/v1/models/Experimento%i:predict'%(n+1), json=payload)
    pred = json.loads(r.content.decode('utf-8'))
    # input(pred)
    return  json.dumps({
        'frase':frase,
        'vector':x_test.tolist(),
        'pred':pred
    })




## Aqui empieza el desastre del backend

import pickle
import re
import numpy as np
from unicodedata import normalize
import math
# import ptvsd
# # Allow other computers to attach to ptvsd at this IP address and port.
# ptvsd.enable_attach(address=('127.0.0.1', 5678), redirect_output=True)

# # Pause the program until a remote debugger is attached
# ptvsd.wait_for_attach()

def preprocessing(twit,vocabulario,n):   
    cosas=[("\\n","\n"),("http://link","η"),("\\\"","\"")]
    # print(vocabulario)
    tnGrams=[]
    for c,v in cosas:
        twit=twit.replace(c,v)
    twit="ŧ"+twit+"¶"
    vector=[]
    for i in range(len(twit)-(n-1)):
        tnGrams.append(twit[i:i+n])        
        if tnGrams[-1] not in vocabulario:
            vector.append(vocabulario.index("UNK"))
        else:
            vector.append(vocabulario.index(tnGrams[-1]))
    return vector,tnGrams

def noCaracteresEspeciales(texto):
	# -> NFD y eliminar diacríticos
	texto = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
        normalize("NFD", texto), 0, re.I
    )

	# -> NFC
	return re.sub('\W', ' ', texto).lower()

def convertirAVector(oracion,dic,n=0):
	vector=[]
	texto=noCaracteresEspeciales(oracion).split()
	texto = ["ŧ"]+texto+["¶"]
	for t in texto:
		try:
			vector.append(dic.index(t))
		except:
			vector.append(dic.index("UNK"))
	return vector,texto

vocabPalabras="/home/max/Documents/GitHubProjects/IronyDetection/Experimento1/Vocabularios/vocabulario4_palabras.pkl"
vocabn1="/home/max/Documents/GitHubProjects/IronyDetection/Experimento2/Vocabularios/vocabulario0_g1.pkl"
vocabn2="/home/max/Documents/GitHubProjects/IronyDetection/Experimento3/Vocabularios/vocabulario4_g2.pkl"
vocabn3="/home/max/Documents/GitHubProjects/IronyDetection/Experimento4/Vocabularios/vocabulario0_g3.pkl"

dics={
    0:pickle.load(open(vocabPalabras,"rb")),
    1:pickle.load(open(vocabn1,"rb")),
    2:pickle.load(open(vocabn2,"rb")),
    3:pickle.load(open(vocabn3,"rb"))
}

preps={
    0:convertirAVector,
    1:preprocessing,
    2:preprocessing,
    3:preprocessing
}

app.run(host='0.0.0.0', port=8090)