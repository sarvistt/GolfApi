from fastapi import FastAPI

from models.AllCoursesRequest import AllCoursesRequest
from scrapers.ScrapCompiler import ScrapCompiler

app = FastAPI()


# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Golf API"}

@app.post("/courses")
async def getAllCourses(request: AllCoursesRequest):
    compiler = ScrapCompiler(request)
    teeData = await compiler.compileAll()
    return teeData
