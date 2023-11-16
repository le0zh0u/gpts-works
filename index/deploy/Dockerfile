FROM python:3.10.9

WORKDIR /app

COPY ./ ./
COPY .env.prod .env

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install PyMySQL uvicorn
RUN python -m nltk.downloader -d /tmp/llama_index punkt

EXPOSE 8068

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8068"]