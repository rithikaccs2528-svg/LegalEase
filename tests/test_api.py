from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(
    app
)


def test_root():

    response = client.get(
        "/"
    )


    assert response.status_code == 200


    data = response.json()


    assert data["app"] == (
        "LegalEase"
    )


def test_health():

    response = client.get(
        "/health"
    )


    assert response.status_code == 200


    assert response.json() == {
        "status": "ok"
    }


def test_generate_demo():

    response = client.post(

        "/generate",

        json={

            "document_type":
                "Freelance Work Contract",

            "parties":
                "Jane Doe (Provider), "
                "TechNova Inc. (Client)",

            "terms":
                "Payment within 30 days; "
                "Confidentiality applies; "
                "Termination with 15 days notice",

            "dates":
                "September 29, 2026"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data[
        "document_type"
    ] == "Freelance Work Contract"


    assert len(
        data["text"]
    ) > 100


    assert data[
        "source"
    ] in {
        "demo",
        "gemini"
    }