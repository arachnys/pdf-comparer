FROM python:2.7-alpine

WORKDIR /pdf-comparer/

RUN apk --no-cache add \
    musl-dev \
    gcc \
    jpeg-dev \
    zlib-dev \
    ghostscript

COPY ./ /pdf-comparer/

RUN pip install .

CMD ["python", "setup.py", "test"]