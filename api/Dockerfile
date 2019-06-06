FROM python:3.6

EXPOSE 80

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV NAME World

# Run test when building the container
RUN chmod 644  test.py

CMD ["python","test.py"]
