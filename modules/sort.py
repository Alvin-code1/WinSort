import os, sys, optparse, re

class system():
    path = ''
    clear = False
    force = False
    search = False
    cascade = False
    verbose = False
    succeded = {'Directorios previamente ordenados':[], 'Numeracion eliminada':[], 'Ficheros movidos':[],'Renombrados':[]}
    failed = []

    def __init__(self, path, clear, force, search, cascade, verbose):
        self.path = path
        self.clear = clear
        self.force = force
        self.search = search
        self.cascade = cascade
        self.verbose = verbose
        self.cancel_requested = False

    # 1. Verifica si un fichero esta numerado
    def numbered(self,s:str)->bool:
        """Funcion que verifica si el fichero esta numerado"""
        if (s[0].isnumeric() and s[1].isnumeric() and (s[2] == '.' or s[2].isspace)) or (s[0].isnumeric() and (s[1] == '.' or s[1].isspace)):
            return True
        return False

    # 2. Verifica si el directorio ya ha sido ordenado
    def check_sorted(self,s):
        """Funcion que verifica si el directorio esta ordenado"""
        try:
            entries = os.listdir(s)
        except OSError as e:
            self.failed.append(f"Error al acceder al directorio {s}: {e}")
            return
        files = [f for f in entries if os.path.isfile(os.path.join(s,f))]
        for file in files:
            if self.numbered(file) or 'episodio' in file.lower():
                continue
            else:
                return False
        self.succeded['Directorios previamente ordenados'].append(f'El directorio {s} se encuentra ordenado!')
        return True

    # 3. Verifica si hay sub directorios en el directorio actual
    def check_dirs(self,s:str)->bool:
        """Verifica si hay sub directorios en el directorio actual"""
        try:
            entries = os.listdir(s)
        except OSError as e:
            self.failed.append(f"Error al acceder al directorio {s}: {e}")
            return
        files = [f for f in entries if os.path.isdir(os.path.join(s,f))]
        if files:
            return True
        return False

    # 4. Elimina la numeracion de un fichero
    def un_num(self,dir,s:str):
        """Funcion que elimina la numeracion de un fichero"""
        if s[0].isnumeric() and s[1].isnumeric() and (s[2] == '.' or s[2].isspace):
            new_name = s[3:]
        elif s[0].isnumeric() and(s[1] == '.' or s[1].isspace):
            new_name = s[2:]
        else:
            new_name = s
        old_path = os.path.join(dir,s)
        new_path = os.path.join(dir,new_name)
        try:
            os.rename(old_path,new_path)
            self.succeded['Numeracion eliminada'].append(f'Eliminada numeracion de {s}!')
        except OSError as e:
            self.failed.append(f'Error al eliminar numeracion de {s}: {e}')

    # 5. Des ordena el directorio
    def un_sort(self,s):
        """Funcion que des ordena el directorio"""
        if self.cancel_requested:
            print('Accion cancelada')
            return
        cascade = self.cascade
        try:
            entries = os.listdir(s)
        except OSError as e:
            self.failed.append(f"Error al acceder al directorio {s}: {e}")
            return
        files = [f for f in entries if os.path.isfile(os.path.join(s,f))]

        for file in files:
            if self.cancel_requested:
                print('Accion cancelada')
                return
            if self.numbered(file):
                self.un_num(s,file)
        if cascade:
            for entry in entries:
                if self.cancel_requested:
                    print('Accion cancelada')
                    return
                full_path = os.path.join(s,entry)
                if os.path.isdir(full_path):
                    self.un_sort(full_path)
        if self.cancel_requested:
            print('Accion cancelada')
            return

    # 6. Ordena los ficheros en directorio recursivamente
    def sort_files(self,s:str):
        if self.cancel_requested:
            print('Accion cancelada')
            return
        cascade = self.cascade
        """Funcion que ordena los ficheros en directorio recursivamente"""
        if self.check_sorted(s):
            self.un_sort(s)
        if 'anime' in s.lower() or 'serie' in s.lower():
            self.sort_chapter(s)
        else:
            if self.check_srt(s):
                if not (s[-4:] == 'subs'):
                    self.move_srt(s)
            try:
                entries = os.listdir(s)
            except OSError as e:
                self.failed.append(f"Error al acceder al directorio {s}: {e}")
                return
            files = [f for f in entries if os.path.isfile(os.path.join(s,f))]
            sorted_files = 0
            for file in files:
                if self.cancel_requested:
                    print('Accion cancelada')
                    return
                if self.numbered(file):
                    self.un_num(s,file)

            try:
                entries = os.listdir(s)
            except OSError as e:
                self.failed.append(f"Error al acceder al directorio {s}: {e}")
                return
            files = [f for f in entries if os.path.isfile(os.path.join(s,f))]

            for index, file_name in enumerate(files, start= 1):
                if self.cancel_requested:
                    print('Accion cancelada')
                    return
                old_path = os.path.join(s,file_name)
                new_name = f"{index}.{file_name}"
                new_path = os.path.join(s, new_name)

                try:
                    os.rename(old_path,new_path)
                    self.succeded['Renombrados'].append(f"Renomrado de: {old_path} a: {new_path}!")
                    sorted_files += 1
                except OSError as e:
                    self.failed.append(f"Error al renombrar {file_name}!")
            print('*************************************************************************************************************************')
            print('*************************************************************************************************************************')
            print(f"\t\tRenombrados {sorted_files} ficheros de {s}!")
            print('*************************************************************************************************************************')
            print('*************************************************************************************************************************')
            if cascade:
                for entry in entries:
                    if self.cancel_requested:
                        print('Accion cancelada')
                        return
                    full_path = os.path.join(s,entry)
                    if os.path.isdir(full_path):
                        self.sort_files(full_path)
            if self.cancel_requested:
                print('Accion cancelada')
                return

    # 7. Verificar si hay ficheros .srt
    def check_srt(self,s:str):
        """Funcion para verificar si hay ficheros .srt"""
        try:
            entries = os.listdir(s)
        except OSError as e:
            self.failed.append(f"Error al acceder al directorio {s}: {e}")
            return
        files = [f for f in entries if os.path.isfile(os.path.join(s,f))]
        for file in files:
            if self.cancel_requested:
                print('Accion cancelada')
                return
            if file[-4:] == '.srt':
                return True
        return False

    # 8. Mover los ficheros .srt
    def move_srt(self,s:str):
        if self.cancel_requested:
            print('Accion cancelada')
            return
        """Funcion para mover los ficheros .srt"""
        new_path = os.path.join(s,'subs/')
        try:
            os.mkdir(new_path)
        except OSError as e:
            self.failed.append(f'Error al crear el directorio {new_path}: {e}')
        try:
            entries = os.listdir(s)
        except OSError as e:
            self.failed.append(f"Error al acceder al directorio {s}: {e}")
            return
        files = [f for f in entries if os.path.isfile(os.path.join(s,f))]
        for file in files:
            if self.cancel_requested:
                print('Accion cancelada')
                return
            if file[-4:] == '.srt':
                old_path = os.path.join(s,file)
                new_new_path = os.path.join(new_path,file)
                try:
                    os.rename(old_path,new_new_path)
                except OSError as e:
                    self.failed.append(f'Error al mover el fichero {file} al directorio {new_path}: {e}')
                self.succeded['Ficheros movidos'].append(f'El fichero {file} ha sido exitosamente movido a {new_path}!')
        if self.cancel_requested:
            print('Accion cancelada')
            return

    # 9. buscar un directorio y devolver todas las coincidencias
    def search_file(self,matches: list,s:str):
        if self.cancel_requested:
            print('Accion cancelada')
            return
        target = self.search
        """Funcion para buscar un directorio y devolver todas las coincidencias"""
        try:
            entries = os.listdir(s)
        except OSError as e:
            self.failed.append(f"Error al acceder al directorio {s}: {e}")
            return
        files = [f for f in entries]
        for file in files:
            if self.cancel_requested:
                print('Accion cancelada')
                return
            if target in file:
                file_path = os.path.join(s,file)
                matches.append(file_path)
        for entry in entries:
            if self.cancel_requested:
                print('Accion cancelada')
                return
            full_path = os.path.join(s,entry)
            if os.path.isdir(full_path):
                self.search_file(matches,target,full_path)
        if self.cancel_requested:
            print('Accion cancelada')
            return

    # 10. Logs verbose (no se decirlo en spanish)
    def log_verbose(self):
        for succes in self.succeded:
            if len(self.succeded[succes]) > 0:
                print(f'\n{succes}:\n')
            for hit in self.succeded[succes]:
                print(f' - {hit}')
        if len(self.failed) > 0:
            print(f'\nErrores: \n')
            for fail in self.failed:
                print(f' - {fail}')

    # 11. Ordenar capitulos:
    def sort_chapter(self,s:str):
        if self.cancel_requested:
            print('Accion cancelada')
            return
        if self.check_sorted(s):
            self.un_sort(s)
        if self.check_srt(s):
            if not (s[-4:] == 'subs'):
                self.move_srt(s)
        try:
            entries = os.listdir(s)
        except OSError as e:
            self.failed.append(f"Error al acceder al directorio {s}: {e}")
            return
        files = [ f for f in entries if os.path.isfile(os.path.join(s,f))]
        directorie = s[s.rindex('\\') + 1:]
        for file in files:
            episode = re.search(r'\d+',file)
            if episode:
                episode = int(episode.group())
                extention = file[file.rindex('.'):]
                old_path = os.path.join(s,file)
                new_name = f'{directorie} Episodio {episode}{extention}'
                new_path = os.path.join(s,new_name)
                self.succeded['Renombrados'].append(f"Renomrado de: {file} a: {new_path}!")
                try:
                    os.rename(old_path, new_path)
                except OSError:
                    self.failed.append(f"Error al renombrar {file}!")
            if self.cancel_requested:
                print('Accion cancelada')
                return
            
        for entry in entries:
            full_path = os.path.join(s,entry)
            if os.path.isdir(full_path):
                print(full_path)
                self.sort_files(full_path)
            if self.cancel_requested:
                print('Accion cancelada')
                return
        if self.cancel_requested:
            print('Accion cancelada')
            return
        return

    # 12. Funcion de parada
    def cancel(self):
        self.cancel_requested = True

