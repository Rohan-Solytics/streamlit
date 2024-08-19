FROM 842928376651.dkr.ecr.ap-south-1.amazonaws.com/python:tiangolo-uwsgi-nginx-python3.10
ARG TOKEN
ARG ACCESS_KEY_ID
ARG SECRET_ACCESS_KEY
ARG STORAGE_URL
ARG REGION
ENV STORAGE_URL $STORAGE_URL
ARG ACCESS_KEY_ID
ARG SECRET_ACCESS_KEY
ENV AWS_ACCOUNT_URL=https://sqs.us-east-1.amazonaws.com/842928376651
ENV ACCESS_KEY_ID=$ACCESS_KEY_ID
ENV SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY
COPY requirements.txt ./
COPY . /code
WORKDIR /code

#RUN pip install pip  --upgrade
RUN apt-get update && apt-get install -y python3-pip
RUN apt-get update && apt-get install -y \
    python3  \
    gfortran musl-dev
RUN pip install -r requirements.txt

RUN aws configure set aws_access_key_id $ACCESS_KEY_ID \
    && aws configure set aws_secret_access_key $SECRET_ACCESS_KEY \
    && aws configure set default.region $REGION \
    && aws configure set default.output json
RUN chmod 777 script.sh
CMD ./script.sh