from flask import Flask, render_template, jsonify, flash, get_flashed_messages
from flask import session, url_for, request, redirect, send_from_directory, abort
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "Alejo"

# Configuración de la conexión MySQL
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306,
    'database': 'motos_db_simple'
}

# ==========================
#      RUTAS PÚBLICAS
# ==========================

@app.route('/')
def inicio():
    return render_template('/sitio/index.html')


@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')


@app.route('/marcas')
def marcas_public():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM marcas')
    marcas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('/sitio/marcas.html', marcas=marcas)

@app.route('/marca/<nombre>')
def marca_detalle(nombre):
    try:
        nombre = nombre.lower()

        paginas = {
            'yamaha': 'yamaha.html',
            'harley': 'harley.html',
            'ducati': 'ducati.html',
            'honda': 'honda.html',
            'bmw': 'bmw.html',
            'kawasaki': 'kawasaki.html',
            'suzuki': 'suzuki.html',
            'ktm': 'ktm.html',
            'triumph': 'triumph.html'
        }

        if nombre in paginas:
            return render_template(f"sitio/marcas/{paginas[nombre]}")
        else:
            abort(404)

    except Exception as e:
        print("Error al cargar marca:", e)
        abort(500)


@app.route('/')
def tipos_motos_public():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categorias')
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sitio/tiposdemotos.html', categorias=categorias)


@app.route('/modelos')
def modelos_public():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id_modelo, m.num_modelo, ma.nom_marca, c.nom_categ, m.anio_lanzamiento
        FROM modelos m
        JOIN marcas ma ON m.id_marca = ma.id_marca
        JOIN categorias c ON m.id_categoria = c.id_categoria
    """)
    modelos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sitio/modelos.html', modelos=modelos)


@app.route('/historia')
def historia_public():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.id_ficha, f.modelo, f.motor, f.cilindraje, f.potencia_hp, 
        f.torque_nm, f.transmision, f.cap_combustible, f.peso_kg, f.velocidad_max_kmh
        FROM ficha_tecnica f
    """)
    fichas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sitio/historia.html', fichas=fichas)


@app.route('/reseñas')
def reseñas():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM resenas")
    reseñas = cursor.fetchall()
    cursor.close()
    conn.close()

    promedio = 0
    if reseñas:
        total = sum(int(r['calificacion']) for r in reseñas)
        promedio = round(total / len(reseñas), 1)

    return render_template('sitio/reseñas.html', reseñas=reseñas, promedio=promedio)


@app.route('/reseñas/agregar', methods=['POST'])
def agregar_resena():
    usuario = request.form['usuario']
    modelo = request.form['modelo']
    calificacion = request.form['calificacion']
    comentario = request.form['comentario']

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute("SELECT id_usuario FROM usuarios WHERE nom_user = %s", (usuario,))
    id_usuario = cursor.fetchone()

    cursor.execute("SELECT id_modelo FROM modelos WHERE num_modelo = %s", (modelo,))
    id_modelo = cursor.fetchone()

    id_usuario_val = id_usuario[0] if id_usuario else None
    id_modelo_val = id_modelo[0] if id_modelo else None

    sql = """
        INSERT INTO resenas (usuario, modelo, calificacion, comentario, id_usuario, id_modelo)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    datos = (usuario, modelo, calificacion, comentario, id_usuario_val, id_modelo_val)
    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/reseñas')


# ==========================
#        ADMIN LOGIN
# ==========================

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

@app.route('/admin/loginAdmin', methods=['POST'])
def admin_login_post():
    usuario = request.form['usuario']
    password = request.form['password']

    if usuario == "Alejandro" and password == "2008":
        session["login"] = True
        session["user"] = "Alejandro"
        return redirect('/admin')
    else:
        return render_template('admin/loginAdmin.html', mensaje="Datos incorrectos")


@app.route('/admin/cerrar')
def admin_cerrar_session():
    session.clear()
    return redirect('/admin/loginAdmin')


# ==========================
#      PANEL ADMIN
# ==========================

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
    
    
    tipo = request.form['tipo']    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    sql = "INSERT INTO tipos_motor(tipo) VALUES(%s);"
    cursor.execute(sql,(tipo,))

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
    cursor.execute(sql, (id_tipo,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/TipoMotorAdmin')

@app.route('/ReseñasAdmin')
def admin_resenas():
    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    conn = mysql.connector.connect(**config) # Crear una conexión al servidor MySQL
    cursor = conn.cursor() # Crear un cursor para ejecutar comandos SQL

    cursor.execute("SELECT * FROM resenas")
    resenas = cursor.fetchall()

    print(resenas)

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.execute("SELECT * FROM modelos")
    modelos = cursor.fetchall()

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return render_template('admin/ReseñasAdmin.html', resenas = resenas, usuarios = usuarios, modelos = modelos)





@app.route('/admin/ReseñasAdmin/guardar', methods = ['POST'])
def admin_resenas_guardar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    
    usuario = request.form['usuario']
    modelo = request.form['modelo']
    calificacion = request.form['calificacion']
    comentario = request.form['comentario']
    id_usuario = request.form['id_usuario']
    id_modelo = request.form['id_modelo']
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "INSERT INTO resenas (usuario, modelo, calificacion, comentario, id_usuario, id_modelo) VALUES (%s, %s, %s, %s, %s, %s)"
    datos = (usuario, modelo, calificacion, comentario, id_usuario, id_modelo)
    
    cursor.execute(sql, datos)
    conn.commit()

    print(usuario)
    print(modelo)
    print(calificacion)
    print(comentario)
    print(id_usuario)
    print(id_modelo)

    return redirect('/ReseñasAdmin')


@app.route('/admin/ReseñasAdmin/borrar', methods = ['POST'])
def admin_resenas_borrar():

    if not 'login' in session:
        return redirect('/admin/loginAdmin')
    

    id_resena = request.form['id_resena']

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    sql = "DELETE FROM resenas WHERE id_resena = %s"
    cursor.execute(sql, [id_resena])
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/ReseñasAdmin')









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



