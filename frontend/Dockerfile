# 1. Usamos una imagen de Node.js (la versión estable más reciente)
FROM node:26-slim

# 2. Creamos la carpeta donde vivirá la app dentro de Docker
WORKDIR /app

# 3. Copiamos los archivos de "instrucciones" de las librerías
COPY package*.json ./

# 4. Instalamos las librerías (como axios, vue-router, etc.)
RUN npm install

# 5. Copiamos el resto del código de tu carpeta al contenedor
COPY . .

# 6. Exponemos el puerto que usa Vite por defecto
EXPOSE 5173

# 7. Arrancamos el servidor de desarrollo
# El "--host" es VITAL para que Docker deje ver la web desde fuera
CMD ["npm", "run", "dev", "--", "--host"]