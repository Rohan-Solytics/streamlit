import requests
import time

def trigger_jenkins_build(branch_name,username, api_token):
    """
    Trigger a Jenkins job build with specified parameters and credentials.
    :param branch_name: Git branch name to pass to the job.
    :param username: Jenkins username.
    :param api_token: Jenkins API token.
    """
    build_url = "https://jenkins.solyticspartners.com/job/NIMBUS/job/NIMBUS-DEV/job/Streamlit/buildWithParameters"
    auth = (username, api_token)

    params = {
        'img_tag': f'streamlit_dev_{branch_name}',
        'release_name': branch_name,
        'branch_name': branch_name,
        'region':'ap-south-1',
        'access_key': access_key,
        'secret_key': secret_key
    }
    response = requests.post(build_url, auth=auth, params=params)
    response.raise_for_status() 
    return response

def check_jenkins_build(username, api_token):
    auth = (username, api_token)
    JENKINS_URL = 'https://jenkins.solyticspartners.com/job/NIMBUS/job/NIMBUS-DEV/job/Streamlit'
    wfapi_url = f'{JENKINS_URL}/wfapi/runs'
    status_message = "PENDING"

    while True:
        try:
            response = requests.get(wfapi_url, auth=auth)
            response.raise_for_status()
            build_info = response.json()

            if build_info:
                latest_build = build_info[0]
                status_message = latest_build['status']
                print(f"Build Status: {status_message}")
                if status_message in ["FAILURE", "SUCCESS"]:
                    break
            else:
                status_message = "NO_BUILDS"
                print("No builds found.")
                break
        except requests.exceptions.RequestException as e:
            status_message = f"ERROR: {e}"
            print(f"Failed to retrieve build info: {e}")
            break
        time.sleep(10)

    return status_message