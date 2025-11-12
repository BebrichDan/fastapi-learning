import pytest
from httpx import AsyncClient, ASGITransport

from my_pydentic import app


LEN_INITIALLY_DATA = 2
SUCCESS_CODE = 200
DEFAULT_TEST_URL = "http://test"
DATA_TEST_BOOK = {"name": "Nazvanie", "author": "AuthorName",}


@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=DEFAULT_TEST_URL,
    ) as ac:
        response = await ac.get("/books")
        assert response.status_code == SUCCESS_CODE

        data = response.json()
        assert len(data['data']) == LEN_INITIALLY_DATA

@pytest.mark.asyncio
async def test_post_books():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=DEFAULT_TEST_URL,
    ) as ac:
        response = await ac.post("/books", json=DATA_TEST_BOOK)
        assert response.status_code == SUCCESS_CODE

        data = response.json()
        assert data["success"] is True