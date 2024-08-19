FROM python:3.9
WORKDIR /run
 
COPY requirements.txt ./requirements.txt
 
RUN pip3 install -r requirements.txt
 
EXPOSE 8501
 
COPY . /run
 
ENTRYPOINT ["streamlit","run"]
 
CMD ["run.py"]