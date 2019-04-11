import nltk
from string import punctuation
import pickle
from nltk.tokenize import TweetTokenizer,word_tokenize
# nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import itertools
import emoji

# #" & ".join(["%.4f"%(sum([i[n] for i in a])/5) for n in range(4)])

# import ptvsd
# # Allow other computers to attach to ptvsd at this IP address and port.
# ptvsd.enable_attach(address=('127.0.0.1', 5678), redirect_output=True)

# # Pause the program until a remote debugger is attached
# ptvsd.wait_for_attach()

# ejemplo de uso
# python3 Preprocessing.py 1 Data/ Experimento2/


def preprocessing(corpus,getVocabulary):
    twits=[]
    with open(corpus,"r") as f:
        docs=f.read().splitlines()
        twits=[d.split("|",2) for d in docs]
    cont=0
    # letras=[("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u")]
    cosas=[("\\n","\n"),("http://link","η"),("\\\"","\"")]
    twitsVectors=[]
    vocabularioBueno=["UNK"]
    dcont=1/len(twits)
    for t in twits:
        print("Llevo {0}".format(cont),end="\r")
        # t[1]=t[1].lower()
        tnGrams=[]
        for c,v in cosas:
            t[1]=t[1].replace(c,v)
        # tnGrams=t[1]
        for i in range(len(t[1])-(n-1)):
            tnGrams.append(t[1][i:i+n])        
            if getVocabulary:
                if tnGrams[-1] not in vocabularioBueno:
                    vocabularioBueno.append(tnGrams[-1])##Aqui va lo de los vectores
        # input(tnGrams)
        
        twitsVectors.append([int(t[0]), list(tnGrams)])
        # input(twitsVectors[-1])
        cont+=dcont

    if getVocabulary:
        return twitsVectors,vocabularioBueno
    else:
        return twitsVectors

def SplitHash(hashTag):
    salida=[""]
    contM=0
    contm=0
    for c in hashTag:
        if c.isupper():
            if salida[-1]!="" :
                salida.append(c)
            else:
                salida[-1]+=c
            contM+=1
        else:
            salida[-1]+=c
            contm+=1
    if contM==len(hashTag) or contm==len(hashTag) or sum([1 for i in salida if len(i)==1])>len(salida)*0.5:
        return [hashTag]
    else:
        return salida

def wordVect2Vect(twits,vocabulario):
    vectores=[]
    cont=0
    dcont=1/len(twits)
    for t in twits:
        vAux=[]
        print("Llevo ",cont,end="\r")
        # input(t)
        for p in t[1]:
            if p in vocabulario:
                vAux.append(vocabulario.index(p))
            else:
                vAux.append(vocabulario.index("UNK"))
        vectores.append([t[0],vAux])
        # input(vectores[-1])
        cont+=dcont
    return vectores    

def getVectors(archivoEntr,archivoPrue,archivoSalpickle,vocabularioF):
    print("Inicia el preprocesamiento de {0} y {1}".format(archivoEntr,archivoPrue))
    twitsTrain,vocabulario=preprocessing(archivoEntr,True)
    pickle.dump(vocabulario,open(vocabularioF,"wb"))
    print("Termine de encontrar el vocab y preprocessar el entrenamiento")
    twitsTest=preprocessing(archivoPrue,False)
    print("Termine de preprocesar la prueba")
    vectoresTrain=(wordVect2Vect(twitsTrain,vocabulario))
    print("Termine de encontrar los vectores de entrenamiento")
    vectoresTest=(wordVect2Vect(twitsTest,vocabulario))
    print("Termine de encontrar los vectores de prueba")

    print("Guardando")

    vTrx=[]
    vTry=[]
    vTsx=[]
    vTsy=[]
    for v in vectoresTrain:
        vTry.append(v[0])
        vTrx.append(v[1])
    for v in vectoresTest:
        vTsy.append(v[0])
        vTsx.append(v[1])
    pickle.dump([(vTrx,vTry),(vTsx,vTsy)],open(archivoSalpickle,"wb"))
import sys 

n=int(sys.argv[1])
baseData=sys.argv[2]
base=sys.argv[3]
lista=[[baseData+"corpusTrain%i.txt"%i,
baseData+"corpusTest%i.txt"%(i),
base+"vectoresSet%i_g%i.pkl"%(i,n),
base+"vocabulario%i_g%i.pkl"%(i,n)] for i in range(5)
    ]

for docs in lista:
    print("Preprocesando {0},{1},{2},{3}".format(docs[0],docs[1],docs[2],docs[3]))
    getVectors(docs[0],docs[1],docs[2],docs[3])
print("Termine todo.")
