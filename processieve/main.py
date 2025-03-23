from fastapi import FastAPI, APIRouter

app = FastAPI()

api_router = APIRouter(
    prefix="/api",
)

@api_router.get('/')
def read_root():
    return {'Hello': 'World'}

app.include_router(api_router)

import processieve.frontend

if __name__ == '__main__':
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
