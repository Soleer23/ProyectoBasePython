from flask import Flask, jsonify
from flask import flash, get_flashed_messages # se importan para poder enviar mensajes a sweetAlerte2
from flask import render_template, session
from flask import url_for
from flask import request                 #recepciona la informacion "DEL FORMULARIO"
from flask import redirect                #redirecciona "MUESTRA LA INFORMACION PARA LAS TABLAS"
import mysql.connector                    #Se importa libreria para conexion a base de datos 
from datetime import datetime             #Se importa para colocar un tiempo exacto "Para la imagen"
from flask import send_from_directory     #optenemos informacion de la imagen
from flask import abort #obtenemos la informacion de la imagen, es necesaria para mostrar las imagenes
import os





app = Flask(__name__) #se crea la aplicacion
app.secret_key="Alejo"  

# Configuración de la conexión MySQL usando MySQL X Protocol
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306,                  # Puerto para MySQL X Protocol
    'database': 'motos_db_simple'
}



@app.route('/')
def inicio():
    
    return render_template('sitio/index.html')


""" Mostramos la imagen y la enviamos a la ruta  """
@app.route('/img/libros/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img/libros'),imagen)

#enlazar los archivos css
""" 
@app.route('/css/<archivocss>')
def css(archivocss):
    return send_from_directory(os.path.join("templates/sitio/css"), archivocss) 
"""


@app.route('/libros')
def libros():

    conn = mysql.connector.connect(**config) # Crear una conexión al servidor MySQL
    cursor = conn.cursor() # Crear un cursor para ejecutar comandos SQL    
    cursor.execute('SELECT * FROM libros') # Ejecutar una consulta SQL     
    listaLibros = cursor.fetchall() # Obtener los resultados de la consulta
    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return render_template('sitio/libros.html', listaLibros = listaLibros)


@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')





@app.route('/admin/')
def admin_index():

    """ Preguntamos si el usuario esta logeado o 
        tiene una session activa """
    if  not 'login' in session:
        return redirect('/admin/loginAdmin') 

    return render_template('admin/index.html')

@app.route('/admin/loginAdmin')
def admin_login():
    return render_template('admin/loginAdmin.html')



""" Ruta para login, solo se valida por codigo, NO por 
    base de datos """
@app.route('/admin/loginAdmin', methods=['POST'])
def admin_login_post():

    usuario  = request.form['usuario']
    password = request.form['password']
    #verifica que llega
    print(usuario,password)

    if usuario == "Alejandro" and password == "2008":
        session["login"] = True
        session["user"] = "Alejandro"

        return redirect('/admin')
    else:
        print(f"datos incorrectos")

    return render_template('admin/loginAdmin.html', mensaje = "Datos incorrectos .|.")

@app.route('/admin/cerrar')
def admin_cerrar_session():
    session.clear()
    return redirect('/admin/loginAdmin')


@app.route('/UserAdmin')
def usuario():
    if not 'login' in session:
        return redirect('/admin/loginAdmin')

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    listaUsuarios2 = cursor.fetchall()
    cursor.close()
    conn.close()

    print("Usuarios:", listaUsuarios2)  

    return render_template('admin/UserAdmin.html', listaUsuarios2= listaUsuarios2)


    

@app.route('/admin/UserAdmin/guardar', methods=['POST'])
def admin_usuarios_guardar():
    if not 'login' in session:
        return redirect('/admin/loginAdmin')

    nom_user = request.form.get('nom_user')
    ape_user = request.form.get('ape_user')
    email_user = request.form.get('email_user')

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "INSERT INTO usuarios (nom_user, ape_user, email_user) VALUES (%s, %s, %s)"
    cursor.execute(sql,(nom_user, ape_user, email_user))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/UserAdmin') 
            
        
        
        
@app.route('/admin/UserAdmin/borrar', methods=['POST'])
def admin_usuarios_borrar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    id_usuario = request.form['id_usuario']

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "DELETE FROM usuarios WHERE id_usuario = %s"
    cursor.execute(sql, [id_usuario])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/UserAdmin')



@app.route('/CategAdmin')
def categorias ():
    """ Preguntamos si el usuario esta logeado o 
        tiene una session activa """
    if  not 'login' in session:
        return redirect('/admin/loginAdmin') 

    """ Esta funcion me sirve para mostrar todos los libros de mi base de datos    """
    conn = mysql.connector.connect(**config) # Crear una conexión al servidor MySQL
    cursor = conn.cursor() # Crear un cursor para ejecutar comandos SQL    
    cursor.execute('SELECT * FROM categorias') # Ejecutar una consulta SQL     
    listacategorias = cursor.fetchall() # Obtener los resultados de la consulta


    #print(f"conexion ok *********************{listaLibros} **************************" )

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return render_template('admin/CategAdmin.html',listacategorias=listacategorias)

