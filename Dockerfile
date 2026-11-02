# Build both images from this file:
#   docker build --build-arg ENGINE=python -t sdplamen/armstrong-numbers:python .
#   docker build --build-arg ENGINE=c      -t sdplamen/armstrong-numbers:c .

# Compile the C engine in a separate stage so the final image needs no compiler.
FROM python:3.13-slim AS c-build
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*
COPY armstrong_nums/c_ext/armstrong.c /src/armstrong.c
RUN gcc -O2 -shared -fPIC -o /src/armstrong.so /src/armstrong.c

FROM python:3.13-slim
ARG ENGINE=python
ENV ENGINE=${ENGINE} \
    DEBUG=False \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=c-build /src/armstrong.so armstrong_nums/c_ext/armstrong.so
# Newer than armstrong.c, so the app uses it instead of trying to recompile.
RUN touch armstrong_nums/c_ext/armstrong.so \
    && python manage.py collectstatic --noinput \
    && python manage.py migrate --noinput \
    && useradd --create-home app && chown -R app /app
USER app

EXPOSE 8000
CMD ["gunicorn", "armstrong_numbers.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
