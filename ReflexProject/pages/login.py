import reflex as rx

def login():
    return  rx.form(
        rx.vstack(
            rx.input.root(
                rx.input(
                    name="email_id",
                    placeholder="Enter your email id...",
                    bg="white",
                    style={"border": "1px solid #007bff"}
                ),
                width="100%",
            ),
               rx.input.root(
                rx.input(
                    name="password",
                    placeholder="Enter your password...",
                    bg="white",
                    style={"border": "1px solid #007bff"}
                ),
                width="100%",
            ),
            

            rx.button("Submit"),
        ),
        # on_submit=State.add_todo,
        reset_on_submit=True,
        width="100%",
    )