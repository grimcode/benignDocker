FROM mysql


# Enviroment variables
ENV MYSQL_DATABASE=benignDB
ENV MYSQL_USER=benignDB
ENV MYSQL_ROOT_PASSWORD=docker
ENV MYSQL_PASSWORD=docker

EXPOSE 3306

# Put files in image for excecution
COPY createTable.sql /docker-entrypoint-initdb.d/
COPY insertData.sql /docker-entrypoint-initdb.d/
