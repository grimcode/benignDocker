FROM mysql

# Enviroment variables
ENV MYSQL_DATABASE benignDB

# Put files in image for excecution
COPY ./sqlScripts/ /docker-entrypoint-initdb.d/

