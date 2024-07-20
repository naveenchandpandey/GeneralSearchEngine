from fastapi.testclient import TestClient
import os
os.chdir(os.getcwd() + '/..')

from app.main import app

client = TestClient(app)


def test_get_product_by_id(id=1):
    response = client.get("/product-by-id/" + str(id), headers={})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Milk 200 ml"
    }


def test_invalid_id(id='a'):
    response = client.get("/product-by-id/" + str(id), headers={})
    assert response.status_code == 422
    assert response.json() == {'detail': [{
        'input': 'a',
        'loc': ['path', 'id'],
        'msg': 'Input should be a valid integer, unable to parse string as an integer',
        'type': 'int_parsing'}]}


def test_non_existent_id(id=100000000):
    response = client.get("/product-by-id/" + str(id), headers={})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid product ID: ' + str(id)}


def test_upload_document():
    response = client.post(
        "/products/bulk-upload-to-cluster",
        headers={},
        json={},
    )
    assert response.status_code == 200
    assert response.json() == {'message': True}


def test_search_document():
    response = client.post(
        "/products/search",
        headers={},
        json={
            "name": "milk",
            "description": "dairy"
        },
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            'available': True,
            'description': 'mother dairy milk 200 ml',
            'max_qty': 1,
            'min_qty': 1,
            'name': 'milk 200 ml',
        },
    ]


def test_search_document_with_spelling_mistake():
    response = client.post(
        "/products/search",
        headers={},
        json={
            "name": "milk",
            "description": "dairya"
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'There seems to be misspelling in the input. Please check. '
           "Following are some possible corrections: {'dairy'}"}
