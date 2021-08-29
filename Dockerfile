FROM python:3

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD  python3 /app/Get_Data.py
