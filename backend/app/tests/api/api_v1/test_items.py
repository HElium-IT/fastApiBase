from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
# import UUID
from app.core.config import settings
from app.tests.utils.item import create_random_item
from app.tests.utils.file_logger import file_logger


@file_logger
def test_create_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


@file_logger
def test_read_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    item = create_random_item(db)
    db.commit()
    response = client.get(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == str(item.id)
    assert content["owner_id"] == str(item.owner_id)
