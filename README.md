# Gestión Documental CMC

Este proyecto es un sistema de gestión documental para la institución CMC.

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/josemiguelmm1987/gestion_documental_cmc.git
    ```
2. Crea un entorno virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4. Ejecuta las migraciones:
    ```bash
    python manage.py migrate
    ```
5. Inicia el servidor de desarrollo:
    ```bash
    python manage.py runserver
    ```