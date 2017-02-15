import re
import os.path

#--- elimina del texto caracteres extraños ---------------
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

#----- Genera el numero correspondiente a la palabra -----------------      
def codificaPalabra(palabra,teclado):
    numeros = ""
    for letra in palabra:
        for tecla in teclado:
            for caracter in teclado[tecla]:
                if caracter == letra:
                    numeros += str(tecla)
    return numeros
    
#-- Lee el archivo y le aplica las operaciones para obtener las palabras planas -----
def readWords(file1):
    text = open(file1,encoding = 'utf8')
    readW = text.read()
    readW.lower()    
    readW = reemplaza(readW)    
    return readW    

# almacenar un diccionario en un fichero
def guardaDiccionario(nombreArchivo,texto):
	with open(nombreArchivo, 'w') as f:
    		for key, value in texto.items():
        		f.write('%s:%s\n' % (key, value))

#------ Carga el diccionario de un archivo creado -----------------------
def leeDiccionario(nombreArchivo):
    data = dict()
    with open(nombreArchivo) as raw_data:	
        for item in raw_data:
            if (':' in item):
                key,value = item.split(':', 1)
                data[key]= float(value[:-1])
    return data
    
#------- Unigram de letras ------------------
def unigramLetras(archivo):
    if not os.path.isfile("unigramLetras"):
        print("Creando diccionario unigram letras")
        a = 0
        diccionario = {}    
        patron2 = re.compile("\w")
        total = (len(patron2.findall(archivo)))        
        for i in "abcdefghijklmnñopqrstuvwxyz":
            patron = re.compile(i)            
            a += len(patron.findall(archivo))        
            diccionario[i]=(len(patron.findall(archivo))/total)
        guardaDiccionario("unigramLetras",diccionario)
        print("Creado diccionario unigram letras")
    else:
        print("Cargando diccionario unigram letras")
        diccionario = leeDiccionario("unigramLetras")
    return (diccionario)

#-------- Bigram de letras -----------------
def bigramLetras(archivo):
    if not os.path.isfile("bigramLetras"):
        print("Creando diccionario bigram letras")
        a = 0
        diccionario = {}        
        for i in "abcdefghijklmnñopqrstuvwxyz":
            patronIni = re.compile(i)
            for j in "abcdefghijklmnñopqrstuvwxyz":        
                patron = re.compile(i+j)    #crea patron de busqueda        
                a += len(patron.findall(archivo))#busca todas las letras del texto                        
                diccionario[i+j]=(len(patron.findall(archivo)))/ len(patronIni.findall(archivo))
        guardaDiccionario("bigramLetras",diccionario)
        print("Creado diccionario bigram letras")
    else:
       print("Cargando diccionario bigram letras")
       diccionario = leeDiccionario("bigramLetras") 
    return (diccionario)
    
#------- Unigram de palabras -----------
def unigramPalabras(archivo):
    if not os.path.isfile("unigramPalabras"):
        print("Creando diccionario unigram palabras")
        a = 0
        diccionario = {}    
        total = len(archivo.split())      
        for i in archivo.split():
            #Clave formada por: [Numero + " " + Palabra]
            clave = codificaPalabra(i,teclado) + " " + i
            if clave not in diccionario:
                patron = re.compile(i)            
                a += len(patron.findall(archivo))        
                diccionario[clave]=(len(patron.findall(archivo))/total)
        guardaDiccionario("unigramPalabras",diccionario)
        print("Creado diccionario unigram palabras") 
    else:
       print("Cargando diccionario unigram palabras")
       diccionario = leeDiccionario("unigramPalabras")  
    return (diccionario)

#------- Bigram de palabras -----------
def bigramPalabras(archivo):
    if not os.path.isfile("bigramPalabras"):
        palabras = archivo.split()
        print("Creando diccionario bigram palabras")
        diccionario = {}        
        for i in range(len(palabras)):
            if i+1 < len(palabras)-1:
                #Clave formada por: [Numero anterior + " " + Palabra siguiente]
                clave = codificaPalabra(palabras[i],teclado) + " " + palabras[i+1]
                if clave not in diccionario:
                    patronIni = re.compile(palabras[i])
                    patronDos = re.compile(palabras[i] + " " + palabras[i+1])          
                    diccionario[clave] = (len(patronDos.findall(archivo))) / len(patronIni.findall(archivo))
        guardaDiccionario("bigramPalabras",diccionario)
        print("Creado diccionario bigram palabras") 
    else:
       print("Cargando diccionario bigram palabras")
       diccionario = leeDiccionario("bigramPalabras")  
    return (diccionario)

#-------------- Decodificacion usando solo bigram y unigram de letras --------------
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


#-------------- Decodificacion usando bigram y unigram de letras y palabras ------
def decodificaUnigramPalabras(numeros,diccionarioUni,diccionarioBi,diccionarioUniPal,teclado):
    numeros= numeros.split(" ")
    texto = []
    posPalabra = 0
    #Recorre los distintos numeros que se encontraban separados por espacios
    for numero in numeros:  
        #Buscar en unigram de palabras si existe alguna entrada para ese numero
        palabra = ""
        frecuencia = 0
        for claves in diccionarioUniPal:
            num,valor = claves.split(' ', 1)
            if(num == numero):
                if(frecuencia < diccionarioUniPal.get(claves)):
                    palabra = valor
                    frecuencia = diccionarioUniPal.get(claves)               
        if len(palabra) > 0:
            print(palabra)
        #Si no existe en unigram de palabras ninguna entrada, se aplica el bigram de letras
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
            
#-------------- Decodificacion usando bigram y unigram de letras y palabras ------
def decodificaBigramPalabras(numeros,diccionarioUni,diccionarioBi,diccionarioUniPal,diccionarioBiPal,teclado):
    numeros= numeros.split(" ")
    texto = []
    posPalabra = 0
    #Recorre los distintos numeros que se encontraban separados por espacios
    for contador in range(len(numeros)):
        if contador == 0:
            numero = numeros[0]
            palabra = ""
            frecuencia = 0
            for claves in diccionarioUniPal:
                num,valor = claves.split(' ', 1)
                if(num == numero):
                    if(frecuencia < diccionarioUniPal.get(claves)):
                        palabra = valor
                        frecuencia = diccionarioUniPal.get(claves)                 
            if len(palabra) > 0:
                print(palabra)
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
        else:
            palabra = ""
            frecuencia = 0
            for claves in diccionarioBiPal:
                num,valor = claves.split(' ', 1)
                if(num == numero):         
                    if(frecuencia < diccionarioBiPal.get(claves)):
                        palabra = valor
                        frecuencia = diccionarioBiPal.get(claves)                      
            print(palabra)
            numero = codificaPalabra(palabra,teclado)
        
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
diccionarioBiPal = bigramPalabras(archivo)
numeros = "42782 58346 5847"
#numeros = "4255462"
#(decodificaBigramLetras(numeros,diccionarioUni,diccionarioBi,teclado))
#print(unigramPalabras(archivo))
(decodificaUnigramPalabras(numeros,diccionarioUni,diccionarioBi,diccionarioUniPal,teclado))
decodificaBigramPalabras(numeros,diccionarioUni,diccionarioBi,diccionarioUniPal,diccionarioBiPal,teclado)
