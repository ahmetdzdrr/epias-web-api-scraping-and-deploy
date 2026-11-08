

# Scraping y Despliegue de la API Web de EPİAŞ

![Screenshot 2024-08-28 at 14 52 30](https://github.com/user-attachments/assets/03dc74bf-fa10-4962-8182-84ca1515745d)

Este repositorio proporciona una solución para extraer datos de la API de EPİAŞ (Energy Exchange Istanbul), procesar los datos y desplegar los resultados utilizando Docker, GitHub Actions y Streamlit Cloud.

## Tabla de Contenidos

- [Descripción del Proyecto](#project-overview)
- [Características](#features)
- [Requisitos](#requirements)
- [Instalación](#installation)
- [Uso](#usage)
  - [Ejecutar el Scraper de la API](#running-the-api-scraper)
  - [Desplegar la Aplicación de Streamlit](#deploying-the-streamlit-application)
- [Estructura de Archivos](#file-structure)
- [Flujo de Trabajo de GitHub Actions](#github-actions-workflow)
- [Despliegue con Docker](#docker-deployment)
- [Contribuir](#contributing)
- [Licencia](#license)

## Descripción del Proyecto

![Screenshot 2024-08-29 at 15 15 27](https://github.com/user-attachments/assets/01131e56-1902-4a82-99f6-d7906c9a0f78)


Este proyecto se centra en recuperar datos de la API de EPİAŞ utilizando un script de Python que envía una solicitud POST con un nombre de usuario y contraseña para obtener una clave de ticket. Esta clave se utiliza luego para realizar solicitudes adicionales y recuperar datos específicos. Los datos recopilados se procesan, filtran y muestran mediante una aplicación de Streamlit. Todo el proceso está automatizado y se despliega utilizando Docker y GitHub Actions.

El proyecto también integra la API de OpenStreetMap para enriquecer los datos con coordenadas geográficas (latitud y longitud) para cada ciudad y distrito.

## Características

- **Extracción de Datos**: Recuperar datos de la API de EPİAŞ utilizando una solicitud POST segura.
- **Enriquecimiento de Datos Geográficos**: Utilizar la API de OpenStreetMap para agregar latitud y longitud para cada ciudad y distrito.
- **Filtrado de Datos**: Filtrar los datos recuperados en función de la ciudad y el distrito.
- **Despliegue Automatizado**: Utilizar GitHub Actions para programar la ejecución del script de extracción cada 24 horas y actualizar los datos automáticamente.
- **Integración con Streamlit**: Mostrar los datos filtrados de manera amigable para el usuario mediante una aplicación de Streamlit.
- **Aplicación Contenerizada**: Contenerizar la aplicación usando Docker para facilitar el despliegue y la escalabilidad.

## Requisitos

- Python 3.8+
- Docker
- Cuenta de GitHub
- Credenciales de la API de EPİAŞ (nombre de usuario, contraseña)
- Una conexión a Internet para acceder a la API de OpenStreetMap

## Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/ahmetdzdrr/epias-web-api-scraping-and-deploy.git
   cd epias-web-api-scraping-and-deploy
   ```

2. **Instalar los paquetes de Python requeridos**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar las variables de entorno**:

   Crea un archivo `.env` en el directorio raíz y agrega tus credenciales de la API de EPİAŞ:

   ```env
   USERNAME=your_username
   PASSWORD=your_password
   ```

## Uso

### Ejecutar el Scraper de la API

Para ejecutar manualmente el script de extracción:

```bash
python main.py
```

Esto recuperará los datos más recientes de la API de EPİAŞ, los enriquecerá con datos de latitud y longitud utilizando la API de OpenStreetMap y los guardará localmente.

### Desplegar la Aplicación de Streamlit

Para ejecutar la aplicación de Streamlit localmente:

```bash
streamlit run streamlit.py
```

La aplicación estará disponible en `http://localhost:8501`.

## Estructura de Archivos

```
epias-web-api-scraping-and-deploy/
│
├── .github/workflows/         # GitHub Actions workflow files
├── data/                      # Directory where scraped data is stored
├── Dockerfile                 # Docker configuration file
├── main.py                    # Main script to fetch data from EPİAŞ API
├── requirements.txt           # Python dependencies
├── streamlit.py               # Streamlit application file
└── README.md                  # Project documentation (this file)
```

## Flujo de Trabajo de GitHub Actions

El repositorio incluye un flujo de trabajo de GitHub Actions que ejecuta automáticamente el script `main.py` cada 24 horas. Los datos se recuperan, enriquecen con datos geográficos y se guardan en el directorio `data/`. El archivo de flujo de trabajo se encuentra en `.github/workflows/`.

Para ver o modificar el flujo de trabajo:

```yaml
name: Data Scraping and Deployment

on:
  schedule:
    - cron: "0 0 * * *"  # Runs every 24 hours

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run the scraping script
      run: python main.py
```

## Despliegue con Docker

El proyecto incluye un `Dockerfile` que puede utilizarse para contenerizar la aplicación.

Para construir y ejecutar el contenedor de Docker:

```bash
docker build -t epias-web-api .
docker run -p 8501:8501 epias-web-api
```

La aplicación de Streamlit estará disponible en `http://localhost:8501`.

## Contribuir

¡Las contribuciones son bienvenidas! No dudes en enviar un Pull Request o abrir un Issue.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
