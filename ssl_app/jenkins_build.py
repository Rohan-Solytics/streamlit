import requests

def trigger_jenkins_build( access_key, secret_key, branch_name='your_branch_name',username='nimbus_developer', api_token='nyInDiuVUo'):
    """
    Trigger a Jenkins job build with specified parameters and credentials.
    :param branch_name: Git branch name to pass to the job.
    :param access_key: Access key for additional services.
    :param secret_key: Secret key for additional services.
    :param username: Jenkins username.
    :param api_token: Jenkins API token.
    :return: Response object from the POST request.
    """
    build_url = "https://jenkins.solyticspartners.com/job/NIMBUS/job/NIMBUS-DEV/job/Streamlit/buildWithParameters"
    auth = (username, api_token)

    # Define the parameters to be passed to the Jenkins job
    params = {
        'img_tag': f'streamlit_dev_{branch_name}',
        'release_name': branch_name,
        'branch_name': branch_name,
        'region':'ap-south-1',
        'access_key': access_key,
        'secret_key': secret_key
    }
    
    try:
        response = requests.post(build_url, auth=auth, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response
    except requests.exceptions.RequestException as e:
        print(f"Failed to trigger build: {e}")
        return None


def check_jenkins_build(JOB_NAME,USERNAME,API_TOKEN):
    try:
        wfapi_url = f'{JENKINS_URL}/wfapi/runs'
        auth = (USERNAME, API_TOKEN)
        JENKINS_URL = 'https://jenkins.solyticspartners.com/job/UBO/job/UBO-QA/job/UBO-DEV'
        wfapi_url = f'{JENKINS_URL}/wfapi/runs'
        response = requests.get(wfapi_url, auth=auth)
        response.raise_for_status()
        build_info = response.json()

        if build_info:
            latest_build = build_info[0]  # Get the latest build
            print(f"Build Status: {latest_build['status']}")
        else:
            print("No builds found.")

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve build info: {e}")