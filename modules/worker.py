import os
from PySide6.QtCore import Signal, QThread, Signal
from sort import system as SortSystem

class WorkerThread(QThread):
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, action_name, path, search_name, cascade, verbose):
        super().__init__()
        self.action_name = action_name
        self.path = str(path)
        self.search_name = search_name
        self.cascade = cascade
        self.verbose = verbose
        self._cancel = False
        self.sys_obj = SortSystem(self.path, False, False, self.search_name, self.cascade, self.verbose )
        self.output_text = ""
        
    def run(self):
        if self._cancel:
            self.finished.emit('Accion cancelada por el usuario!')
            return
        try:
            output_text = self.output_text
            if self._cancel:
                self.finished.emit('Accion cancelada por el usuario!')
                return
            
            if self.action_name == 'search':
                sys_obj = self.sys_obj
                matches = []
                # Implementacion corregida de busqueda
                self.search_files_recursive(self.path, self.search_name, matches)
                if self._cancel:
                    self.finished.emit('Accion cancelada por el usuario!')
                    return
                output_text = '\n'.join(matches) if matches else "No se encontraron coincidencias"
            elif self.action_name == 'sort':
                sys_obj = self.sys_obj
                sys_obj.sort_files(self.path)
                if self._cancel:
                    self.finished.emit('Accion cancelada por el usuario!')
                    return
                output_text = "Ordenacion completada!"
            elif self.action_name == 'unsort':
                sys_obj = self.sys_obj
                sys_obj.un_sort(self.path)
                if self._cancel:
                    self.finished.emit('Accion cancelada por el usuario!')
                    return
                output_text = "Deshacer completado!"
            else:
                output_text = "Accion no reconocida"
            
            if self._cancel:
                self.finished.emit('Accion cancelada por el usuario!')
                return

            if self.verbose and hasattr(sys_obj, 'succeded'):
                verbose_output = []
                for category, items in sys_obj.succeded.items():
                    if items:
                        verbose_output.append(f"\n{category}:")
                        for item in items:
                            verbose_output.append(f"  - {item}")
                if hasattr(sys_obj, 'failed') and sys_obj.failed:
                    verbose_output.append("\nErrores:")
                    for error in sys_obj.failed:
                        verbose_output.append(f"  - {error}")
                        
                if verbose_output:
                    output_text += "\n\nRegistro detallado:" + '\n'.join(verbose_output)
                    
            self.finished.emit(output_text)
                    
        except Exception as e:
            self.error.emit(f"Error durante la ejecucion: {str(e)}")
    
    def cancel(self):
        self._cancel = True
        if hasattr(self, 'sys_obj'):
            self.sys_obj.cancel()
    
    def search_files_recursive(self, directory, target, matches):
        """Funcion de busqueda recursiva corregida"""
        if self._cancel:
            return
        try:
            entries = os.listdir(directory)
        except OSError as e:
            return
        
        for entry in entries:
            if self._cancel:
                return
            full_path = os.path.join(directory, entry)
            if target.lower() in entry.lower():
                matches.append(full_path)
            
            if os.path.isdir(full_path):
                self.search_files_recursive(full_path, target, matches)
