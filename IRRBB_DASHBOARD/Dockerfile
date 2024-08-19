FROM python:3.9
ARG TOKEN
ARG REGION
ARG ACCESS_KEY_ID
ARG SECRET_ACCESS_KEY
WORKDIR /run
 
COPY requirements.txt ./requirements.txt
 
RUN pip install git+https://SolyticsdevOps:${TOKEN}@github.com/Nuva-Org/SolyticsUtilsPackage.git@openshift
 
RUN pip3 install -r requirements.txt
 
EXPOSE 8501
 
COPY . /run
 
RUN aws configure set aws_access_key_id $ACCESS_KEY_ID \
&& aws configure set aws_secret_access_key $SECRET_ACCESS_KEY \
&& aws configure set default.region $REGION \
&& aws configure set default.output json
 
ENTRYPOINT ["streamlit","run"]
 
CMD ["run.py"]