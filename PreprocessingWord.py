from sklearn.metrics import accuracy_score,confusion_matrix,recall_score,precision_score,f1_score
from unicodedata import normalize
import numpy as np
import re
import sys
import pickle

# ejemplo de uso
# python3 PreprocessingWord.py Data/ Experimento1/

def noCaracteresEspeciales(texto):
	# -> NFD y eliminar diacríticos
	texto = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", texto), 0, re.I
    )

	# -> NFC
	return re.sub('\W',' ',texto).lower()

def crearVocabulario(archCorpus,umbral):
	"""Con esta función creamos el vocabulario a partir del archCorpus
	INPUT: archCorpus- nombre del archivo con el corpus, 
		umbral- numero de apariciones minima para considerarlas relevantes
	OUTPUT: el vocabulario"""
	corpus=open(archCorpus,"r").readlines()
	vocabulario={"UNK":0}
	for twit in corpus:
		twitSplit=noCaracteresEspeciales(twit)
		for palabra in twitSplit.split():
			if palabra!="http://link":
				if palabra not in vocabulario:
					vocabulario[palabra]=1
				else:
					vocabulario[palabra]+=1
	ignorados=0
	for palabra in list(vocabulario):
		if vocabulario[palabra]<umbral:
			vocabulario["UNK"]+=1
			vocabulario.pop(palabra)
			ignorados+=1
	print("ignore ",ignorados," palabras")
	return vocabulario

def convertirAVector(oracion,dic):
	vector=[]
	texto=noCaracteresEspeciales(oracion).split()
	for t in texto:
		try:
			vector.append(dic.index(t))
		except:
			vector.append(dic.index("UNK"))
	return vector


def corpusAVectores(corpuses,vocabulario,separacion):
	# try:
	dic=list(vocabulario.keys())
	# print(corpuses)
	with open(corpuses[0],"r") as f:
		c=f.readlines()
		vect_train=np.array(list(map(lambda x:(int(x[0]),convertirAVector(x[1],dic)),[i.split(separacion,1) for i in c ])),dtype=object)
	with open(corpuses[1],"r") as f:
		c=f.readlines()
		vect_test=np.array(list(map(lambda x:(int(x[0]),convertirAVector(x[1],dic)),[i.split(separacion,1) for i in c ])),dtype=object)
		# print(vect_test)
	return [(vect_train[:,1],vect_train[:,0]),(vect_test[:,1],vect_test[:,0])]
	# pickle.dump([(vect_train[:,1],vect_train[:,0]),(vect_test[:,1],vect_test[:,0]),dic],open(archivoPickle,"wb"))

	
	# except Exception as e:
	# 	print("Ha ocurrido un error: ",e)
	# 	return 0

def getVectors(archivoEntr,archivoPrue,archivoSalpickle,vocabularioF):
	vocabulario=crearVocabulario(
		archivoEntr #el corpus de entrenamiento
		,5 #umbral a partir de cuantas apariciones se considera relevante
		)
	pickle.dump(vocabulario,open(vocabularioF,"wb"))
	print("Inicia el preprocesamiento de {0} y {1}".format(archivoEntr,archivoPrue))
	vectores=corpusAVectores([archivoEntr,archivoPrue],vocabulario,"|")
	pickle.dump(vectores,open(archivoSalpickle,"wb"))
	print("Guardando")
baseData=sys.argv[1]
base=sys.argv[2]
lista=[[baseData+"corpusTrain%i.txt"%i,
baseData+"corpusTest%i.txt"%(i),
base+"vectoresSet%i_palabras.pkl"%(i),
base+"vocabulario%i_palabras.pkl"%(i)] for i in range(5)
]
for docs in lista:
    print("Preprocesando {0},{1},{2}".format(docs[0],docs[1],docs[2],docs[3]))
    getVectors(docs[0],docs[1],docs[2],docs[3])
print("Termine todo.")