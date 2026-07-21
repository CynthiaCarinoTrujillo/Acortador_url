from flask import Flask, render_template, request #render_template es una clase importada
#request es el objeto que trae datos enviados por el navegador
import random
import string 
from urllib.parse import urlparse #para validar URLs
app= Flask(__name__) #inicializando aplicacion
urls_dict={} #para que es?

def es_url_valida(url): #funcion que valida si la URL es correcta
    try:
        resultado = urlparse(url)
        esquemas_validos = ['http', 'https']
        return resultado.scheme in esquemas_validos and bool(resultado.netloc)
    except:
        return False

def generar_url_corta(): #funcion que genera el url corto
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres)for _ in range(6))

@app.route('/', methods=['GET', 'POST']) #esto es un decorador indicando que es la ruta raiz. Indicamos que acepte GET y POST

def index(): #esto es una vista que se expresa en forma de funcion
    if request.method== 'POST':
        url =request.form['URLusuario']
        if not es_url_valida(url):
            return "URL no valida"
        url_corta= generar_url_corta()
        urls_dict[url_corta]= url
        url_corta_completa=f"www.{url_corta}.com"
        return render_template('resultado.html', url_corta=url_corta_completa)
    return render_template('index.html')

@app.route('/<codigo>')
def redirigir(codigo):
    if codigo in urls_dict:
        from flask import redirect
        return redirect(urls_dict[codigo])
    else:
        return "URL no encontrada", 404

if __name__=='__main__': #comprobamos que si estamos desde el archivo main 
    app.run(debug=True, port=5000)  #entonces ejecutamos la aplicacion
