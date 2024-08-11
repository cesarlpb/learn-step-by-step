# Usa una imagen oficial de Python
FROM python:3.12

# Instala Git
RUN apt-get update && apt-get install -y git

# Clona el repositorio
RUN git clone https://github.com/cesarlpb/learn-step-by-step.git /usr/src/app

# Establece el directorio de trabajo
WORKDIR /usr/src/app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de Django
EXPOSE 8000

# Comando para iniciar el servidor de desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
