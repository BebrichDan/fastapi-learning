from fastapi import FastAPI, Depends, HTTPException, Response
from authx import AuthX, AuthXConfig
import uvicorn

app = FastAPI(title="My App")

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

@app.post('/login')
def login(username: str, password: str, response: Response):
    if username == "dan" and password == "1337":             # без базы в целях посмотреть как работатет
        token = security.create_access_token(uid=username)
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(401, detail={"message": "Bad credentials"})

@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def get_protected():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("autefication:app", reload=True)