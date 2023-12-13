from fastapi import FastAPI, Request, status
from mangum import Mangum
from iamtest.routers.users import user
from iamtest.routers.services import service
from iamtest.routers.resources import resource
from iamtest.routers.permissions import permission
from iamtest.routers.groups import group
from iamtest.models.entity.common import Response

app = FastAPI()
lambda_handler = Mangum(app)

#라우터 정의
app.include_router(service.router, prefix="/services", tags=["service"])
app.include_router(resource.router, prefix="/resources", tags=["resource"])
app.include_router(permission.router, prefix="/permissions", tags=["permission"])
app.include_router(group.router, prefix="/groups", tags=["group"])
app.include_router(user.router, prefix="/users", tags=["user"])

#테스트 코드
@app.get('/')
def root():
    response = Response()
    response.message = 'test site'
    return response
