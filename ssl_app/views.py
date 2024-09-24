import os
import logging
import boto3
import time
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SSLCertificate
from .sslhelper import create_route53_validation_record, update_values_yml
from .jenkins_build import trigger_jenkins_build, check_jenkins_build

# Configure logging
import base64
import re
import requests
from github import Github
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class trigger_jenkins(APIView):
    def post(self, request):
        branch_name=request.data.get('branch_name')  
        username='nimbus_developer'
        api_token='118d2caf04826dbacb68a98f312e94f93e'  
        try: 
            trigger_jenkins_build( branch_name,username, api_token) 
            return Response({"msg":"build trigger successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class check_build(APIView):
    def get(self, request):  
        try:
            username = 'nimbus_developer'
            api_token = '118d2caf04826dbacb68a98f312e94f93e'
            status_message = check_jenkins_build(username, api_token)
            return Response({"status": status_message}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CheckCertificateStatus(APIView):
    def get(self, request):
        certificate_arn = request.query_params.get('arn')
        if not certificate_arn:
            return Response({"error": "Certificate ARN is required"}, status=status.HTTP_400_BAD_REQUEST)     
        try:
            acm_client = boto3.client('acm')
            cert_description = acm_client.describe_certificate(CertificateArn=certificate_arn)
            cert_status = cert_description['Certificate']['Status']   
            return Response({
                "certificate_arn": certificate_arn,
                "status": cert_status
            }, status=status.HTTP_200_OK)       
        except acm_client.exceptions.ResourceNotFoundException:
            return Response({"error": "Certificate not found"}, status=status.HTTP_404_NOT_FOUND)    
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateSSLCertificate(APIView):
    def post(self, request):
        branch_name = request.data.get('branch_name')  
        if not branch_name:
            return Response({"error": "Branch name is required"}, status=status.HTTP_400_BAD_REQUEST) 
        sanitized_branch_name = branch_name.replace('_', '-')
        hostname = f"{sanitized_branch_name}.solytics.us"
        acm_client = boto3.client('acm')  
        try:
            response = acm_client.request_certificate(
                DomainName=hostname,
                ValidationMethod='DNS',
                Options={'CertificateTransparencyLoggingPreference': 'ENABLED'}
            )
            certificate_arn = response['CertificateArn']
            print(f'Certificate ARN: {certificate_arn}')
        except Exception as e:
            return Response({"error": f"Failed to create SSL certificate: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Get the DNS validation records
        retry_count = 0
        max_retries = 10
        dns_records = None
        initial_status = None
        while retry_count < max_retries:
            try:
                cert_details = acm_client.describe_certificate(CertificateArn=certificate_arn)
                initial_status = cert_details['Certificate']['Status']
                if 'DomainValidationOptions' in cert_details['Certificate']:
                    domain_validation_options = cert_details['Certificate']['DomainValidationOptions']
                    if domain_validation_options and 'ResourceRecord' in domain_validation_options[0]:
                        dns_records = domain_validation_options[0]['ResourceRecord']
                        break
                print(f"Attempt {retry_count}: Certificate details retrieved, but DNS records not yet available.")
                retry_count += 1
                time.sleep(5)
            except Exception as e:
                return Response({"error": f"Failed to get validation records: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Create Route 53 records for certificate validation
        zone_id = "Z073211023REDLUYMTKDC"
        try:
            create_route53_validation_record(zone_id, dns_records['Name'], dns_records['Value'])
            print("created Route 53 validation record")
        except Exception as e:
            return Response({"error": f"Failed to create Route 53 validation record: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Create CNAME record to route the hostname
        target_dns_name = "nimbus-dev-streamlit-991053992.ap-south-1.elb.amazonaws.com"
        try:
            create_route53_validation_record(zone_id, hostname, target_dns_name)
            print("created CNAME record")
        except Exception as e:
            return Response({"error": f"Failed to create CNAME record: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        update_values_yml(sanitized_branch_name, hostname, certificate_arn)
        return Response({
            "message": "SSL certificate created and stored successfully",
            "branch_name": branch_name,
            "hostname": hostname,
            "certificate_arn": certificate_arn
        }, status=status.HTTP_201_CREATED)
    
class UpdateYAMLView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        branch_name=data.get('branch_name')
        certificate_arn = data.get('certificateArn')
        name_override = f"streamlit-{branch_name}"
        fullname_override = f"streamlit-{branch_name}"
        host =f"{branch_name}.solytics.us"

        try:
            GITHUB_TOKEN = 'insert token'  # Replace with an actual token for production use
            OWNER = 'Rohan-Solytics'
            REPO_NAME = 'ideal-stream-lit'
            BRANCH = 'test-IRRBB'
            FILE_PATH = 'helm-chart-streamlit/values.yaml'

            # Initialize GitHub API client
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(f"{OWNER}/{REPO_NAME}")
            contents = repo.get_contents(FILE_PATH, ref=BRANCH)
            file_content = base64.b64decode(contents.content).decode('utf-8')
            
            # Update specific lines for the required parameters if provided
            file_content, count = re.subn(
                r'^(nameOverride:\s*).*$', f'nameOverride: "{name_override}"', 
                file_content, flags=re.MULTILINE
            )
            file_content, count = re.subn(
                r'^(fullnameOverride:\s*).*$', f'fullnameOverride: "{fullname_override}"', 
                file_content, flags=re.MULTILINE
            )
            file_content, count = re.subn(
                r'^(.*alb.ingress.kubernetes.io/certificate-arn:\s*).*$', 
                f'alb.ingress.kubernetes.io/certificate-arn: "{certificate_arn}"', 
                file_content, flags=re.MULTILINE
            )
            file_content, count = re.subn(
                r'^(.*host:\s*).*$', 
                f'  host: "{host}"', 
                file_content, flags=re.MULTILINE
            )        
            encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')

            # Prepare data for commit
            commit_message = 'Selective parameter update in values.yaml'
            data = {
                "message": commit_message,
                "content": encoded_content,
                "sha": contents.sha,
                "branch": BRANCH
            }
            url = f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }

            # Send request to update the file on GitHub
            response = requests.put(url, json=data, headers=headers)
            if response.status_code == 200:
                return Response({"message": "File updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to update file", "details": response.json()}, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
