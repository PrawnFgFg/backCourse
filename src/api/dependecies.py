from pydantic import BaseModel
from typing import Annotated
from fastapi import Query, Depends


class PaginationParam(BaseModel):
    page: Annotated[int | None, Query(1, description="Номер страницы", gt=0)]
    per_page: Annotated[int | None, Query(7, description="Количество отелей на стр", gt=1, lt=30)]
    

PaginationDep = Annotated[PaginationParam, Depends()]