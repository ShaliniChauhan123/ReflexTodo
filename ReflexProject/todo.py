from sqlmodel import Field

import reflex as rx




class Todo(
    rx.Model,
    table=True,  # type: ignore
):
    """A local Todo model with todo_id, todo, is_completed """


    user_id:str=Field(unique=True,nullable=False,index=True)
    todo:str=Field(nullable=False)
    is_completed:bool=Field(nullable=False)

    
