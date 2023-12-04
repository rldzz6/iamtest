from fastapi import FastAPI, Request, status
from mangum import Mangum
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from iamtest.routers.services import service
from iamtest.routers.resources import resource
from iamtest.routers.permissions import permission
from iamtest.routers.groups import group

app = FastAPI()
lambda_handler = Mangum(app)

#라우터 정의
app.include_router(service.router, prefix="/services", tags=["service"])
app.include_router(resource.router, prefix="/resources", tags=["resource"])
app.include_router(permission.router, prefix="/permissions", tags=["permission"])
app.include_router(group.router, prefix="/groups", tags=["group"])

#테스트 코드
@app.get('/')
def root():
    return{'DidimAIM': 'iam.didimservice.com'}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )