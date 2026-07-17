from flask import Flask, render_template, request #render_template es una clase importada
#request es el objeto que trae datos enviados por el navegador
app= Flask(__name__) #inicializando aplicacion

@app.route('/', methods=['GET', 'POST']) #esto es un decorador indicando que es la ruta raiz. Indicamos que acepte GET y POST

def index(): #esto es una vista que se expresa en forma de funcion
    if request.method== 'POST':
        url =request.form['URLusuario']
        return f"Recibi la URL: {url}"
    return render_template('index.html')

if __name__=='__main__': #comprobamos que si estamos desde el archivo main 
    app.run(debug=True, port=5000)  #entonces ejecutamos la aplicacion
