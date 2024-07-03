from bottle import Bottle, request, run, template, static_file
import os
import json
from html import escape
from datetime import datetime

app = Bottle()

# Definir la estructura del directorio base
root_dir = {
    'interfaz': ['Capacitacion', 'Migracion', 'Pre-produccion', 'Pruebas'],
    'pantalla': ['Capacitacion', 'Migracion', 'Pre-produccion', 'Pruebas']
}

# Definir los subsubdirectorios por cada subdirectorio
subsubdirectories = {
    'Capacitacion': ['cuentas_medicas', 'ordenes_medicas', 'autorizaciones','prestaciones al modelo'],
    'Migracion': ['subsub1', 'subsub2', 'subsub3', 'subsub4'],
    'Pre-produccion': ['subsub1', 'subsub2', 'subsub3', 'subsub4'],
    'Pruebas': ['subsub1', 'subsub2', 'subsub3', 'subsub4']
}

# Tipos MIME permitidos
ALLOWED_MIME_TYPES = [
    'application/msword',  # .doc
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
    'application/vnd.ms-excel',  # .xls
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
    'application/json',  # .json
    'text/plain'  # .txt
]

# Función para listar archivos dentro del directorio de la aplicación
def list_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.sample'):
                continue
            file_path = os.path.join(root, file)
            upload_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            file_list.append({'filename': file, 'directory': root, 'upload_date': upload_date})
    return file_list

# Función auxiliar para reemplazar el prefijo de un directorio
def replace_prefix(directory, prefix, new_prefix):
    if directory.startswith(prefix):
        return directory.replace(prefix, new_prefix, 1)
    return directory

# Ruta principal que muestra la estructura de directorios
@app.route('/')
def index():
    root_dir_json = json.dumps(root_dir)
    subsubdirectories_json = json.dumps(subsubdirectories)
    
    # Obtener la lista de archivos cargados en el directorio de la aplicación
    files_info = list_files('archivos_cargados')

    return template('index', root_dir=root_dir_json, subsubdirectories=subsubdirectories_json, files_info=files_info, replace_prefix=replace_prefix)

# Ruta para manejar la carga de archivos
@app.route('/upload', method='POST')
def do_upload():
    upload = request.files.get('upload')
    category = request.forms.get('category')
    subdirectory = request.forms.get('subdirectory')
    subsubdirectory = request.forms.get('subsubdirectory')
    save_path = os.path.join('archivos_cargados', category, subdirectory, subsubdirectory, upload.filename)
    
    if upload:
        if upload.content_type not in ALLOWED_MIME_TYPES:
            return '''
                <script>
                    alert('Solo se permite subir archivos de tipo Word, Excel, JSON y TXT.');
                    window.location.href = '/';
                </script>
            '''
        
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        
        # Verificar si el archivo ya existe
        if os.path.exists(save_path):
            return '''
                <script>
                    if (confirm('El archivo ya existe. ¿Deseas sobrescribirlo?')) {
                        // Continuar con la carga y sobrescritura del archivo
                        fetch('/upload', {{
                            method: 'POST',
                            body: new FormData(document.querySelector('form'))
                        }}).then(response => {{
                            if (response.ok) {{
                                alert('Archivo guardado con éxito en {}');
                                location.href = '/'; // Redirigir a la página principal
                            }} else {{
                                alert('Error al guardar el archivo.');
                            }}
                        }});
                    } else {
                        alert('No se sobrescribirá el archivo.');
                        window.location.href = '/';
                    }
                </script>
            '''.format(save_path)
        else:
            upload.save(save_path)
            return '''
                Archivo guardado con éxito en {}<br>
                <button onclick="window.location.href = '/';">Aceptar</button>
            '''.format(save_path)
    else:
        return 'No se pudo guardar el archivo.'

# Ruta para servir archivos estáticos (CSS, JS, etc.)
@app.route('/style.css')
def serve_css():
    return static_file('style.css', root='.')

# Ruta para manejar las solicitudes de eliminación
@app.route('/delete', method='POST')
def delete_file():
    filename = request.forms.get('filename')
    directory = request.forms.get('directory')
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return '''
            Archivo eliminado con éxito.<br>
            <button onclick="window.location.href = '/';">Aceptar</button>
        '''
    else:
        return 'El archivo no existe o no se puede eliminar.'

# Ruta para previsualizar y editar archivos
@app.route('/edit/<filename:path>')
def edit_file(filename):
    # Construir la ruta completa del archivo correctamente
    file_path = os.path.join('archivos_cargados', filename.replace('archivos_cargados/', ''))

    print(f"Intentando editar el archivo en la ruta: {file_path}")

    # Verificar si el archivo existe
    if os.path.exists(file_path):
        # Obtener la extensión del archivo
        _, file_extension = os.path.splitext(filename.lower())

        # Verificar si la extensión está permitida
        allowed_extensions = ['.json', '.txt', '.doc', '.docx', '.xls', '.xlsx']
        if file_extension in allowed_extensions:
            # Leer el contenido del archivo
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Escapar caracteres especiales antes de mostrarlos en la plantilla
            escaped_content = escape(content)
            
            # Renderizar la plantilla de edición con el contenido del archivo
            return template('edit', filename=filename, content=escaped_content)
        else:
            # Si la extensión no está permitida, mostrar un mensaje de error
            print(f"La extensión del archivo '{file_extension}' no está permitida.")
            return '''
                <script>
                    alert('No se puede editar este tipo de archivo. Solo se permiten archivos de tipo JSON, TXT, Word o Excel.');
                    window.location.href = '/';
                </script>
            '''
    else:
        # Si el archivo no existe, mostrar un mensaje de error
        print(f"El archivo '{file_path}' no existe.")
        return '''
            <script>
                alert('El archivo no existe.');
                window.location.href = '/';
            </script>
        '''
    
# Ruta para guardar los cambios en los archivos editados
@app.route('/save', method='POST')
def save_file():
    filename = request.forms.get('filename')
    content = request.forms.get('content')
    file_path = os.path.join('archivos_cargados', filename.replace('archivos_cargados/', ''))

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return '''
            <script>
                alert('Archivo guardado con éxito.');
                window.location.href = '/';
            </script>
        '''
    except Exception as e:
        return f'''
            <script>
                alert('Error al guardar el archivo: {e}');
                window.location.href = '/';
            </script>
        '''

if __name__ == '__main__':
    run(app, host='localhost', port=8080)
