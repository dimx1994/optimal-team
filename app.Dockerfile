FROM python:3.9
COPY requirements.txt /players/
COPY app /players/app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r /players/requirements.txt

WORKDIR /players
ENV PYTHONPATH="${PYTHONPATH}:/players"

CMD ["gunicorn", "--config", "app/gunicorn_config.py", "app.main:app"]