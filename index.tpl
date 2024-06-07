<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cargar Archivos</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azpwNRM+0qADAC4s6w8Qpgodz28+zcev5t9uUKCrYN7nqKfOplNFsR2+" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha384-KyZXEAg3QhqLMpG8r+Knujsl5+z8T3+to6zB0lNqd2v2+6qzAxB5E6KrFdI5Ighj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-JvF1pN8v3N1w4zsmFsq8U0M8e9s2g0U3JqEHD8g3JlzxC87IVZS6Zt8zDkPF3V+a" crossorigin="anonymous"></script>

</head>
<body>
    <h1>Cargar Archivos</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="upload" accept="*/*" required><br>
        <label for="category">Selecciona una categoría:</label>
        <select id="category" name="category" onchange="updateSubdirectories()">
            <option value="interfaz">Interfaz</option>
            <option value="pantalla">Pantalla</option>
        </select><br>
        <label for="subdirectory">Selecciona un subdirectorio:</label>
        <select id="subdirectory" name="subdirectory">
        </select><br>
        <label for="subsubdirectory">Selecciona un subsubdirectorio:</label>
        <select id="subsubdirectory" name="subsubdirectory">
            <option value=""></option>
        </select><br>
        <input type="submit" value="Cargar">
    </form>

    <!-- Sección para mostrar archivos cargados -->
    <h2>Archivos Cargados</h2>
        <ul>
            % for file_info in files_info:
                <li>
                    % if file_info and 'filename' in file_info:
                        {{ file_info['filename'] }} - Cargado en {{ file_info['directory'] }} el {{ file_info['upload_date'] }}
                    % else:
                        Información del archivo no disponible
                        % end
                        <form action="/delete" method="post" style="display:inline;">
                            <input type="hidden" name="filename" value="{{ file_info['filename'] }}">
                            <input type="hidden" name="directory" value="{{ file_info['directory'] }}">
                            <input type="submit" value="Borrar">
                        </form>
                    </li>
                % end
            </ul>
    
            <script>
                const rootDir = JSON.parse('{{!root_dir}}');
                const subsubdirectories = JSON.parse('{{!subsubdirectories}}');
    
                function updateSubdirectories() {
                                    const category = document.getElementById('category').value;
                const subdirectorySelect = document.getElementById('subdirectory');
                const subsubdirectorySelect = document.getElementById('subsubdirectory');
                const subdirectory = subdirectorySelect.value;
                subdirectorySelect.innerHTML = ''; // Limpiar la lista de subdirectorios
                subsubdirectorySelect.innerHTML = ''; // Limpiar la lista de subsubdirectorios

                if (rootDir[category]) {
                    rootDir[category].forEach(subdir => {
                        subdirectorySelect.innerHTML += `<option value="${subdir}">${subdir}</option>`;
                    });
                }

                updateSubsubdirectories(); // Llamar a la función para actualizar los subsubdirectorios
            }

            function updateSubsubdirectories() {
                const category = document.getElementById('category').value;
                const subdirectory = document.getElementById('subdirectory').value;
                const subsubdirectorySelect = document.getElementById('subsubdirectory');
                subsubdirectorySelect.innerHTML = ''; // Limpiar la lista de subsubdirectorios

                if (subsubdirectories[subdirectory]) {
                    subsubdirectories[subdirectory].forEach(subsubdir => {
                        subsubdirectorySelect.innerHTML += `<option value="${subsubdir}">${subsubdir}</option>`;
                    });
                }
            }

            window.onload = function() {
                updateSubdirectories();
            };
        </script>
</body>
</html>

