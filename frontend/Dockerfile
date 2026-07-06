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

RUN npm run build

# Etapa 2: Servir con Nginx (Súper ligero)
FROM nginx:alpine AS production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
# Exponemos el puerto 80 del contenedor
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]