def main():
    opt = optparse.OptionParser()
    opt.add_option('-p', '--path',dest='path',default=os.getcwd()[:3])
    opt.add_option('-c','--clear',action='store_true', dest='clear')
    opt.add_option('-f','--force',action='store_true',dest='force')
    opt.add_option('-s','--search',dest='search',default=False)
    opt.add_option('--cascade', dest='cascade',action='store_true')
    opt.add_option('-v','--verbose', dest='verbose',action='store_true')
    options, args = opt.parse_args()
    target_dir = options.path
    clear = options.clear
    force = options.force
    search = options.search
    cascade = options.cascade
    verbose = options.verbose
    matches = []
    sort = system(target_dir,clear,force,search, cascade,verbose)
    if target_dir and not (search or clear or force):
        if not os.path.isdir(target_dir):
            print(f"La ruta especificada no es un directorio valido: {target_dir}")
            sys.exit(1)
        if not sort.check_sorted(target_dir) or (sort.check_dirs(target_dir) and cascade):
            sort.sort_files(target_dir)
    elif clear:
        if sort.check_sorted(target_dir) or sort.check_dirs(target_dir):
            sort.un_sort(target_dir)
            print('Eliminacion del orden completada!')
        else:
            print("El directorio se encuenta des ordenado. Para ordenar simplemente especifique el path!")
    elif force:
        sort.sort_files(target_dir)
    elif search:
        sort.search_file(matches,target_dir)
        if len(matches) == 0:
            print(f'No se encontraron coincidencias del nombre de archivo o directorio {target_dir}')
        else:
            print('Se encontraron las siguientes coincidencias de directorios o ficheros: \n')
            for match in range(len(matches)):
                print(f'\n{match + 1}. {matches[match]}')
    if sort.verbose:
        sort.log_verbose()

if __name__ == '__main__':
    main()