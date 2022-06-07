FROM python:3.10
 
WORKDIR /app
COPY ./configuration.ini /app/configuration.ini
COPY ./endpoints /app/endpoints
COPY ./hw_engine.py /app/hw_engine.py
COPY ./requirements.txt /app/requirements.txt
COPY ./utils /app/utils
 
RUN pip install -r requirements.txt
 
ENTRYPOINT ["python"]
CMD ["hw_engine.py"]
