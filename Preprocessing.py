# import nltk
from string import punctuation
import pickle
# from nltk.tokenize import TweetTokenizer,word_tokenize
# nltk.download("stopwords")
# from nltk.corpus import stopwords
# from nltk.stem import SnowballStemmer
import numpy as np
# import itertools
import emoji
import math
# #" & ".join(["%.4f"%(sum([i[n] for i in a])/5) for n in range(4)])

# import ptvsd
# # Allow other computers to attach to ptvsd at this IP address and port.
# ptvsd.enable_attach(address=('127.0.0.1', 5678), redirect_output=True)

# # Pause the program until a remote debugger is attached
# ptvsd.wait_for_attach()

# ejemplo de uso
# python3 Preprocessing.py 1 Data/ Experimento2/ 300 0 5


def preprocessing(corpus,getVocabulary,lenPad,vocabulario=None):
    twits=[]
    with open(corpus,"r") as f:
        docs=f.read().splitlines()
        twits=[d.split("|",2) for d in docs]
    cont=0
    # letras=[("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u")]
    cosas=[("\\n","\n"),("http://link","η"),("\\\"","\"")]
    twitsVectors=[]
    vocabularioBueno=["NTG","UNK"]
    dcont=1/len(twits)
    for t in twits:
        print("Llevo {0}".format(cont),end="\r")
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

        # input(tnGrams)
        # if getVocabulary:
        #     vector.append(vocabularioBueno.index("¶")) #simbolo de fin de línea
        #     # falta=math.ceil((lenPad-len(vector))/2)
        #     # vector=[vocabularioBueno.index("NTG")]*falta+vector+[vocabularioBueno.index("NTG")]*falta
        #     # vector=vector[:lenPad]
        # else:
        #     vector.append(vocabulario.index("¶")) #simbolo de fin de línea
            # falta=math.ceil((lenPad-len(vector))/2)
            # vector=[vocabulario.index("NTG")]*falta+vector+[vocabulario.index("NTG")]*falta
            # vector=vector[:lenPad]
        # vector= np.array((vector*(math.ceil(lenPad/len(vector))))[:lenPad],dtype=np.float32)
        
        # input(vector)
        if(len(vector)==0):
            print(vector)
            print(original)
            input(t[1])
        twitsVectors.append((float(t[0]), vector))
        # input(twitsVectors[-1])
        cont+=dcont

    if getVocabulary:
        return np.array(twitsVectors,dtype=object),vocabularioBueno
    else:
        return np.array(twitsVectors,dtype=object)

# def SplitHash(hashTag):
#     salida=[""]
#     contM=0
#     contm=0
#     for c in hashTag:
#         if c.isupper():
#             if salida[-1]!="" :
#                 salida.append(c)
#             else:
#                 salida[-1]+=c
#             contM+=1
#         else:
#             salida[-1]+=c
#             contm+=1
#     if contM==len(hashTag) or contm==len(hashTag) or sum([1 for i in salida if len(i)==1])>len(salida)*0.5:
#         return [hashTag]
#     else:
#         return salida

# def wordVect2Vect(twits,vocabulario,lenPad):
#     vectores=[]
#     cont=0
#     dcont=1/len(twits)
#     for t in twits:
#         vAux=[]
#         print("Llevo ",cont,end="\r")
#         # input(t)
#         for p in t[1]:
#             if p in vocabulario:
#                 vAux.append(vocabulario.index(p))
#             else:
#                 vAux.append(vocabulario.index("UNK"))
        
#         vAux=(vAux*(math.ceil(lenPad/len(vAux))))[:lenPad]
        
#         vectores.append([t[0],vAux])
#         # input(vectores[-1])
#         cont+=dcont
#     return vectores    

def getVectors(archivoEntr,archivoPrue,archivoSalpickle,vocabularioF,lenPad):
    print("Inicia el preprocesamiento de {0} y {1}".format(archivoEntr,archivoPrue))
    twitsTrain,vocabulario=preprocessing(archivoEntr,True,lenPad)
    pickle.dump(vocabulario,open(vocabularioF,"wb"))
    print("Termine de encontrar el vocab y preprocessar el entrenamiento")
    twitsTest=preprocessing(archivoPrue,False,lenPad,vocabulario)    
    print("\nGuardando\n")
    pickle.dump([(twitsTrain[:,1],twitsTrain[:,0]),(twitsTest[:,1],twitsTest[:,0])],open(archivoSalpickle,"wb"))
import sys 

n=int(sys.argv[1])
baseData=sys.argv[2]
base=sys.argv[3]
lenPad=int(sys.argv[4])
rango1=int(sys.argv[5])
rango2=int(sys.argv[6])
lista=[[baseData+"corpusTrain%i.txt"%i,
baseData+"corpusTest%i.txt"%(i),
base+"vectoresSet%i_g%i.pkl"%(i,n),
base+"vocabulario%i_g%i.pkl"%(i,n)] for i in range(rango1,rango2)
    ]
print("Procesaré:\n"+"\n".join([" ".join(l) for l in lista]))
aceptar=input("Aceptar(Y/n):")
if(aceptar=="Y" or aceptar=="y" or aceptar==""):
    pass
else:
    exit()
for docs in lista:
    print("Preprocesando {0},{1},{2},{3}".format(docs[0],docs[1],docs[2],docs[3]))
    getVectors(docs[0],docs[1],docs[2],docs[3],lenPad)
print("Termine todo.")
