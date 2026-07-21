from flask import Flask, render_template, request #render_template es una clase importada
#request es el objeto que trae datos enviados por el navegador
import random
import string 
from urllib.parse import urlparse #para validar URLs
import sqlite3
from datetime import datetime
import os

app= Flask(__name__) #inicializan aplicacion
urls_dict={} 

def es_url_valida(url): #funcion que valida si la URL es correcta
    try:
        resultado = urlparse(url)
        esquemas_validos = ['http', 'https']
        return resultado.scheme in esquemas_validos and bool(resultado.netloc)
    except:
        return False
    
def inicializar_bd(): #funcion para la base de datos
    conexion = sqlite3.connect('urls.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            url_original TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conexion.commit()
    conexion.close()

def guardar_url(codigo, url_original):
    conexion = sqlite3.connect('urls.db')
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO urls (codigo, url_original) VALUES (?, ?)', (codigo, url_original))
    conexion.commit()
    conexion.close()

def obtener_url(codigo):
    conexion = sqlite3.connect('urls.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT url_original FROM urls WHERE codigo = ?', (codigo,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado[0] if resultado else None

inicializar_bd()

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
        guardar_url(url_corta, url)
        url_corta_completa=f"www.{url_corta}.com"
        return render_template('resultado.html', url_corta=url_corta, request_host=request.host)
    return render_template('index.html')

@app.route('/<codigo>')
def redirigir(codigo):
    url_original = obtener_url(codigo)
    if url_original:
        from flask import redirect
        return redirect(url_original)
    else:
        return "URL no encontrada", 404

if __name__=='__main__': #comprobamos que si estamos desde el archivo main 
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
