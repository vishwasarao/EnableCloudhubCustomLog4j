import requests


def get_access_token(client, secret):
    token_url = "https://anypoint.mulesoft.com/accounts/api/v2/oauth2/token"
    login_data = {
        "client_id": client,
        "client_secret": secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(token_url, data=login_data)
    access_token = response.json().get("access_token")
    return access_token


def get_logging_status(application_url, headers):
    response = requests.get(application_url, headers=headers)
    data = response.json()
    return data.get("loggingCustomLog4JEnabled", None)


def update_logging_status(application_url, headers, new_value):
    update_data = {"loggingCustomLog4JEnabled": new_value}
    response = requests.put(application_url, headers=headers, json=update_data)
    return response.text


client_id = "352715aa383645caaa1a563f8ae929e4"
client_secret = "693Fa2aAE1Cf4370b8f292c7723732Ec"
env = "5227e08a-7aa1-4827-ad9b-9b58cbacd0a6"
access_token = None

# List of app_names
app_names = ["dev", "test", "prod"]

for app_name in app_names:
    if access_token is None:
        access_token = get_access_token(client_id, client_secret)

    if access_token:
        # Base URL for the application
        application_url = f"https://anypoint.mulesoft.com/cloudhub/api/v2/applications/{app_name}"

        headers = {
            "authorization": f"bearer {access_token}",
            "content-type": "application/json",
            "x-anypnt-env-id": env,
        }

        current_value = get_logging_status(application_url, headers)

        if current_value is not None and current_value is False:
            update_response = update_logging_status(application_url, headers, "true")
            print(f"Update for {app_name}: {update_response}")
        else:
            print(f"No update needed for {app_name}. Current value is already true or unknown.")
    else:
        print("Failed to obtain access token.")
