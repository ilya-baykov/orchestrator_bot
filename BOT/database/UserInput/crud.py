from database.UserInput.model import UserInput
from database.base_crud import BaseCRUD


class UserInputCRUD(BaseCRUD):
    model = UserInput
