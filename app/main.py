from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from .database import SessionLocal
from .crud.product_operations import ProductOperations
from .external_services import SearchManagerFactory
from .schemas.product_schema import ProductSchema
from .schemas.input_schema.pattern_input_schema import Pattern
from .helpers import ConfigHelper
from .exceptions import InvalidInput


config_helper = ConfigHelper("app/app_config.cnf")
config = config_helper.get_config()
db = SessionLocal()
app = FastAPI()
search_manager_factory = SearchManagerFactory(config)
search_manager = search_manager_factory.get_search_manager(SearchManagerFactory.ManagerType.SOLR.value)


@app.get("/product-by-id/{id}")
async def get_product_by_id(id: int):
    try:
        product = ProductOperations.get_product_by_id(db, id)
    except InvalidInput as ex:
        raise HTTPException(HTTPStatus.BAD_REQUEST.value, detail=ex.message)
    return {"message": f"{product.name}"}


@app.post("/products/bulk-upload-to-cluster")
async def bulk_upload_to_cluster():
    products = ProductOperations.get_all_products(db)
    response = search_manager.upload_documents_to_index(products)
    return {"message": response}


@app.get("/products/get-document-by-id/{id}")
async def get_document_by_id(id: int):
    document = search_manager.get_document_by_id(id)
    return document


@app.post("/products/search")
async def get_products_by_pattern(pattern: Pattern):
    try:
        documents = search_manager.get_documents_by_pattern(pattern)
    except InvalidInput as ex:
        raise HTTPException(HTTPStatus.BAD_REQUEST.value, detail=ex.message)
    products = []
    for item in documents:
        _product = search_manager.format_data(item)
        product = ProductSchema(**_product)
        products.append(product)
    return products
