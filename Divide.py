import sys
import random
from sklearn.model_selection import KFold

# ejemplo de uso
# python3 Divide.py corpus_complete_alan.txt Data/


def obtenerCorpuses(nombreArchivo, nombresBase):
    """Con esta función se crea 5 archivos con las  secciones del corpus
    INPUT:el nombre del corpus completo sin seccionar
    OUTPUT:si el proceso fue exitoso regresa los nombres de los archivos sino 0"""
    try:
        corpus = open(nombreArchivo, "r").readlines()
        random.shuffle(corpus, random.random)
        X = [x.split("|", 2)[2] for x in corpus]
        y = [y.split("|", 2)[1] for y in corpus]
        # X=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
        # y=np.array([20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1])
        print('El total del corpus es: ', len(X), ' twits')
        skf = KFold(n_splits=5)
        i = 0
        nombres = []
        for train, test in skf.split(X, y):
            # print("%s %s" % (train, test))
            f = open(nombresBase[0]+str(i)+".txt", "w")
            for idx in train:
                f.write(y[idx]+"|"+X[idx])
            f.close()
            f = open(nombresBase[1]+str(i)+".txt", "w")
            for idx in test:
                f.write(y[idx]+"|"+X[idx])
            nombres.append([nombresBase[0]+str(i)+".txt",
                            nombresBase[1]+str(i)+".txt"])
            i += 1
            f.close()

        return nombres
    except Exception as e:
        print("Ha ocurrido un problema: ", e)
        return 0


corpus = sys.argv[1]
base = sys.argv[2]
obtenerCorpuses(corpus, [base+"corpusTrain", base+"corpusTest"])
