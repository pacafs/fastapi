from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True): # type: ignore
    __tablename__ = "tasks" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(index=True)
    completed: bool = Field(default=False)
