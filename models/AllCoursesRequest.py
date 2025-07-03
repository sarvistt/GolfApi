from pydantic import BaseModel

class AllCoursesRequest(BaseModel):
    date: str
    search_time: str
    holes: int
    players: int