### ESVA Backend

Backend for ESVA West's virtual assistant. Currently in development is the inclusion of a vector db to store the data, specifically by implementing chroma db and the integration of metadata for context retrieval.


To run the project it is necessary to set up the necessary environment variables

(el dockerfile puede estar basado en una imagen publica de dockerhub, en la que unicamente se encuentra una imagen base de python con las librerias descargadas, esto con el objetivo de ahorrar tiempo al momento de ejecutar el docker build sobre el contenedor principal.)

Despliegue: 
1. primero es necesario adquirir el archivo env y adjuntarlo al proyecto al mismo nivel que app.py
2. Para un entorno de desarrollo, se puede generar una imagen base sobre la que se van a descargar las librerias necesarias. esta se encuentra en baseContainer, es necesario generarla con el siguiente comando: "docker build -t esva-base-backend ."
3. montar el proyecto en base a la imagen previamente creada: es neceario crear la imagen del proyecto, para esto, a nivel de app.py se ejecuta el siguiente comando: "docker build -t esva-backend ."