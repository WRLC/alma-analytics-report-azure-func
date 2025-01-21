"""
ApiCall.py
"""
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests
import urllib.parse


class ApiCall:
    """
    An object to create and execute an API call.
    """
    def __init__(self, region: str, iz: str, report_path: str) -> None:
        """
        Initialize the API call object.
        :param iz: The institution code.
        :param report_path: The path to the report.
        """
        self.region = region
        self.iz = iz
        self.report_path = report_path

    def build_path(self) -> str:
        """
        Build the API path.
        :return: The API path.
        """
        path = f'https://api-{self.region}.hosted.exlibrisgroup.com'

        if self.region == 'cn':
            path += '.cn'

        path += '/almaws/v1/analytics/reports'

        return path

    # noinspection PyTypeChecker
    def get_apikey(self) -> str:
        """
        Get the API key from the Azure Key Vault.

        :return: The API key.
        """
        # Get the API key from Key Vault
        keyvaultname = os.environ["KEY_VAULT_NAME"]  # Get the Azure Key Vault name
        kvuri = f"https://{keyvaultname}.vault.azure.net"  # Get the Azure Key Vault URI
        credential = DefaultAzureCredential()  # Get the Azure credentials
        secret_client = SecretClient(vault_url=kvuri, credential=credential)  # Get the Azure Key Vault client

        apikey = secret_client.get_secret(f"{self.iz}-ALMA-API-KEY").value  # Get the API key from the Azure Key Vault

        return apikey

    def execute(self) -> requests.Response or JSONResponse:
        """
        Execute the API call.
        :return: The response from the API call.
        """
        payload = {'limit': '1000', 'col_names': 'true', 'path': self.report_path, 'apikey': self.get_apikey()}
        payload_str = urllib.parse.urlencode(payload, safe=':%')

        try:  # Try to get the report from Alma
            response = requests.get(self.build_path(), params=payload_str)  # Get the report from Alma
        except Exception as e:  # Handle exceptions
            return JSONResponse(
                status_code=500,
                content={'status': 'error', 'message': f'An error occurred: {e}'},
            )

        if response.status_code != 200:  # Check for HTTP errors
            return JSONResponse(
                status_code=response.status_code,
                content={'status': 'error', 'message': f'An error occurred: {response.text}'},
            )

        return response
