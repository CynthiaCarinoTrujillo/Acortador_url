from flask import Flask #clase importada

app= Flask(__name__) #inicializando aplicacion

@app.route('/') #esto es un decorador indicando que es la ruta raiz

def index(): #esto es una vista que se expresa en forma de funcion
    return "Hola :)"

if __name__=='__main__': #comprobamos que si estamos desde el archivo main 
    app.run(debug=True, port=5000)  #entonces ejecutamos la aplicacion
