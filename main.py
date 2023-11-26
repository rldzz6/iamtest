#FastAPI 앱 인스턴스 생성 및 실행, 로깅 실행, db 세션 생성
from fastapi import FastAPI
from mangum import Mangum
from iamtest.routers.services import service
from iamtest.routers.resources import resource
from iamtest.routers.groups import group

app = FastAPI()

#라우터 정의
app.include_router(service.router, prefix="/service", tags=["service"])
app.include_router(resource.router, prefix="/resource", tags=["resource"])
app.include_router(group.router, prefix="/group", tags=["group"])

#테스트 코드
@app.get('/')
def root():
    return{'msg': 'test'}

handler = Mangum(app)