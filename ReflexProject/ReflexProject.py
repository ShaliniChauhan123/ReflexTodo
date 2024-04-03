from typing import List, Dict

import reflex as rx


class State(rx.State):
    todos: List[Dict[str, str]] = [{"text": "Learning", "completed": False}]

    def add_todo(self, form_data: dict[str, str]):
        new_item = form_data.get("new_item")
        if new_item:
            self.todos.append({"text": new_item, "completed": False})

    def remove_todo(self, todo):
        self.todos.remove(todo)

    def toggle_completed(self, todo):
        # Find the index of the todo item in the list
        for idx, item in enumerate(self.todos):
            if item == todo:
                # Toggle the completion status
                self.todos[idx]["completed"] = not self.todos[idx]["completed"]
                break


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
             rx.button("Delete", on_click=lambda: state.remove_todo(todo), color_scheme="ruby"),
              style={"justify-content": "space-between"},
                width="100%"
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


app = rx.App()
app.add_page(index)
