from pydantic import BaseModel
from typing import List, Optional, Union

class BookDetail(BaseModel):
    key: str
    title: str
    description: Optional[Union[str, dict]]
    subjects: Optional[List[str]]
    authors: Optional[List[dict]]
    covers: Optional[List[int]]
    first_publish_date: Optional[str]
