"""
This is the main file for the FastAPI app.
"""
import urllib.parse
from WrapperFunction.Models.ApiCall import ApiCall
from WrapperFunction.Models.Request import Request
from fastapi import FastAPI

fastapi_app = FastAPI()  # Init FastAPI app


@fastapi_app.get("/")
async def root():
    """
    Home page.

    :return: A generic message.
    """
    return {"message": "Hello World"}


# noinspection PyTypeChecker
@fastapi_app.post("/report")
async def get_report(request: Request) -> list[dict[str, str]]:
    """
    Get a report from Alma.

    :param request: the request object.

    :return: report data in JSON format.
    """
    path = request.path
    iz = request.iz
    region = request.region

    # Get the report from Alma
    data = ApiCall(region, iz, path).get_rows()

    return data
