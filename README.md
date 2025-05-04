# Preview the app

You can access the app at the following links:

-   **Backend**: [https://lyrical-oath-458519-k1.oa.r.appspot.com/](https://lyrical-oath-458519-k1.oa.r.appspot.com/)
-   **Frontend**: [https://frontend-dot-lyrical-oath-458519-k1.oa.r.appspot.com/](https://frontend-dot-lyrical-oath-458519-k1.oa.r.appspot.com/)

# API Endpoints

# Instalación

## Clonar el repositorio

```
git clone git@github.com:raulisimo/reserweb.git
cd reserweb
```

Dentro de la carpeta de proyecto hay dos carpetas:
1. **backend**: con el código de Python 3 usando FastAPI
2. **frontend**: con el código de Vue 3.

## Crear un entorno virtual

Navegar a la carpeta de backend

    cd backend

Es recomendable usar un entorno virtual.

```
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

## Instalar dependencias

```
pip install -r requirements.txt
```

## Instalar frontend (Vue 3)

Hace falta tener npm para instalar el frontend.

1. Navegar a la carpeta de frontend.

```
cd frontend
```

2.Instalar las dependencias de Vue:

```
npm install
```

# Setup del entorno

Antes de correr la app necesito configrar las siguientes variables de entorno (.env file)

In your project root, create a .env file with the following content:

### General settings

    APP_TITLE="RESERWEB"
    ENVIRONMENT="DEV"
    DEBUG="true" 

# Database settings (for development)

    DATABASE_URL="sqlite:///./test.db"  cadena der conexión a MySQL

