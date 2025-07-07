from fastapi import FastAPI, Request

from models.AllCoursesRequest import AllCoursesRequest
from scrapers.ScrapCompiler import ScrapCompiler
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import ValidationError

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Root endpoint
@app.get("/")
@limiter.limit("5/minute")
async def read_root(request: Request):
    return {"message": "Welcome to the Golf API"}


@app.post("/courses")
@limiter.limit("3/minute")  # TODO: prod Limit to 1 requests per minute
async def getAllCourses(request: Request, body: AllCoursesRequest):
    try:
        compiler = ScrapCompiler(request)
        teeData = await compiler.compileAll()
        return teeData
    except ValidationError as e:
        return {"error": "Invalid request data", "details": e.errors()}
