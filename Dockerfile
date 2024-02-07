FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip instal --no-cache-dir -r requirements.txt

COPY . .

CMD ["unicorn", "app.maim:app", "--host", "0.0.0.0" "--port", "8000"]