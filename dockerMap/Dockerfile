FROM mysql

# Enviroment variables
ENV MYSQL_DATABASE benignDB

# Put files in image for excecution
COPY createTable.sql /docker-entrypoint-initdb.d/
COPY insertData.sql /docker-entrypoint-initdb.d/