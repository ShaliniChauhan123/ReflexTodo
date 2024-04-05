from typing import List, Dict

from .pages.login import require_login

from .registration import registration_page as registration_page

import reflex as rx
from .base_state import State


def todo_list(state):
    return rx.cond(
        state.todos,
        rx.foreach(
            state.todos,
            lambda todo: rx.hstack(
                rx.flex(
                    rx.checkbox(
                        name="completed",
                        value=todo["completed"],
                        on_change=lambda value: state.toggle_completed(todo),
                        style={"padding-right": "12px"}
                    ),
                   rx.cond(
                         todo["completed"],
                         rx.heading(todo["text"], font_size="1.2em", color_scheme="blue", style={"text-decoration": "line-through",  "text-decoration-color": "red",
                                     "font-weight": "bold","text-decoration-thickness": "2.5px"}),
                         rx.heading(todo["text"], font_size="1.2em", color_scheme="blue")
                        )
,
                style={"align-items":"center", "justify-content":"center"},
   
                ),
                   rx.button("Delete", on_click=lambda: state.remove_todo(todo), color_scheme="ruby"), style={"justify-content": "space-between"},width="100%"
                ),
             spacing="1",
        ),
        rx.text("No todos yet.")
    )


def todo_input():
    return rx.form(
        rx.hstack(
            rx.input.root(
                rx.input(
                    name="new_item",
                    placeholder="Add a todo...",
                    bg="white",
                    style={"border": "1px solid #007bff"}
                ),
                width="100%",
            ),
            rx.button("Add"),
        ),
        on_submit=State.add_todo,
        reset_on_submit=True,
        width="100%",
    )

@require_login
def index():
    return rx.center(
        rx.vstack(
            rx.heading("Welcome to Reflex Todo App!", size="6", style={"padding-bottom": "24px"}),
            todo_input(),
            todo_list(State),
            spacing="2",
            style={"margin": "60px", "width": "50%","padding":"36px", "border-radius":"12px","background-color":"rgba(237, 231, 225)"}
        )
    )


async def api_test(item_id: int):
    return {"my_result": item_id}


app = rx.App()
app.api.add_api_route("/items/{item_id}", api_test)
# app.api.add_api_route("/register", api_test)
app.add_page(index)
# app.add_page(login)
# app.add_page(registration_page)

