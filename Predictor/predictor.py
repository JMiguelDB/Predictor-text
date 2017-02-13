import re

#elimina del texto caracteres extraños
def reemplaza(archivo):
    patron = re.compile('\d+')
    archivo = archivo.replace(',','')
    archivo = archivo.replace('*','')
    archivo = archivo.replace('?','')
    archivo = archivo.replace('¿','')
    archivo = archivo.replace('!','')
    archivo = archivo.replace('¡','')
    archivo = archivo.replace('á','a')
    archivo = archivo.replace('é','e')
    archivo = archivo.replace('í','i')
    archivo = archivo.replace('ó','o')
    archivo = archivo.replace('ú','u')
    archivo = archivo.replace('.','')
    archivo = archivo.replace('-',' ')
    archivo = archivo.replace('_',' ')    
    archivo = archivo.replace(':',' ')
    archivo = archivo.replace(';',' ')
    archivo = archivo.replace(']','')
    archivo = archivo.replace('[','')
    archivo = archivo.replace('(','')
    archivo = archivo.replace(')','')
    #archivo = archivo.replace(patron,'')    
    archivo = patron.sub('',archivo)    
    return archivo.lower()

#codifica la cadena de numeros para elegir la letra más frecuente
def descomprime(l):
    l = str(l)
    if not l:
        return l
    else:
        prev=l[0]
        cont=1
        res=[]
        for x in l[1:]:
            if x == prev:
                cont+=1
            else:
                res.append([cont,prev] if cont>1 else prev)
                cont = 1
                prev = x
        res.append([cont,prev] if cont>1 else prev)
        return res
        
#Genera el numero correspondiente a la palabra       
def codificaPalabra(palabra,teclado):
    numeros = ""
    for letra in palabra:
        for tecla in teclado:
            for caracter in teclado[tecla]:
                if caracter == letra:
                    numeros += str(tecla)
    return numeros
    
#Lee el archivo y le aplica las operaciones para obtener las palabras planas
def readWords(file1):
    text = open(file1,encoding = 'utf8')
    readW = text.read()
    readW.lower()    
    readW = reemplaza(readW)    
    return readW    

#Unigram de letras
def unigramLetras(archivo):
    a = 0
    diccionario = {}    
    patron2 = re.compile("\w")
    total = (len(patron2.findall(archivo)))        
    for i in "abcdefghijklmnñopqrstuvwxyz":
        patron = re.compile(i)            
        a += len(patron.findall(archivo))        
        diccionario[i]=(len(patron.findall(archivo))/total)
    return (diccionario)

#Bigram de letras
def bigramLetras(archivo):
    a = 0
    diccionario = {}        
    for i in "abcdefghijklmnñopqrstuvwxyz":
        patronIni = re.compile(i)
        for j in "abcdefghijklmnñopqrstuvwxyz":        
            patron = re.compile(i+j)    #crea patron de busqueda        
            a += len(patron.findall(archivo))#busca todas las letras del texto                        
            diccionario[i+j]=(len(patron.findall(archivo)))/ len(patronIni.findall(archivo))
    #diccionario = limpia(diccionario)    
    return (diccionario)
    

def unigramPalabras(archivo):
    a = 0
    diccionario = {}    
    total = len(archivo.split())      
    for i in archivo.split():
        if i not in diccionario:
            patron = re.compile(i)            
            a += len(patron.findall(archivo))        
            diccionario[codificaPalabra(i,teclado)]=[i,(len(patron.findall(archivo))/total)]
    return (diccionario)

def decodificaBigramLetras(numeros,diccionarioUni,diccionarioBi,teclado):
    numeros= numeros.split(" ")
    texto = []
    posPalabra = 0
    #Recorre los distintos numeros que se encontraban separados por espacios
    for numero in numeros:    
        #Se genera la primera letra a partir del unigram
        valDigito = (teclado.get(int(numero[0])))            
        letraI=valDigito[0]
        frecuenciaI = diccionarioUni.get(valDigito[0])            
        for y in valDigito:
            if(frecuenciaI < diccionarioUni.get(y)):
                letraI=y
                frecuenciaI = diccionarioUni.get(y)
        #Genera el resto de letras con el bigram
        texto.append(letraI)
        posLetra = 0
        for digito in numero[1:]:
            valDigito = (teclado.get(int(digito)))            
            letra=valDigito[0] 
            frecuencia = diccionarioBi.get(texto[posPalabra][posLetra]+letra)                     
            for valor in valDigito:
                if(frecuencia < diccionarioBi.get(texto[posPalabra][posLetra]+valor)):
                    letra=valor
                    frecuencia = diccionarioBi.get(texto[posPalabra][posLetra]+valor)    
            texto[posPalabra]+=letra
            print(posPalabra,posLetra, texto)
            posLetra += 1
        posPalabra += 1

def decodificaUnigramPalabras(numeros,diccionarioUni,diccionarioBi,diccionarioUniPal,teclado):
    numeros= numeros.split(" ")
    texto = []
    posPalabra = 0
    #Recorre los distintos numeros que se encontraban separados por espacios
    for numero in numeros:  
        if numero in diccionarioUniPal.keys() is not None:
            print(diccionarioUniPal.get(numero))
        else:
            #Se genera la primera letra a partir del unigram
            valDigito = (teclado.get(int(numero[0])))            
            letraI=valDigito[0]
            frecuenciaI = diccionarioUni.get(valDigito[0])            
            for y in valDigito:
                if(frecuenciaI < diccionarioUni.get(y)):
                    letraI=y
                    frecuenciaI = diccionarioUni.get(y)
            #Genera el resto de letras con el bigram
            texto.append(letraI)
            posLetra = 0
            for digito in numero[1:]:
                valDigito = (teclado.get(int(digito)))            
                letra=valDigito[0] 
                frecuencia = diccionarioBi.get(texto[posPalabra][posLetra]+letra)                     
                for valor in valDigito:
                    if(frecuencia < diccionarioBi.get(texto[posPalabra][posLetra]+valor)):
                        letra=valor
                        frecuencia = diccionarioBi.get(texto[posPalabra][posLetra]+valor)    
                texto[posPalabra]+=letra
                print(posPalabra,posLetra, texto)
                posLetra += 1
            posPalabra += 1
        
teclado = {}
teclado[2] = ["a","b","c"]
teclado[3] = ["d","e","f"]
teclado[4] = ["g","h","i"]
teclado[5] = ["j","k","l"]
teclado[6] = ["m","n","ñ","o"]
teclado[7] = ["p","q","r","s"]
teclado[8] = ["t","u","v"]
teclado[9] = ["w","x","y","z"]


archivo = readWords("texto")
diccionarioUni=unigramLetras(archivo)
diccionarioBi=bigramLetras(archivo)
diccionarioUniPal=unigramPalabras(archivo)
numeros = "42782 58346 5847"
#numeros = "4255462"
#(decodificaBigramLetras(numeros,diccionarioUni,diccionarioBi,teclado))
#print(unigramPalabras(archivo))
(decodificaUnigramPalabras(numeros,diccionarioUni,diccionarioBi,diccionarioUniPal,teclado))
