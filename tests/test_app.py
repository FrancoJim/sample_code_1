import pytest

from sample_1.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_api_returns_breakdown(client):
    resp = client.get("/api/v1/change?amount=1.23")
    assert resp.status_code == 200
    assert resp.get_json() == {
        "total": "1.23",
        "change": [
            {"denom_name": "One Dollar Bill", "count": 1, "denom_amount": "1.00"},
            {"denom_name": "Dime", "count": 2, "denom_amount": "0.10"},
            {"denom_name": "Penny", "count": 3, "denom_amount": "0.01"},
        ],
    }


def test_api_missing_amount(client):
    resp = client.get("/api/v1/change")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


@pytest.mark.parametrize("bad", ["abc", "0", "-5", "nan", "inf", "1e30"])
def test_api_bad_amount_is_400_not_500(client, bad):
    resp = client.get(f"/api/v1/change?amount={bad}")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_index_form_get(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Change Machine" in resp.data


def test_index_form_post(client):
    resp = client.post("/", data={"amount": "5.00"})
    assert resp.status_code == 200
    assert b"Five Dollar Bill" in resp.data


def test_index_form_post_bad_input(client):
    resp = client.post("/", data={"amount": "nan"})
    assert resp.status_code == 400
    assert b"finite" in resp.data


def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}
