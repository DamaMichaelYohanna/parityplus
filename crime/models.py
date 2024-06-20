from sqlmodel import SQLModel, Field


class Crime(SQLModel, table=True):
    class Config:
        from_attributes = True

    id: int | None = Field(default=None, primary_key=True)
    category: str
    details: str
    name: str | None
    state: str | None
    lga: str | None
    date: str
