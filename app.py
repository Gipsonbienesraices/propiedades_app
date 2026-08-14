from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.utils import secure_filename
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

@app.route('/registrar', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
