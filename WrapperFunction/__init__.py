"""
This is the main file for the FastAPI app.
"""
from bs4 import BeautifulSoup
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from WrapperFunction.Models.ApiCall import ApiCall
from WrapperFunction.Models.Request import Request

fastapi_app = FastAPI(debug=True)  # Init FastAPI app


@fastapi_app.get("/")
async def root() -> dict[str, str]:
    """
    Home page.

    :return: A generic message.
    """
    return {"message": "Hello World"}


# noinspection PyTypeChecker
@fastapi_app.post("/report", status_code=status.HTTP_200_OK)
async def get_report(request: Request) -> JSONResponse:
    """
    Get a report from Alma.

    :param request: the request object.

    :return: report data in JSON format.
    """
    path = request.path
    iz = request.iz
    region = request.region

    api_call = ApiCall(region, iz, path)
    response = api_call.execute()

    if isinstance(response, JSONResponse):
        return response

    soup = BeautifulSoup(response.content, 'xml')  # Parse the XML response

    if soup.find('error'):  # Check for Alma errors
        return JSONResponse(
            status_code=500,
            content={'status': 'error', 'message': f'An error occurred: {soup.find("error").text}'},
        )

    columnlist = soup.find_all('xsd:element')  # Get the columns from the XML response

    if not columnlist:  # Check for columns
        return JSONResponse(
            status_code=404,
            content={'status': 'error', 'message': 'No data columns in response.'},
        )

    columns = {}  # Create a dictionary of columns
    for column in columnlist:  # Add columns to the dictionary
        columns[column['name']] = column['saw-sql:columnHeading']

    rowlist = soup.find_all('Row')  # Get the rows from the XML response

    if not rowlist:  # Check for rows
        return JSONResponse(
            status_code=404,
            content={'status': 'error', 'message': 'No data rows in response.'},
        )

    rows = []
    for value in rowlist:
        values = {}
        kids = value.findChildren()
        for kid in kids:
            values[kid.name] = kid.text
        rows.append(values)

    return JSONResponse(
        status_code=200,
        content={
            'status': 'success',
            'data': {
                'columns': columns,
                'rows': rows
            }
        },
    )
