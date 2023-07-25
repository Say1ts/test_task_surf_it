FROM python:3.11
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY . /usr/src/app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8042

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8042"]