from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import re
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'tu_clave_secreta_aqui')

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

def extract_youtube_id(url):
    """Extrae el ID del video de YouTube de varios formatos de URL"""
    if not url:
        return None
    
    # Patrones exclusivos para YouTube Shorts (formato vertical)
    patterns = [
        r'youtube\.com\/shorts\/([^&\n?#]+)',   # YouTube Shorts sin www
        r'youtube\.com\/shorts\/([^&\n?#]+)',   # YouTube Shorts con www
        r'youtu\.be\/shorts\/([^&\n?#]+)'     # youtu.be shorts
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

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
            fecha_creacion TEXT NOT NULL,
            youtube_url TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS imagenes (
            id SERIAL PRIMARY KEY,
            propiedad_id INTEGER NOT NULL,
            url TEXT NOT NULL,
            es_principal BOOLEAN DEFAULT FALSE,
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

@app.route('/propiedad/<int:propiedad_id>')
def ver_propiedad(propiedad_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM propiedades WHERE id = %s', (propiedad_id,))
        propiedad = cur.fetchone()
        
        if not propiedad:
            flash('Propiedad no encontrada')
            return redirect(url_for('index'))
        
        # Obtener imágenes
        cur.execute('SELECT url FROM imagenes WHERE propiedad_id = %s ORDER BY es_principal DESC', (propiedad_id,))
        imagenes = cur.fetchall()
        cur.close()
        conn.close()
        
        prop_dict = dict(propiedad)
        prop_dict['imagenes'] = [img['url'] for img in imagenes]
        
        return render_template('ver_propiedad.html', propiedad=prop_dict)
    except Exception as e:
        print(f"Error al ver propiedad: {e}")
        flash('Error al cargar la propiedad')
        return redirect(url_for('index'))

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM propiedades ORDER BY fecha_creacion DESC')
        propiedades = cur.fetchall()
        cur.close()
        conn.close()
        
        # Obtener imágenes para cada propiedad
        propiedades_con_imagenes = []
        for prop in propiedades:
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('SELECT url FROM imagenes WHERE propiedad_id = %s ORDER BY es_principal DESC', (prop['id'],))
                imagenes = cur.fetchall()
                cur.close()
                conn.close()
                prop_dict = dict(prop)
                prop_dict['imagenes'] = [img['url'] for img in imagenes]
                propiedades_con_imagenes.append(prop_dict)
            except Exception as e:
                print(f"Error al obtener imágenes para propiedad {prop['id']}: {e}")
                prop_dict = dict(prop)
                prop_dict['imagenes'] = []
                propiedades_con_imagenes.append(prop_dict)
        
        # Agrupar propiedades por tipo
        propiedades_por_tipo = {
            'Casa': [],
            'Terreno': [],
            'Departamento': [],
            'Otro': []
        }
        
        for prop in propiedades_con_imagenes:
            tipo = prop.get('tipo_propiedad', 'Otro')
            if tipo in propiedades_por_tipo:
                propiedades_por_tipo[tipo].append(prop)
            else:
                propiedades_por_tipo['Otro'].append(prop)
        
        return render_template('index.html', propiedades_por_tipo=propiedades_por_tipo)
    except Exception as e:
        print(f"Error en index: {e}")
        return render_template('index.html', propiedades=[])

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

@app.route('/cambiar_password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    if request.method == 'POST':
        password_actual = request.form['password_actual']
        nueva_password = request.form['nueva_password']
        confirmar_password = request.form['confirmar_password']
        
        # Verificar que la nueva contraseña coincida
        if nueva_password != confirmar_password:
            flash('Las contraseñas nuevas no coinciden')
            return render_template('cambiar_password.html')
        
        # Verificar contraseña actual
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM usuarios WHERE id = %s', (current_user.id,))
        user = cur.fetchone()
        
        if not check_password_hash(user['password_hash'], password_actual):
            flash('La contraseña actual es incorrecta')
            cur.close()
            conn.close()
            return render_template('cambiar_password.html')
        
        # Actualizar contraseña
        nuevo_hash = generate_password_hash(nueva_password)
        cur.execute('UPDATE usuarios SET password_hash = %s WHERE id = %s', 
                   (nuevo_hash, current_user.id))
        conn.commit()
        cur.close()
        conn.close()
        
        flash('Contraseña cambiada exitosamente')
        return redirect(url_for('index'))
    
    return render_template('cambiar_password.html')

@app.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            precio = float(request.form['precio'])
            ubicacion = request.form['ubicacion']
            descripcion = request.form['descripcion']
            recamaras = request.form.get('recamaras')
            banos = request.form.get('banos')
            tipo_propiedad = request.form['tipo_propiedad']
            operacion = 'Venta'
            youtube_url = request.form.get('youtube_url')
            
            # Imágenes desde URLs
            imagen_principal = request.form.get('imagen_principal')
            galeria_urls = request.form.get('galeria_urls')
            
            # Manejar campos opcionales para terrenos
            if tipo_propiedad == 'Terreno':
                recamaras = None
                banos = None
            else:
                recamaras = int(recamaras) if recamaras else None
                banos = int(banos) if banos else None
            
            # Procesar URL de YouTube
            youtube_video_id = None
            if youtube_url:
                youtube_video_id = extract_youtube_id(youtube_url)
            
            fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Guardar propiedad en la base de datos
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO propiedades (titulo, precio, ubicacion, descripcion, recamaras, banos, tipo_propiedad, operacion, fecha_creacion, youtube_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
                (titulo, precio, ubicacion, descripcion, recamaras, banos, tipo_propiedad, operacion, fecha_creacion, youtube_video_id)
            )
            propiedad_id = cur.fetchone()['id']
            
            # Guardar imagen principal si existe
            if imagen_principal:
                cur.execute(
                    'INSERT INTO imagenes (propiedad_id, url, es_principal) VALUES (%s, %s, %s)',
                    (propiedad_id, imagen_principal, True)
                )
            
            # Guardar URLs de galería si existen
            if galeria_urls:
                urls_lista = [url.strip() for url in galeria_urls.split(',') if url.strip()]
                for url in urls_lista:
                    cur.execute(
                        'INSERT INTO imagenes (propiedad_id, url, es_principal) VALUES (%s, %s, %s)',
                        (propiedad_id, url, False)
                    )
            
            conn.commit()
            cur.close()
            conn.close()
            
            flash('Propiedad registrada exitosamente!')
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error al registrar propiedad: {e}")
            flash('Error al registrar la propiedad. Por favor intenta nuevamente.')
            return redirect(url_for('index'))
    
    return render_template('registrar.html')

@app.route('/editar/<int:propiedad_id>', methods=['GET', 'POST'])
@login_required
def editar(propiedad_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM propiedades WHERE id = %s', (propiedad_id,))
        propiedad = cur.fetchone()
        
        if not propiedad:
            flash('Propiedad no encontrada')
            return redirect(url_for('index'))
        
        print(f"Propiedad obtenida: {propiedad}")
        
        # Obtener imágenes actuales con manejo de errores para compatibilidad
        imagenes_actuales = []
        try:
            # Primero intentar con columnas nuevas
            cur.execute('SELECT * FROM imagenes WHERE propiedad_id = %s', (propiedad_id,))
            rows = cur.fetchall()
            print(f"Imágenes obtenidas: {len(rows)}")
            print(f"Filas de imágenes: {rows}")
            
            # Procesar resultados para asegurar que tengan las columnas esperadas
            for row in rows:
                print(f"Procesando fila: {row}")
                if 'url' in row:
                    imagenes_actuales.append(row)
                elif 'ruta' in row:
                    # Convertir formato antiguo a nuevo
                    row_dict = dict(row)
                    row_dict['url'] = row_dict['ruta']
                    row_dict['es_principal'] = row_dict.get('es_principal', False)
                    imagenes_actuales.append(row_dict)
                else:
                    print(f"Fila sin columnas esperadas: {row.keys()}")
                    
        except Exception as e:
            print(f"Error al obtener imágenes: {e}")
            imagenes_actuales = []
        
        print(f"Imágenes actuales procesadas: {len(imagenes_actuales)}")
        print(f"Imágenes actuales: {imagenes_actuales}")
        
        cur.close()
        conn.close()
        
        if request.method == 'POST':
            try:
                titulo = request.form['titulo']
                precio = float(request.form['precio'])
                ubicacion = request.form['ubicacion']
                descripcion = request.form['descripcion']
                recamaras = request.form.get('recamaras')
                banos = request.form.get('banos')
                tipo_propiedad = request.form['tipo_propiedad']
                operacion = 'Venta'
                youtube_url = request.form.get('youtube_url')
                
                # Imágenes desde URLs
                imagen_principal = request.form.get('imagen_principal')
                galeria_urls = request.form.get('galeria_urls')
                
                if tipo_propiedad == 'Terreno':
                    recamaras = None
                    banos = None
                else:
                    recamaras = int(recamaras) if recamaras else None
                    banos = int(banos) if banos else None
                
                # Procesar URL de YouTube
                youtube_video_id = None
                if youtube_url:
                    youtube_video_id = extract_youtube_id(youtube_url)
                
                # Actualizar propiedad
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    'UPDATE propiedades SET titulo = %s, precio = %s, ubicacion = %s, descripcion = %s, recamaras = %s, banos = %s, tipo_propiedad = %s, youtube_url = %s WHERE id = %s',
                    (titulo, precio, ubicacion, descripcion, recamaras, banos, tipo_propiedad, youtube_video_id, propiedad_id)
                )
                
                # Eliminar imágenes seleccionadas
                imagenes_a_eliminar = request.form.getlist('eliminar_imagenes')
                for img_id in imagenes_a_eliminar:
                    try:
                        cur.execute('DELETE FROM imagenes WHERE id = %s', (img_id,))
                    except Exception as e:
                        print(f"Error al eliminar imagen {img_id}: {e}")
                
                # Actualizar o agregar imagen principal
                if imagen_principal:
                    try:
                        # Verificar si ya existe imagen principal
                        cur.execute('SELECT id FROM imagenes WHERE propiedad_id = %s AND es_principal = TRUE', (propiedad_id,))
                        existing_principal = cur.fetchone()
                        
                        if existing_principal:
                            cur.execute('UPDATE imagenes SET url = %s WHERE id = %s', (imagen_principal, existing_principal['id']))
                        else:
                            cur.execute(
                                'INSERT INTO imagenes (propiedad_id, url, es_principal) VALUES (%s, %s, %s)',
                                (propiedad_id, imagen_principal, True)
                            )
                    except Exception as e:
                        print(f"Error al actualizar imagen principal: {e}")
                
                # Actualizar galería de imágenes
                if galeria_urls:
                    try:
                        # Eliminar imágenes de galería existentes
                        cur.execute('DELETE FROM imagenes WHERE propiedad_id = %s AND es_principal = FALSE', (propiedad_id,))
                        
                        # Agregar nuevas URLs de galería
                        urls_lista = [url.strip() for url in galeria_urls.split(',') if url.strip()]
                        for url in urls_lista:
                            cur.execute(
                                'INSERT INTO imagenes (propiedad_id, url, es_principal) VALUES (%s, %s, %s)',
                                (propiedad_id, url, False)
                            )
                    except Exception as e:
                        print(f"Error al actualizar galería: {e}")
                
                conn.commit()
                cur.close()
                conn.close()
                
                flash('Propiedad actualizada exitosamente!')
                return redirect(url_for('index'))
                    
            except Exception as e:
                print(f"Error al actualizar propiedad: {e}")
                flash('Error al actualizar la propiedad. Por favor intenta nuevamente.')
                return redirect(url_for('index'))
        
        print(f"Renderizando editar.html con propiedad: {propiedad} y imagenes: {imagenes_actuales}")
        return render_template('editar.html', propiedad=propiedad, imagenes=imagenes_actuales)
        
    except Exception as e:
        print(f"Error en editar: {e}")
        import traceback
        traceback.print_exc()
        flash('Error al cargar la propiedad para edición')
        return redirect(url_for('index'))

@app.route('/eliminar/<int:propiedad_id>', methods=['POST'])
@login_required
def eliminar(propiedad_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Eliminar imágenes de la base de datos
        cur.execute('DELETE FROM imagenes WHERE propiedad_id = %s', (propiedad_id,))
        
        # Eliminar propiedad
        cur.execute('DELETE FROM propiedades WHERE id = %s', (propiedad_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        flash('Propiedad eliminada exitosamente!')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error al eliminar propiedad: {e}")
        flash('Error al eliminar la propiedad')
        return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
