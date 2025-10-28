from pydantic import BaseModel

class CategoryGroupCreate(BaseModel):
    name: str

class CategoryGroupOut(CategoryGroupCreate):
    id: int
    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str
    group_id: int | None = None
    rollover: bool = True

class CategoryOut(CategoryCreate):
    id: int
    class Config:
        from_attributes = True
