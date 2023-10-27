from fastapi import FastAPI
from fastapi.testclient import TestClient
from api_test.main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_new_method():
    response = client.get("/test")
    assert response.status_code == 200
    
