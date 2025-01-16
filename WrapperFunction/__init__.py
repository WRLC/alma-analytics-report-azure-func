"""
This is the main file for the FastAPI app.
"""
from WrapperFunction.Models.ApiCall import ApiCall
from WrapperFunction.Models.Exceptions import MessageException
from WrapperFunction.Models.Request import Request
from fastapi import FastAPI
from fastapi.responses import JSONResponse

fastapi_app = FastAPI()  # Init FastAPI app


# noinspection PyUnusedLocal
@fastapi_app.exception_handler(MessageException)
async def message_exception_handler(request: Request, exc: MessageException):
    """
    Handle MessageException.

    :param request:
    :param exc:

    :return:
    """
    return JSONResponse(
        status_code=exc.code,
        content={'message': f'{exc.message}'},
    )


@fastapi_app.get("/")
async def root():
    """
    Home page.

    :return: A generic message.
    """
    return {"message": "Hello World"}


# noinspection PyTypeChecker
@fastapi_app.post("/report")
async def get_report(request: Request) -> list[dict[str, str]] or Exception:
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

    if isinstance(data, Exception):
        raise MessageException(500, 'An error occurred while processing the request.')

    return data
