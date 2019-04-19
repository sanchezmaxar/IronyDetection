import tensorflow as tf
from tensorflow.keras.preprocessing import sequence
from tensorflow.python.keras.layers import Input, LSTM, Bidirectional, Dense, Embedding, Dropout
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

def make_model(ModeloJson):
    
    tf.keras.backend.clear_session()
    model= tf.keras.models.model_from_json(open(ModeloJson).read())
    return model



def preprocessing(corpus,getVocabulary,n,vocabulario=None):
    twits=corpus
    
    cont=0
    # letras=[("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u")]
    cosas=[("\\n","\n"),("http://link","η"),("\\\"","\"")]
    twitsVectors=[]
    vocabularioBueno=["NTG","UNK"]
    dcont=1/len(twits)
    oraciones=[]
    for t in twits:
        # print("Llevo {0}".format(cont),end="\r")
        # t[1]=t[1].lower()
        
        tnGrams=[]
        for c,v in cosas:
            t[1]=t[1].replace(c,v)
        # tnGrams=t[1]
        original=t[1]
        vector=[] 
        t[1]="ŧ"+t[1]+"¶"
        for i in range(len(t[1])-(n-1)):
            tnGrams.append(t[1][i:i+n])        
            if getVocabulary:
                if tnGrams[-1] not in vocabularioBueno:
                    vocabularioBueno.append(tnGrams[-1])##Aqui va lo de los vectores
                vector.append(vocabularioBueno.index(tnGrams[-1]))
            else:
                if tnGrams[-1] not in vocabulario:
                    vector.append(vocabulario.index("UNK"))
                else:
                    vector.append(vocabulario.index(tnGrams[-1]))
        if(len(vector)==0):
            print(vector)
            print(original)
            input(t[1])
        twitsVectors.append((float(t[0]), vector))
        oraciones.append(tnGrams)
        cont+=dcont

    if getVocabulary:
        return np.array(twitsVectors,dtype=object),tnGrams,vocabularioBueno
    else:
        return np.array(twitsVectors,dtype=object),tnGrams


def evaluate(oracion,dic,inferencing_model,n,maxlen):
    print(oracion)
    tV,frase=preprocessing(oracion,False,n,dic)
    input(tV)
    x_test=[tV[0][1]]
    x_test = [x[::-1] for x in x_test]
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
    
    input(x_test.shape)
    y_pred=inferencing_model.predict(x_test)
    
    return frase,tV,y_pred

n=1
archPesos="/home/max/Documents/GitHubProjects/IronyDetection/Experimento2/Pesos/weights0_g1.hd5"
archVectores="/home/max/Documents/GitHubProjects/IronyDetection/Experimento2/Vocabularios/vocabulario0_g1.pkl"
modeloJson="/home/max/Documents/GitHubProjects/IronyDetection/Experimento2/Modelo.json"
dic1=pickle.load(open(archVectores,"rb"))
modelo1=make_model(modeloJson)
modelo1.load_weights(archPesos)

frase="Aunque Marvel Studios ya ha dicho por activa y por pasiva que no dará más información sobre el futuro del UCM hasta después del estreno de Vengadores: Endgame el próximo 26 de abril, las informaciones y rumores se suceden por […]"
print("Tu frase fue : ",evaluate([[0,frase]],dic1,modelo1,n,200))
# frase="ustedes deberían hacer un fic dónde suho es el líder de los nerdos y chanyeol el del equipo de la escuela, se unen bla bla bla y se aman¿"
# print("Tu frase fue : ",evaluate([[0,frase]],dic1,modelo1,n,200))
# frase="Igual igual vaya, parecen dos gotas de agua #ironia"
# print("Tu frase fue : ",evaluate([[0,frase]],dic1,modelo1,n,200))
# frase="Que ironía tener que escribir todo lo que no puedo decirte."
# print("Tu frase fue : ",evaluate([[0,frase]],dic1,modelo1,n,200))

# falsoNegativos=0
# falsoPositivos=0
# verdaderosNegativos=0
# verdaderosPositivos=0
# with open("/home/max/Documents/GitHubProjects/IronyDetection/Data/prueba.txt","r") as f:
#     l=f.read().splitlines()
#     for i,t in enumerate(l):
#         print("%i"%i,end="\r")
#         frase=t.split("|")
#         # print("Tu frase fue : %s "%evaluate([[0,sys.argv[1]]],dic,modelo))
#         aux=evaluate([[0,frase[1]]],dic1,modelo1,n,200)
#         aux=np.rint(aux)
#         if aux==1:
#             if int(frase[0])==1:
#                 verdaderosPositivos+=1
#             else:
#                 falsoPositivos+=1
#         else:
#             if int(frase[0])==1:
#                 falsoNegativos+=1
#             else:
#                 verdaderosNegativos+=1
# print("FN: %i"%falsoNegativos)
# print("FP: %i"%falsoPositivos)
# print("TN: %i"%verdaderosNegativos)
# print("TP: %i"%verdaderosPositivos)
# # modelo=make_model(max_features).load_weights(pesos)

# # print("Frase -> %s"%sys.argv[1])