FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /main

COPY req.txt /main/
RUN pip install --upgrade pip && \
    pip install -r req.txt

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY . /main/
CMD ["gunicorn", "diogram.wsgi:application", "--bind", "0.0.0.0:8000"]