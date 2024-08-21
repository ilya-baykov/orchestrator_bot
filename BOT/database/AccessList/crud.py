from database.AccessList.model import AccessList
from database.base_crud import BaseCRUD


class AccessListCRUD(BaseCRUD):
    model = AccessList
