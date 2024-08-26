FROM python:3.12.5 AS builder

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


FROM python:3.12.5-slim

RUN apt-get update && apt-get -y install curl

COPY --from=builder /wheels /wheels
RUN python3 -m pip install --upgrade pip \
    && pip install --no-cache /wheels/*

WORKDIR /src
COPY src/ .

EXPOSE 80

ENTRYPOINT ["python3"]
CMD ["app.py"]
