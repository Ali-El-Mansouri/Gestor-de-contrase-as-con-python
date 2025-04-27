# Gestor de Contraseñas 🔒

Proyecto de un **gestor de contraseñas seguro** desarrollado en **Python** con **interfaz gráfica** usando **Tkinter**.

Permite **añadir, buscar, listar, eliminar y editar** contraseñas de forma segura, además de generar contraseñas aleatorias fuertes.

---

## 📜 Características

- Programación orientada a objetos (POO).
- Interfaz gráfica amigable (Tkinter).
- Cifrado seguro de contraseñas usando `cryptography` (Fernet AES).
- Contraseña maestra para proteger el acceso.
- Generador automático de contraseñas seguras.
- Edición de contraseñas guardadas.
- Protección de archivos sensibles mediante `.gitignore`.
- Persistencia de datos en archivo `.json` cifrado.

---

## 🛠️ Tecnologías utilizadas

- Python 3.11
- Tkinter
- Cryptography
- JSON
- Git & GitHub

---

## 🚀 Instalación y uso

1. Clona el repositorio:

```bash
git clone https://github.com/MiUsuario/gestor-contraseñas-python.git
cd gestor-contraseñas-python
```

2. Instala la librería `cryptography`:

```bash
pip install cryptography
```

3. Ejecuta el programa:

```bash
python main.py
```

4. Introduce la **contraseña maestra** para acceder al gestor.

---

## 📂 Archivos importantes

| Archivo            | Descripción                                                   |
|--------------------|----------------------------------------------------------------|
| `main.py`           | Código principal del gestor de contraseñas.                    |
| `passwords.json`    | Archivo cifrado donde se guardan las contraseñas (**no subir**).|
| `secret.key`        | Clave secreta para descifrar las contraseñas (**no subir**).     |
| `.gitignore`        | Ignora automáticamente archivos sensibles.                    |

---

## ⚠️ Importante sobre seguridad

- Nunca subas `secret.key` ni `passwords.json` a repositorios públicos.
- Cambia la contraseña maestra en `main.py` para mejorar la seguridad.

---

## 📄 Licencia

Este proyecto está licenciado bajo [MIT License](https://opensource.org/licenses/MIT).

---

## ✨ Autor

- **Nombre:** Ali El Mansouri
- **GitHub:** [@Ali-El-Mansouri](https://github.com/Ali-El-Mansouri)

---