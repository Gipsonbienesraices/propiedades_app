from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'tu_clave_secreta_aqui')
app.config['UPLOAD_FOLDER'] = 'imagenes_propiedades'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Configuración de base de datos
DATABASE_URL = os.getenv('DATABASE_URL')

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

# Clase User para Flask-Login
class User(UserMixin):
    def __init__(self, user_id, username, is_admin):
        self.id = user_id
        self.username = username
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user:
        return User(user['id'], user['username'], user['is_admin'])
    return None

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT TRUE
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS propiedades (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            precio REAL NOT NULL,
            ubicacion TEXT NOT NULL,
            descripcion TEXT,
            recamaras INTEGER,
            banos INTEGER,
            tipo_propiedad TEXT NOT NULL,
            operacion TEXT NOT NULL,
            fecha_creacion TEXT NOT NULL
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS imagenes (
            id SERIAL PRIMARY KEY,
            propiedad_id INTEGER NOT NULL,
            ruta TEXT NOT NULL,
            FOREIGN KEY (propiedad_id) REFERENCES propiedades (id)
        )
    ''')
    
    # Crear usuario admin por defecto si no existe
    cur.execute("SELECT * FROM usuarios WHERE username = 'admin'")
    if not cur.fetchone():
        password_hash = generate_password_hash('admin123')
        cur.execute(
            'INSERT INTO usuarios (username, password_hash, is_admin) VALUES (%s, %s, %s)',
            ('admin', password_hash, True)
        )
    
    conn.commit()
    cur.close()
    conn.close()

@app.route('/imagenes_propiedades/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM propiedades ORDER BY fecha_creacion DESC')
    propiedades = cur.fetchall()
    cur.close()
    conn.close()
    
    # Obtener imágenes para cada propiedad
    propiedades_con_imagenes = []
    for prop in propiedades:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT ruta FROM imagenes WHERE propiedad_id = %s', (prop['id'],))
        imagenes = cur.fetchall()
        cur.close()
        conn.close()
        prop_dict = dict(prop)
        prop_dict['imagenes'] = [img['ruta'] for img in imagenes]
        propiedades_con_imagenes.append(prop_dict)
    
    return render_template('index.html', propiedades=propiedades_con_imagenes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['id'], user['username'], user['is_admin'])
            login_user(user_obj)
            flash('¡Inicio de sesión exitoso!')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente')
    return redirect(url_for('index'))

@app.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        precio = float(request.form['precio'])
        ubicacion = request.form['ubicacion']
        descripcion = request.form['descripcion']
        recamaras = request.form.get('recamaras')
        banos = request.form.get('banos')
        tipo_propiedad = request.form['tipo_propiedad']
        operacion = 'Venta'  # Fijo como solicitado
        
        # Manejar campos opcionales para terrenos
        if tipo_propiedad == 'Terreno':
            recamaras = None
            banos = None
        else:
            recamaras = int(recamaras) if recamaras else None
            banos = int(banos) if banos else None
        
        fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Guardar propiedad en la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO propiedades (titulo, precio, ubicacion, descripcion, recamaras, banos, tipo_propiedad, operacion, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
            (titulo, precio, ubicacion, descripcion, recamaras, banos, tipo_propiedad, operacion, fecha_creacion)
        )
        propiedad_id = cur.fetchone()['id']
        
        # Guardar imágenes
        archivos = request.files.getlist('imagenes')
        for file in archivos:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Agregar timestamp para evitar nombres duplicados
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Guardar ruta en la base de datos
                cur.execute(
                    'INSERT INTO imagenes (propiedad_id, ruta) VALUES (%s, %s)',
                    (propiedad_id, filename)
                )
        
        conn.commit()
        cur.close()
        conn.close()
        
        flash('Propiedad registrada exitosamente!')
        return redirect(url_for('index'))
    
    return render_template('registrar.html')

@app.route('/editar/<int:propiedad_id>', methods=['GET', 'POST'])
@login_required
def editar(propiedad_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM propiedades WHERE id = %s', (propiedad_id,))
    propiedad = cur.fetchone()
    
    if not propiedad:
        flash('Propiedad no encontrada')
        return redirect(url_for('index'))
    
    # Obtener imágenes actuales
    cur.execute('SELECT * FROM imagenes WHERE propiedad_id = %s', (propiedad_id,))
    imagenes_actuales = cur.fetchall()
    cur.close()
    conn.close()
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        precio = float(request.form['precio'])
        ubicacion = request.form['ubicacion']
        descripcion = request.form['descripcion']
        recamaras = request.form.get('recamaras')
        banos = request.form.get('banos')
        tipo_propiedad = request.form['tipo_propiedad']
        operacion = 'Venta'
        
        if tipo_propiedad == 'Terreno':
            recamaras = None
            banos = None
        else:
            recamaras = int(recamaras) if recamaras else None
            banos = int(banos) if banos else None
        
        # Actualizar propiedad
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE propiedades SET titulo = %s, precio = %s, ubicacion = %s, descripcion = %s, recamaras = %s, banos = %s, tipo_propiedad = %s WHERE id = %s',
            (titulo, precio, ubicacion, descripcion, recamaras, banos, tipo_propiedad, propiedad_id)
        )
        
        # Manejar nuevas imágenes
        archivos = request.files.getlist('imagenes')
        for file in archivos:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                cur.execute(
                    'INSERT INTO imagenes (propiedad_id, ruta) VALUES (%s, %s)',
                    (propiedad_id, filename)
                )
        
        # Eliminar imágenes seleccionadas
        imagenes_a_eliminar = request.form.getlist('eliminar_imagenes')
        for img_id in imagenes_a_eliminar:
            # Eliminar archivo del sistema
            cur.execute('SELECT ruta FROM imagenes WHERE id = %s', (img_id,))
            img = cur.fetchone()
            if img:
                try:
                    img_path = os.path.join(app.config['UPLOAD_FOLDER'], img['ruta'])
                    if os.path.exists(img_path):
                        os.remove(img_path)
                except:
                    pass  # Si falla la eliminación del archivo, continuamos
            
            # Eliminar registro de la base de datos
            cur.execute('DELETE FROM imagenes WHERE id = %s', (img_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        flash('Propiedad actualizada exitosamente!')
        return redirect(url_for('index'))
    
    return render_template('editar.html', propiedad=propiedad, imagenes=imagenes_actuales)

@app.route('/eliminar/<int:propiedad_id>', methods=['POST'])
@login_required
def eliminar(propiedad_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Obtener imágenes para eliminar archivos
    cur.execute('SELECT ruta FROM imagenes WHERE propiedad_id = %s', (propiedad_id,))
    imagenes = cur.fetchall()
    
    # Eliminar archivos del sistema
    for img in imagenes:
        try:
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img['ruta'])
            if os.path.exists(img_path):
                os.remove(img_path)
        except:
            pass
    
    # Eliminar imágenes de la base de datos
    cur.execute('DELETE FROM imagenes WHERE propiedad_id = %s', (propiedad_id,))
    
    # Eliminar propiedad
    cur.execute('DELETE FROM propiedades WHERE id = %s', (propiedad_id,))
    
    conn.commit()
    cur.close()
    conn.close()
    
    flash('Propiedad eliminada exitosamente!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
