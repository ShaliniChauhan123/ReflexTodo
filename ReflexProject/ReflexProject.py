import reflex as rx


class State(rx.State):
    todos: list = ["hey let's start creating your todos----"]

    def add_todo(self,  form_data: dict[str, str]):
        new_item = form_data.get("new_item")
        if new_item:
            self.todos.append(new_item)

    def remove_todo(self, todo):
        self.todos.remove(todo)


def todo_list(state):
    return rx.cond(
        state.todos,
        rx.foreach(
            state.todos,
            lambda todo: rx.hstack(
                rx.heading(todo, font_size="1.2em"),
                rx.button("Delete", on_click=lambda: state.remove_todo(todo))
            ),
            spacing="1"
        ),
        rx.text("No todos yet.")
    )


def handle_add_todo_click(state, text_input):
    todo_text = text_input.get_value("value")
    if todo_text is not None:
        state.add_todo(todo_text)

def todo_input():
    return rx.form(
        rx.hstack(
            rx.input.root(
                rx.input(
                    name="new_item",
                    placeholder="Add a todo...",
                    bg="white",
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
    return rx.vstack(
        rx.heading("Welcome to Reflex Todo App!", size="3"),
        todo_input(),
        todo_list(State),
        spacing="2"
    )


app = rx.App()
app.add_page(index)