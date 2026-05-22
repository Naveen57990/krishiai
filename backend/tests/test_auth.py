import pytest


@pytest.mark.asyncio
async def test_signup(client, test_user_data):
    response = await client.post("/api/v1/auth/signup", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["full_name"] == test_user_data["full_name"]
    assert "password" not in data


@pytest.mark.asyncio
async def test_signup_duplicate_email(client, test_user_data):
    await client.post("/api/v1/auth/signup", json=test_user_data)
    response = await client.post("/api/v1/auth/signup", json=test_user_data)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login(client, test_user_data):
    await client.post("/api/v1/auth/signup", json=test_user_data)
    response = await client.post("/api/v1/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"],
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client, test_user_data):
    await client.post("/api/v1/auth/signup", json=test_user_data)
    response = await client.post("/api/v1/auth/login", json={
        "email": test_user_data["email"],
        "password": "wrongpassword",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile(client, test_user_data):
    await client.post("/api/v1/auth/signup", json=test_user_data)
    login_resp = await client.post("/api/v1/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"],
    })
    token = login_resp.json()["access_token"]
    response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == test_user_data["email"]
