import sys
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Golf API"}


def test_get_all_courses(monkeypatch):
    class MockCompiler:
        async def compileAll(self):
            return {"result": "success"}

    monkeypatch.setattr("main.ScrapCompiler", lambda req: MockCompiler())

    payload = {
        "date": getCurrentDay(),
        "search_time": "6:00 am",
        "holes": "9",
        "players": "18",
    }

    response = client.post("/courses", json=payload)
    print("RESPONSE:", response.json())
    assert response.status_code == 200
    assert response.json() == {"result": "success"}


def test_getAllCourses_invalid():
    payload = {}
    response = client.post("/courses", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()


def getCurrentDay():
    now = datetime.now(ZoneInfo("America/Winnipeg"))
    weekday = now.strftime("%A")
    month = now.strftime("%b")
    day = now.day
    return f"{weekday}, {month} {day}"
