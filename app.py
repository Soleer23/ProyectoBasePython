from flask import Flask, jsonify
from flask import flash, get_flashed_messages # se importan para poder enviar mensajes a sweetAlerte2
from flask import render_template, session
from flask import url_for
from flask import request                 #recepciona la informacion "DEL FORMULARIO"
from flask import redirect                #redirecciona "MUESTRA LA INFORMACION PARA LAS TABLAS"
import mysql.connector                   #Se importa libreria para conexion a base de datos 
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
    
    conn = mysql.connector.connect(**config) # Crear una conexión al servidor MySQL
    cursor = conn.cursor() # Crear un cursor para ejecutar comandos SQL

    cursor.execute("SELECT * FROM modelos")
    modelos = cursor.fetchall()
    
    print(modelos)

    cursor.execute("SELECT * FROM marcas")
    marcas = cursor.fetchall()
    

    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    
    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return render_template('admin/ModelosAdmin.html', modelos = modelos, marcas = marcas, categorias = categorias)


@app.route('/admin/ModelosAdmin/guardar', methods = ['POST'])
def admin_modelos_guardar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')

    num_modelo = request.form['num_modelo']
    marca = request.form['marca']
    categoria = request.form['categoria']
    anio_lanzamiento = request.form['anio_lanzamiento']
    id_marca = request.form['id_marca']
    id_categoria = request.form['id_categoria']



    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "INSERT INTO modelos (num_modelo, marca, categoria, anio_lanzamiento,id_marca, id_categoria) VALUES (%s, %s, %s, %s, %s, %s)"
    datos = (num_modelo, marca, categoria, anio_lanzamiento, id_marca, id_categoria)
    
    cursor.execute(sql, datos)
    conn.commit()
    

    print(num_modelo)
    print(marca)
    print(categoria)
    print(anio_lanzamiento)
    print(id_marca)
    print(id_categoria)

    return redirect('/ModelosAdmin')

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

    return redirect('/ModelosAdmin')


@app.route('/MotosAdmin')
def admin_motos():
    if not 'login' in session:
        return redirect('/admin/loginAdmin')

    conn = mysql.connector.connect(**config) # Crear una conexión al servidor MySQL
    cursor = conn.cursor() # Crear un cursor para ejecutar comandos SQL

    cursor.execute("SELECT * FROM motos")
    motos = cursor.fetchall()
    
    print(motos)

    cursor.execute("SELECT * FROM ficha_tecnica")
    ficha_tecnica = cursor.fetchall()
    

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    
    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return render_template('admin/MotosAdmin.html', motos = motos, ficha_tecnica = ficha_tecnica, usuarios = usuarios)


@app.route('/admin/MotosAdmin/guardar', methods = ['POST'])
def admin_motos_guardar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    num_serie = request.form['num_serie']
    nom_moto = request.form['nom_moto']
    id_ficha = request.form['id_ficha']
    id_usuario = request.form['id_usuario']

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "INSERT INTO motos (num_serie, nom_moto, id_ficha, id_usuario) VALUES (%s, %s, %s, %s)"
    datos = (num_serie, nom_moto, id_ficha, id_usuario)

    cursor.execute(sql, datos)
    conn.commit()

    print(num_serie)
    print(nom_moto)
    print(id_ficha)
    print(id_usuario)

    return redirect('/MotosAdmin')


@app.route('/admin/MotosAdmin/borrar', methods = ['POST'])
def admin_motos_borrar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    

    id_motos  = request.form['id_motos ']

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "DELETE FROM motos WHERE id_motos  = %s"
    cursor.execute(sql, [id_motos ])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/MotosAdmin')


@app.route('/FichaTecAdmin')
def admin_ficha_tecnica():
    if not 'login' in session:
        return redirect('/admin/loginAdmin')

    conn = mysql.connector.connect(**config) # Crear una conexión al servidor MySQL
    cursor = conn.cursor() # Crear un cursor para ejecutar comandos SQL

    cursor.execute("SELECT * FROM ficha_tecnica")
    ficha_tecnica = cursor.fetchall()
    
    print(ficha_tecnica)

    cursor.execute("SELECT * FROM modelos")
    modelos = cursor.fetchall()
    

    cursor.execute("SELECT * FROM tipos_motor")
    tipos_motor = cursor.fetchall()
    
    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return render_template('admin/FichaTecAdmin.html', ficha_tecnica = ficha_tecnica, modelos = modelos, tipos_motor = tipos_motor)



@app.route('/admin/FichaTecAdmin/guardar', methods = ['POST'])
def admin_ficha_tecnica_guardar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    modelo = request.form['modelo']
    motor = request.form['motor']
    cilindraje = request.form['cilindraje']
    potencia_hp = request.form['potencia_hp']
    torque_nm =	request.form['torque_nm']
    transmision = request.form['transmision'] 
    cap_combustible = request.form['cap_combustible']
    peso_kg = request.form['peso_kg']
    velocidad_max_kmh = request.form['velocidad_max_kmh']
    id_modelo = request.form['id_modelo']
    id_tipo = request.form['id_tipo']

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "INSERT INTO ficha_tecnica (modelo, motor, cilindraje, potencia_hp, torque_nm, transmision, cap_combustible, peso_kg, velocidad_max_kmh, id_modelo, id_tipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s , %s , %s, %s)"
    datos = (modelo, motor, cilindraje, potencia_hp, torque_nm, transmision, cap_combustible, peso_kg, velocidad_max_kmh, id_modelo, id_tipo)

    cursor.execute(sql, datos)
    conn.commit()
    
    print(modelo)
    print(motor)
    print(cilindraje)
    print(potencia_hp)
    print(torque_nm)
    print(transmision)
    print(cap_combustible)
    print(peso_kg)
    print(velocidad_max_kmh)
    print(id_modelo)
    print(id_tipo)

    return redirect('/FichaTecAdmin')

@app.route('/admin/FichaTecAdmin/borrar', methods = ['POST'])
def admin_ficha_tecnica_borrar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    

    id_ficha  = request.form['id_ficha ']

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "DELETE FROM ficha_tecnica WHERE id_ficha  = %s"
    cursor.execute(sql, [id_ficha ])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/FichaTecAdmin')

@app.route('/TipoMotorAdmin')
def admin_tipos_motor():
    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tipos_motor')
    tipomotor  = cursor.fetchall()
    cursor.close()
    conn.close()

    print("Tipos:", tipomotor )  

    return render_template('/admin/TipoMotorAdmin.html', tipomotor = tipomotor )


@app.route('/admin/TipoMotorAdmin/guardar', methods=['POST'])
def admin_tipos_motor_guardar():
    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    tipo = request.form.get('tipo')

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "INSERT INTO tipos_motor (tipo) VALUES (%s)"
    cursor.execute(sql,(tipo))

    conn.commit()
    cursor.close()                                                                                                                                      
    conn.close()

    return redirect('/TipoMotorAdmin') 

@app.route('/admin/TipoMotorAdmin/borrar', methods=['POST'])
def admin_tipos_motor_borrar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    id_tipo = request.form.get('id_tipo')

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "DELETE FROM tipos_motor WHERE id_tipo = %s"
    cursor.execute(sql, [id_tipo])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/TipoMotorAdmin')








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



