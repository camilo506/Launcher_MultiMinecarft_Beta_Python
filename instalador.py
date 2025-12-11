"""
Instalador Simple y Funcional para MultiMinecraft Launcher
==========================================================

Instalador que funciona correctamente con todos los archivos embebidos.
"""

import os
import sys
import shutil
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading
from pathlib import Path
import json

class MinecraftInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minecraft Launcher - Instalador")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # Variables
        appdata_path = os.getenv('APPDATA')
        if appdata_path is None:
            appdata_path = str(Path.home() / "AppData" / "Roaming")
        self.install_path = tk.StringVar(value=os.path.join(appdata_path, ".MultiMinecraft"))
        self.create_desktop_shortcut = tk.BooleanVar(value=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Título principal
        title_frame = tk.Frame(self.root, bg='#2b2b2b')
        title_frame.pack(fill='x', padx=20, pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🚀 Minecraft Launcher",
            font=('Arial', 20, 'bold'),
            fg='#00ff00',
            bg='#2b2b2b'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Instalador Automático",
            font=('Arial', 12),
            fg='#cccccc',
            bg='#2b2b2b'
        )
        subtitle_label.pack()
        
        # Frame de configuración
        config_frame = tk.LabelFrame(
            self.root,
            text="Configuración de Instalación",
            font=('Arial', 10, 'bold'),
            fg='#00ff00',
            bg='#2b2b2b'
        )
        config_frame.pack(fill='x', padx=20, pady=10)
        
        # Opciones adicionales
        options_frame = tk.Frame(config_frame, bg='#2b2b2b')
        options_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Checkbutton(
            options_frame,
            text="Crear acceso directo en el escritorio",
            variable=self.create_desktop_shortcut,
            font=('Arial', 9),
            fg='#cccccc',
            bg='#2b2b2b',
            selectcolor='#404040',
            activebackground='#2b2b2b',
            activeforeground='#cccccc'
        ).pack(anchor='w')
        
        # Frame de progreso
        self.progress_frame = tk.LabelFrame(
            self.root,
            text="Progreso de Instalación",
            font=('Arial', 10, 'bold'),
            fg='#00ff00',
            bg='#2b2b2b'
        )
        self.progress_frame.pack(fill='x', padx=20, pady=10)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate'
        )
        self.progress_bar.pack(fill='x', padx=10, pady=10)
        
        self.status_label = tk.Label(
            self.progress_frame,
            text="Listo para instalar",
            font=('Arial', 9),
            fg='#cccccc',
            bg='#2b2b2b'
        )
        self.status_label.pack(pady=5)
        
        # Botones
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        self.install_btn = tk.Button(
            button_frame,
            text="🚀 Instalar Launcher",
            command=self.start_installation,
            font=('Arial', 11, 'bold'),
            bg='#00aa00',
            fg='#ffffff',
            padx=20,
            pady=8
        )
        self.install_btn.pack(side='left')
        
        self.cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancelar",
            command=self.root.quit,
            font=('Arial', 11),
            bg='#aa0000',
            fg='#ffffff',
            padx=20,
            pady=8
        )
        self.cancel_btn.pack(side='right')
        
        # Configurar estilo
        self.root.configure(bg='#2b2b2b')
        
    def update_status(self, message):
        """Actualiza el mensaje de estado"""
        self.status_label.config(text=message)
        self.root.update()
    
    def start_installation(self):
        """Inicia el proceso de instalación en un hilo separado"""
        self.install_btn.config(state='disabled')
        self.cancel_btn.config(state='disabled')
        self.progress_bar.start()
        
        # Ejecutar instalación en hilo separado
        thread = threading.Thread(target=self.install_launcher)
        thread.daemon = True
        thread.start()
    
    def install_launcher(self):
        """Instala el launcher de Minecraft"""
        try:
            install_dir = Path(self.install_path.get())
            
            # Crear directorio de instalación
            self.update_status("Creando directorio de instalación...")
            install_dir.mkdir(parents=True, exist_ok=True)
            
            # Copiar archivos del launcher
            self.update_status("Copiando archivos del launcher...")
            self.copy_launcher_data(install_dir)
            
            # Crear acceso directo
            if self.create_desktop_shortcut.get():
                self.update_status("Creando acceso directo en el escritorio...")
                self.create_desktop_shortcut_func(install_dir)
            
            # Crear archivo de configuración
            self.update_status("Configurando launcher...")
            self.create_launcher_config(install_dir)
            
            self.progress_bar.stop()
            self.update_status("✅ Instalación completada exitosamente!")
            
            messagebox.showinfo(
                "Instalación Completada",
                f"El launcher de Minecraft se ha instalado correctamente en:\\n{install_dir}\\n\\n"
                "Puedes iniciarlo desde el acceso directo en el escritorio."
            )
            
            # Habilitar botón de cerrar
            self.cancel_btn.config(text="✅ Cerrar", state='normal')
            
        except Exception as e:
            self.progress_bar.stop()
            self.update_status(f"❌ Error durante la instalación: {str(e)}")
            messagebox.showerror("Error de Instalación", f"Ocurrió un error durante la instalación:\\n{str(e)}")
            self.install_btn.config(state='normal')
            self.cancel_btn.config(state='normal')
    
    def copy_launcher_data(self, install_dir):
        """Copia la carpeta de la aplicación autocontenida."""
        # Determinar la ruta de origen de los datos del launcher
        if getattr(sys, 'frozen', False):
            # Si se ejecuta como un ejecutable de PyInstaller
            source_dir = Path(sys._MEIPASS) / 'MultiMinecraft'
        else:
            # Si se ejecuta como un script .py
            source_dir = Path(__file__).parent / 'dist' / 'MultiMinecraft'

        if not source_dir.exists():
            raise FileNotFoundError(f"No se encontró el directorio de la aplicación: {source_dir}")

        # Copiar la carpeta completa
        shutil.copytree(source_dir, install_dir, dirs_exist_ok=True)

    def create_desktop_shortcut_func(self, install_dir):
        """Crea un acceso directo .url en el escritorio."""
        try:
            desktop = Path.home() / 'Desktop'
            shortcut_file = desktop / 'MultiMinecraft Launcher.url'
            exe_path = install_dir / 'MultiMinecraft.exe'

            if not exe_path.exists():
                print(f"Advertencia: No se encontró {exe_path} para crear el acceso directo.")
                return

            with open(shortcut_file, 'w', encoding='utf-8') as f:
                f.write('[InternetShortcut]\n')
                f.write(f'URL=file:///{exe_path}\n')
                # El icono se tomará del propio .exe
                f.write(f'IconFile={exe_path}\n')
                f.write('IconIndex=0\n')
        except Exception as e:
            print(f"Error creando acceso directo: {e}")
    
    def create_launcher_config(self, install_dir):
        """Crea archivo de configuración inicial"""
        config = {
            "install_path": str(install_dir),
            "installed_version": "1.0.0",
            "install_date": str(Path().cwd()),
            "desktop_shortcut": self.create_desktop_shortcut.get()
        }
        
        with open(install_dir / 'install_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

def main():
    """Función principal del instalador"""
    try:
        app = MinecraftInstaller()
        app.root.mainloop()
    except Exception as e:
        print(f"Error iniciando el instalador: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
