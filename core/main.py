import time
from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends,Response,Request
from fastapi.middleware.cors import CORSMiddleware
from tasks.routes import router as tasks_routes
from user.routes import router as users_routes

tags_metadata = [
    {"name":"tasks",
     "description":"Operations related to task management",
     "externalDocs":{
         "description":"More about tasks",
         "url":"http://example.com/docs/tasks"
         }
    }
    ]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(title="Todo Application",
              description="this is a section for description",
              version="0.0.1",
              terms_of_service="http://example.com/terms/",
              contact={
                  "name": "Ali Bigdeli",
                  "url": "https://thealibigdeli.ir/",
                  "email": "bigdeli.ali3@gmail.com",
                },
              license_info={"name": "MIT"},
              lifespan=lifespan,
              openapi_tags=tags_metadata)

app.include_router(tasks_routes, prefix="/api/v1")
app.include_router(users_routes)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()  # زمان شروع پردازش درخواست
    # print("before")
    response = await call_next(request)  # پردازش درخواست توسط FastAPI
    # print("after")
    process_time = time.perf_counter() - start_time  # مدت زمان پردازش محاسبه شود
    response.headers["X-Process-Time"] = str(process_time)  # اضافه کردن هدر به پاسخ برای نمایش مدت زمان اجرای درخواست
    return response

origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # اجازه به همه دامنه‌ها (برای محیط توسعه)
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # اجازه به همه متدها (GET, POST, PUT, DELETE و ...)
    allow_headers=["*"],  # اجازه به همه هدرها
)

# روش یک >> Basic Authentication (احراز هویت پایه)
# کد زیر تست ساده و اولیه برای Basic Authentication بود
# /*from fastapi.security import HTTPBasic,HTTPBasicCredentials

# security = HTTPBasic()

# @app.get("/private")
# def private_route(credentials: HTTPBasicCredentials=Depends(security)):
#     print(credentials)
#     return {"message":"This is a private route."}*/

# /*basic_auth تست ماژول
# from auth.basic_auth import get_authenticated_user
# from user.model import UserModel

# @app.get("/private")
# def private_route(user: UserModel = Depends(get_authenticated_user)):
#     print(user)
#     return {"message":"This is a private route."}*/

# روش دو  >> API Key Authentication  >> با توجه به شرایط دو مدل پیاده سازی دارد
# مدل اول >> API Key Header  
# /*from fastapi.security import APIKeyHeader

# header_scheme = APIKeyHeader(name="x-key")

# @app.get("/private")
# def private_route(api_key = Depends(header_scheme)):
#     print(api_key)
#     return {"message":"This is a private route."}*/

#مدل دوم >> API Key Query(Query Parameter Authentication)
# نمونه url >> http://127.0.0.1:8000/private?x-key=hellooo
# /*from fastapi.security import APIKeyQuery

# query_scheme = APIKeyQuery(name="x-key")

# @app.get("/private")
# def private_route(api_key = Depends(query_scheme)):
#     print(api_key)
#     return {"message":"This is a private route."}*/

# روش سوم >> Token Authentication
# کد زیر تست ساده و اولیه برای Token Authentication بود
# /*from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer

# security = HTTPBearer(scheme_name="Token")

# @app.get("/private")
# def private_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     print(credentials)
#     return {"message":"This is a private route."}*/

# /*token_auth تست ماژول >> Token Authentication
# from auth.token_auth import get_authenticated_user
# from user.model import TokenModel

# @app.get("/private")
# def private_route(user: TokenModel = Depends(get_authenticated_user)):
#     print(user.username)
#     return {"message":"This is a private route."}*/

# jwt_auth تست ماژول >> jwt Authentication
# from auth.jwt_auth import get_authenticated_user

# @app.get("/private")
# def private_route(user = Depends(get_authenticated_user)):
#     print(user.id)
#     return {"message":"This is a private route."}

# @app.get("/public")
# def public_route():
#     return {"message":"This is a public route."}

# تست کوکی
# /*@app.post("/set-cookie")
# def set_cookie(response:Response):
#     response.set_cookie(key="test",value="something")
#     return {"message":"cookie has been set successfully."}

# @app.get("/get-cookie")
# def get_cookie(request:Request):
#     print(request.cookies.get("test"))
#     return {"message":"cookie has been get successfully."}*/
