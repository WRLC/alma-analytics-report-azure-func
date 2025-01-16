# alma-analytics-report-azure-func

A FastAPI Azure Function that retrieves an Alma Analytics report and returns its data as a JSON object.

## Environment Variables

The following environment variables are required:

* `KEY_VAULT_NAME`: The name of the Azure Key Vault that stores the Alma API keys.

## Azure Key Vault

The Azure Function uses Azure Key Vault to store Alma API keys as secrets. The secret name is based on the Alma IZ code:
```
<alma-IZ-code>-ALMA-API-KEY
```
The secret value is the Alma API key, which should have Analytics read rights for the institution's production IZ.

## Usage

The Azure Function is triggered by an HTTP POST request to `report` path of the function URL:
    ```
    https://<function-app-name>.azurewebsites.net/api/report
    ```

The request must include the following body parameters:

```json
{
    "path": "<path-to-analytics-report>",
    "iz": "<alma-IZ-code>",
    "region": "<alma-region>"
}
```

* `<path-to-analytics-report>`: the `path` parameter of the Alma Anlytics report's URL
* `<alma-IZ-code>`: the institution's Alma IZ code (this can be whatever your want, but it must match the IZ prefix of an API key's secret name in the Azure Key Vault)
* `<alma-region>`: the Alma region for the Alma IZ. It must be one of the following values:
  * `na` (North America)
  * `eu` (Europe)
  * `ap` (Asia-Pacific)
  * `ca` (Canada)
  * `cn` (China)