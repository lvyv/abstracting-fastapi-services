import logging

from schemas.foo import FooItemCreate
from utils.app_exceptions import AppException
from services.main import AppService, AppCRUD
from models.foo import FooItem
from utils.service_result import ServiceResult
import httpx


class FooService(AppService):
    def create_item(self, item: FooItemCreate) -> ServiceResult:
        foo_item = FooCRUD(self.db).create_item(item)
        if not foo_item:
            return ServiceResult(AppException.FooCreateItem())
        return ServiceResult(foo_item)

    def get_item(self, item_id: int) -> ServiceResult:
        foo_item = FooCRUD(self.db).get_item(item_id)
        if not foo_item:
            return ServiceResult(AppException.FooGetItem({"item_id": item_id}))
        if not foo_item.public:
            return ServiceResult(AppException.FooItemRequiresAuth())
        return ServiceResult(foo_item)

    async def phm_call(self, item_id: str) -> ServiceResult:
        dev_type = 'pump'
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.post(f'http://127.0.0.1:29082/api/v1/soh/{dev_type}?dev_id={item_id}')
            logging.debug(r)
            return ServiceResult(r.content)


class FooCRUD(AppCRUD):
    def create_item(self, item: FooItemCreate) -> FooItem:
        foo_item = FooItem(description=item.description, public=item.public)
        self.db.add(foo_item)
        self.db.commit()
        self.db.refresh(foo_item)
        return foo_item

    def get_item(self, item_id: int) -> FooItem:
        foo_item = self.db.query(FooItem).filter(FooItem.id == item_id).first()
        if foo_item:
            return foo_item
        return None
