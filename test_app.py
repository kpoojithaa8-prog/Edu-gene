import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to EduGenie" in response.text
    print("[PASS] test_homepage passed")

def test_static_css():
    response = client.get("/static/style.css")
    assert response.status_code == 200
    assert "EduGenie" in response.text
    print("[PASS] test_static_css passed")

def test_qa_endpoint():
    response = client.get("/qa?question=What+is+gravity?")
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    print("[PASS] test_qa_endpoint passed. Answer:", data["answer"][:60])

def test_explain_endpoint():
    response = client.post("/explain/", json={"topic": "Gravity"})
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    print("[PASS] test_explain_endpoint passed. Explanation:", data["explanation"][:60])

def test_summarize_endpoint():
    response = client.post("/summarize/", json={"text": "Artificial Intelligence is transforming education."})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    print("[PASS] test_summarize_endpoint passed. Summary:", data["summary"][:60])

def test_quiz_endpoint():
    response = client.post("/quiz", json={"text": "The solar system consists of the sun and eight planets."})
    assert response.status_code == 200
    data = response.json()
    assert "quiz" in data
    print("[PASS] test_quiz_endpoint passed. Quiz length:", len(data["quiz"]))

def test_learning_recommendation_endpoint():
    response = client.get("/learn/recommendations?topic=Python")
    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    print("[PASS] test_learning_recommendation_endpoint passed. Rec:", data["recommendation"][:60])

if __name__ == "__main__":
    print("Starting EduGenie endpoint tests...")
    test_homepage()
    test_static_css()
    test_qa_endpoint()
    test_explain_endpoint()
    test_summarize_endpoint()
    test_quiz_endpoint()
    test_learning_recommendation_endpoint()
    print("=== All EduGenie API endpoint tests passed! ===")

