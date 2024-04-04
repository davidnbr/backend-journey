# Archivo principal que maneja rutas y lanzamiento de la aplicación

from flask import Flask, render_template, request, redirect, url_for # Importo Flask y render_template para renderizar archivos HTML
import os # Para acceder a directorios
import db.client as db # Importo el cliente de la base de datos

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) # Creo direccion absoluta para luego usarlo y acceder a archivos en mi directorio
template_dir = os.path.join(template_dir, 'src', 'templates') # Agrego las dos carpetas que necesito para llegar a mi carpeta de templates

app = Flask(__name__, template_folder=template_dir) # Inicializo la aplicación de Flask

# Rutas de la aplicación
@app.route('/')
def home():
    cursor = db.database.cursor() # Creo un cursor para interactuar con la base de datos
    cursor.execute("SELECT * FROM users")
    my_result = cursor.fetchall() # Obtengo todos los resultados de la consulta
    # Convertir datos a diccionario
    insert_object = []
    column_names = [column[0] for column in cursor.description] # Almaceno nombres de columnas
    for record in my_result: # Uso zip para hacer un arreglo bidimensional
        insert_object.append(dict(zip(column_names, record))) # Creo un diccionario con los nombres de las columnas y los valores de cada registro
    cursor.close() # Cierro el cursor

    # Paso los datos para poder iterar con esa información (insert_object)
    return render_template('index.html', data=insert_object) # Renderizo el archivo index.html

# Ruta para guardar usuarios en la base de datos
@app.route('/user', methods=['POST'])
def add_user():
    username = request.form['username'] # Obtengo el contenido del input de formulario en index.html
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (username, name, password) VALUES (%s, %s, %s)" # Consulta SQL con 3 valores tipo string (%s)
        data = (username, name, password)
        cursor.execute(sql, data)
        db.database.commit() # Hago commit a base de datos para que se suban los datos
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id = %s"
    data = (id,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>',methods=['POST'])
def edit(id):
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    
    if username and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE users SET username = %s, name = %s, password = %s WHERE id = %s"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ =='__main__': # Si corremos el archivo principal
    app.run(debug=True) # Lanzo la aplicación en modo debug