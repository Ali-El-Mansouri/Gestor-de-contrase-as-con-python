import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
import random
import string
from cryptography.fernet import Fernet

MASTER_PASSWORD = "123ejemplo"  # Puedes cambiarla por la que quieras

# --------- (Password y PasswordManager iguales que antes) ---------

class Password:
    def __init__(self, site, username, password):
        self.site = site
        self.username = username
        self.password = password

    def __str__(self):
        return f"Sitio: {self.site}\nUsuario: {self.username}\nContraseña: {self.password}\n"

    def to_dict(self):
        return {
            'site': self.site,
            'username': self.username,
            'password': self.password
        }

class PasswordManager:
    def __init__(self, filename="passwords.json", key_file="secret.key"):
        self.filename = filename
        self.key_file = key_file
        self.passwords = []
        self.cipher = self.load_key()
        self.load_passwords()


    def load_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        else:
            with open(self.key_file, 'rb') as f:
                key = f.read()
        return Fernet(key)

    def encrypt(self, text):
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt(self, token):
        return self.cipher.decrypt(token.encode()).decode()

    def load_passwords(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.passwords = [
                    Password(
                        item['site'],
                        item['username'],
                        self.decrypt(item['password'])
                    )
                    for item in data
                ]
        else:
            self.passwords = []

    def save_passwords(self):
        with open(self.filename, 'w') as file:
            json.dump([
                {
                    'site': pwd.site,
                    'username': pwd.username,
                    'password': self.encrypt(pwd.password)
                }
                for pwd in self.passwords
            ], file, indent=4)

    def add_password(self, site, username, password):
        new_password = Password(site, username, password)
        self.passwords.append(new_password)
        self.save_passwords()

    def list_passwords(self):
        return [str(pwd) for pwd in self.passwords]

    def find_password(self, site):
        return [str(pwd) for pwd in self.passwords if pwd.site.lower() == site.lower()]

    def delete_password(self, site):
        before = len(self.passwords)
        self.passwords = [pwd for pwd in self.passwords if pwd.site.lower() != site.lower()]
        self.save_passwords()
        return before != len(self.passwords)

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    
    def edit_password(self, site, new_username, new_password):
        found = False
        for pwd in self.passwords:
            if pwd.site.lower() == site.lower():
                pwd.username = new_username
                pwd.password = new_password
                found = True
                break
        if found:
            self.save_passwords()
            return True
        else:
            return False

# --------- (Interfaz Gráfica mejorada) ---------

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Contraseñas")
        self.root.configure(bg="#f0f0f0")  # Fondo claro
        self.edit_button = tk.Button(root, text="✏️ Editar Contraseña", command=self.edit_password, width=25, bg="#9C27B0", fg="white", font=("Arial", 12))
        self.edit_button.pack(pady=5)

        self.manager = PasswordManager()

        title = tk.Label(root, text="Gestor de Contraseñas 🔒", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=10)

        self.add_button = tk.Button(root, text="➕ Añadir Contraseña", command=self.add_password, width=25, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.add_button.pack(pady=5)

        self.list_button = tk.Button(root, text="📄 Listar Contraseñas", command=self.list_passwords, width=25, bg="#2196F3", fg="white", font=("Arial", 12))
        self.list_button.pack(pady=5)

        self.search_button = tk.Button(root, text="🔍 Buscar Contraseña", command=self.search_password, width=25, bg="#FFC107", fg="black", font=("Arial", 12))
        self.search_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="❌ Eliminar Contraseña", command=self.delete_password, width=25, bg="#F44336", fg="white", font=("Arial", 12))
        self.delete_button.pack(pady=5)

        self.output_text = tk.Text(root, height=15, width=60, font=("Arial", 10))
        self.output_text.pack(pady=10)

    def add_password(self):
        site = simpledialog.askstring("Sitio", "Introduce el sitio web:")
        username = simpledialog.askstring("Usuario", "Introduce el nombre de usuario:")

        choice = messagebox.askyesno("Generar contraseña", "¿Quieres que se genere automáticamente?")
        if choice:
            password = self.manager.generate_password()
            messagebox.showinfo("Contraseña generada", f"Tu contraseña segura es:\n{password}")
        else:
            password = simpledialog.askstring("Contraseña", "Introduce tu contraseña:")

        if site and username and password:
            self.manager.add_password(site, username, password)
            messagebox.showinfo("Éxito", "Contraseña añadida correctamente.")

    def list_passwords(self):
        self.output_text.delete('1.0', tk.END)
        passwords = self.manager.list_passwords()
        if passwords:
            for pwd in passwords:
                self.output_text.insert(tk.END, pwd + '\n')
        else:
            self.output_text.insert(tk.END, "No hay contraseñas guardadas.\n")

    def search_password(self):
        site = simpledialog.askstring("Buscar", "Introduce el sitio web a buscar:")
        if site:
            self.output_text.delete('1.0', tk.END)
            results = self.manager.find_password(site)
            if results:
                for res in results:
                    self.output_text.insert(tk.END, res + '\n')
            else:
                self.output_text.insert(tk.END, "No se encontró ninguna contraseña.\n")

    def delete_password(self):
        site = simpledialog.askstring("Eliminar", "Introduce el sitio web a eliminar:")
        if site:
            success = self.manager.delete_password(site)
            if success:
                messagebox.showinfo("Eliminado", "Contraseña eliminada correctamente.")
            else:
                messagebox.showwarning("No encontrado", "No se encontró ninguna contraseña para eliminar.")

    def edit_password(self):
        site = simpledialog.askstring("Editar", "Introduce el sitio web que quieres editar:")
        if site:
            existing = self.manager.find_password(site)
            if existing:
                new_username = simpledialog.askstring("Nuevo Usuario", "Introduce el nuevo nombre de usuario:")
                
                choice = messagebox.askyesno("Generar nueva contraseña", "¿Quieres generar una nueva contraseña automáticamente?")
                if choice:
                    new_password = self.manager.generate_password()
                    messagebox.showinfo("Contraseña generada", f"Nueva contraseña segura:\n{new_password}")
                else:
                    new_password = simpledialog.askstring("Nueva Contraseña", "Introduce la nueva contraseña:")

                if new_username and new_password:
                    success = self.manager.edit_password(site, new_username, new_password)
                    if success:
                        messagebox.showinfo("Actualizado", "Contraseña actualizada correctamente.")
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar la contraseña.")
            else:
                messagebox.showwarning("No encontrado", "No se encontró ninguna contraseña para ese sitio.")


# --------- (Arranque) ---------

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana

    password = simpledialog.askstring("Autenticación", "Introduce la contraseña maestra:", show="*")
    
    if password == MASTER_PASSWORD:
        root.deiconify()  # Mostrar ventana
        app = PasswordManagerGUI(root)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Contraseña incorrecta. Saliendo del programa...")
        root.destroy()