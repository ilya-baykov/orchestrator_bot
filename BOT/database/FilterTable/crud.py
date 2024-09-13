import logging
from database.FilterTable.model import FilterTable
from database.base_crud import BaseCRUD

logger = logging.getLogger(__name__)


class FilterTableCRUD(BaseCRUD):
    model = FilterTable

