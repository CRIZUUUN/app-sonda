from bottle import Bottle, request, run, template, static_file
import os
import json
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


# Ruta principal que muestra la estructura de directorios
@app.route('/')
def index():
    root_dir_json = json.dumps(root_dir)
    subsubdirectories_json = json.dumps(subsubdirectories)
    
    # Obtener la lista de archivos cargados en el directorio de la aplicación
    files_info = list_files('archivos_cargados')

    return template('index', root_dir=root_dir_json, subsubdirectories=subsubdirectories_json, files_info=files_info)

# Ruta para manejar la carga de archivos
@app.route('/upload', method='POST')
def do_upload():
    upload = request.files.get('upload')
    category = request.forms.get('category')
    subdirectory = request.forms.get('subdirectory')
    subsubdirectory = request.forms.get('subsubdirectory')
    save_path = os.path.join('archivos_cargados', category, subdirectory, subsubdirectory, upload.filename)
    
    if upload:
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        upload.save(save_path)
        return 'Archivo guardado con éxito en {}'.format(save_path)
    else:
        return 'No se pudo guardar el archivo.'

# Ruta para servir archivos estáticos (CSS, JS, etc.)
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')

# Ruta para manejar las solicitudes de eliminación
@app.route('/delete', method='POST')
def delete_file():
    filename = request.forms.get('filename')
    directory = request.forms.get('directory')
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return 'Archivo eliminado con éxito.'
    else:
        return 'El archivo no existe o no se puede eliminar.'
    
if __name__ == '__main__':
    run(app, host='localhost', port=8080)