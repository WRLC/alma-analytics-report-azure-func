"""
ApiCall.py
"""
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from bs4 import BeautifulSoup
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

    def execute(self) -> str or Exception:
        """
        Execute the API call.
        :return: The API response.
        """
        payload = {'limit': '1000', 'col_names': 'true', 'path': self.report_path, 'apikey': self.get_apikey()}
        payload_str = urllib.parse.urlencode(payload, safe=':%')

        try:  # Try to get the report from Alma
            response = requests.get(self.build_path(), params=payload_str)  # Get the report from Alma
            response.raise_for_status()  # Check for errors
        except requests.exceptions.RequestException as e:
            return e

        return response.content

    def soupify(self) -> str or Exception:
        """
        Execute the API call.
        :return: The API response.
        """
        response = self.execute()

        if isinstance(response, Exception):
            return response

        soup = BeautifulSoup(response, 'xml')

        return soup

    def get_columns(self) -> dict[str, str] or Exception:
        """
        Get the headings of all columns.
        :return: A dictionary of column headings.
        """
        soup = self.soupify()

        if isinstance(soup, Exception):
            return soup

        columnlist = soup.find_all('xsd:element')  # Get the columns from the XML response

        if not columnlist:
            return Exception('No columns found in the response.')

        columns = {}
        for column in columnlist:
            columns[column['name']] = column['type']

        return columns

    def get_rows(self) -> list[dict[str, str]] or Exception:
        """
        Get the values of all rows.
        :return: List of dictionaries of row values.
        """

        columns = self.get_columns()

        if isinstance(columns, Exception):
            return [{"message": "No columns found in the response."}]

        soup = self.soupify()

        if isinstance(soup, Exception):
            return [{"message": "No rows found in the response."}]

        rowlist = soup.find_all('row')

        if not rowlist:
            return [{"message": "No rows found in the response."}]

        rows = []

        for row in rowlist:
            rowdict = {}
            for value in row:
                heading = columns[value['name']]
                rowdict[heading] = value.text
            rows.append(rowdict)

        return rows
