# MiProyecto

Aplicación básica de Flask con registro e inicio de sesión conectada a MongoDB.

## Requisitos

- Python 3.13+
- MongoDB local o cluster remoto
- Dependencias en `pyproject.toml`

## Instalación

1. Instala las dependencias:

```bash
python -m pip install -e .
```

2. Opcional: define variables de entorno:

- `MONGODB_URI` (por defecto `mongodb://localhost:27017`)
- `SECRET_KEY` (recomendado para sesiones seguras)

En Windows PowerShell:

```powershell
$env:MONGODB_URI = "mongodb://localhost:27017"
$env:SECRET_KEY = "mi_clave_secreta"
```

## Ejecutar

```bash
python main.py
```

Abre `http://127.0.0.1:5000` en tu navegador.

## Características

- Registro de usuario con correo y contraseña
- Inicio de sesión con sesión Flask
- Almacenamiento de usuarios en MongoDB
- Contraseña cifrada con PBKDF2-HMAC-SHA256