@app.route('/admin/CategAdmin/guardar', methods=['POST'])
def admin_categorias_guardar():
    if not 'login' in session:
        return redirect('/admin/loginAdmin')

    nom_categ = request.form.get('nom_categ')
    des_categ = request.form.get('des_categ')

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "INSERT INTO categorias (nom_categ, des_categ) VALUES (%s, %s)"
    cursor.execute(sql,[nom_categ, des_categ])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/CategAdmin') 


@app.route('/admin/CategAdmin/borrar', methods=['POST'])
def admin_categorias_borrar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    id_categoria = request.form['id_categoria']

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "DELETE FROM categorias WHERE id_categoria = %s"
    cursor.execute(sql, [id_categoria])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/CategAdmin')



@app.route('/MarcasAdmin')
def marcas ():
    """ Preguntamos si el usuario esta logeado o 
        tiene una session activa """
    if  not 'login' in session:
        return redirect('/admin/loginAdmin') 

    """ Esta funcion me sirve para mostrar todos los libros de mi base de datos    """
    conn = mysql.connector.connect(**config) # Crear una conexión al servidor MySQL
    cursor = conn.cursor() # Crear un cursor para ejecutar comandos SQL    
    cursor.execute('SELECT * FROM marcas') # Ejecutar una consulta SQL     
    listamarcas = cursor.fetchall() # Obtener los resultados de la consulta


    #print(f"conexion ok *********************{listaLibros} **************************" )

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return render_template('/admin/MarcasAdmin.html',listamarcas=listamarcas)

@app.route('/admin/MarcasAdmin/guardar', methods= ['POST'])
def admin_marcas_guardar():
    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    nom_marca = request.form.get('nom_marca')
    pais_origen = request.form.get('pais_origen')
    año_funda = request.form.get('año_funda')

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "INSERT INTO marcas (nom_marca, pais_origen, año_funda ) VALUES (%s, %s, %s)"
    cursor.execute(sql,[nom_marca, pais_origen, año_funda])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/MarcasAdmin')

@app.route('/admin/MarcasAdmin/borrar', methods=['POST'])
def admin_marcas_borrar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    id_marca = request.form['id_marca']

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "DELETE FROM marcas WHERE id_marca = %s"
    cursor.execute(sql, [id_marca])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/MarcasAdmin')


@app.route('/ModelosAdmin')
def admin_modelos():
    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor

    cursor.execute("SELECT * FROM 'modelos'")
    modelos = cursor.fetchall()
    conexion.commit
    print(modelos)

    cursor.execute("SELECT * FROM 'marcas'")
    marcas = cursor.fetchall()
    conexion.commit()

    cursor.execute("SELECT * FROM 'categorias'")
    categorias = cursor.fetchall()
    conexion.commit()

    return render_template('admin/ModelosAdmin.html', modelos = modelos, marcas = marcas, categorias = categorias)


@app.route('/admin/ModelosAdmin/guardar', methods = ['POST'])
def admin_modelos_guardar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')

    id_modelo = request.form['id_modelo']
    id_categoria = request.form['id_categoria']
    id_marca = request.form['id_marca']
    num_modelo = request.form['num_modelo']
    nom_marca = request.form['nom_marca']
    nom_categ = request.form['nom_categ']


    sql = "INSERT INTO 'modelos' ('id_modelo', 'id_categoria', 'id_marca', 'num_modelo', 'nom_marca', 'nom_categ') VALUES (%s, %s, %s, %s, %s, %s)"
    datos = (id_modelo, id_categoria, id_marca, num_modelo, nom_marca, nom_categ)
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    print(id_modelo)
    print(id_categoria)
    print(id_marca)
    print(num_modelo)
    print(nom_marca)
    print(nom_categ)

    return redirect('/admin/ModelosAdmin')

@app.route('/admin/ModelosAdmin/borrar', methods = ['POST'])
def admin_modelos_borrar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    

    id_modelo = request.form['id_modelo']

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "DELETE FROM modelos WHERE id_modelo = %s"
    cursor.execute(sql, [id_modelo])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/admin/ModelosAdmin')





"""
Este comando es necesario para 
correr nuestra aplicacion
""",
if __name__ == '__main__':
    app.run(debug=True)



from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:password@localhost/motos_db_simple'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "clave_secreta"

db = SQLAlchemy(app)




