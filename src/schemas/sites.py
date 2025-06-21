from pydantic import BaseModel, HttpUrl


class SiteCreateSchema(BaseModel):
    url: HttpUrl
    expected_status_code: int
