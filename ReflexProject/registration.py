"""New user registration form and validation logic."""
from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator

import reflex as rx

from sqlmodel import select

from .base_state import State
# from .login import LOGIN_ROUTE, REGISTER_ROUTE
from .user import User


class RegistrationState(State):
    """Handle registration form submission and redirect to login page after registration."""

    success: bool = False
    error_message: str = ""

    async def handle_registration(
        self, form_data
    ): 
        with rx.session() as session:
            email_id = form_data["email_id"]
            if not email_id:
                self.error_message = "Email cannot be empty"
                yield rx.set_focus("email_id")
                return
            # existing_user = session.exec(
            #     select(User).where(User.email_id == email_id)
            # ).one_or_none()
            # if existing_user is not None:
            #     self.error_message = (
            #         f"email_id {email_id} is already registered. Try a different email_id"
            #     )
            #     yield [rx.set_value("email_id", ""), rx.set_focus("email_id")]
            #     return
            password = form_data["password"]
            if not password:
                self.error_message = "Password cannot be empty"
                yield rx.set_focus("password")
                return
          
            # Create the new user and add it to the database.
            new_user = User()  # type: ignore
            new_user.email_id = email_id
            new_user.password_hash = User.hash_password(password)
            new_user.enabled = True
            print('checl',new_user)
            all_users = session.query(User).all()

            # Print the details of each user
            for user in all_users:
                print(f"User ID: {user.id}, Email: {user.email_id}")


            session.add(new_user)
            session.commit()
        # Set success and redirect to login page after a brief delay.
        self.error_message = ""
        self.success = True
        yield
        await asyncio.sleep(0.5)
        yield [rx.redirect("/login"), RegistrationState.set_success(False)]

@rx.page(route="/register")
def registration_page() -> rx.Component:

    register_form = rx.box(
        rx.vstack(
            rx.form(
                rx.fragment(
                    rx.heading("Create an account", size="7", margin_bottom="2rem"),
                    rx.text(
                        "Email_id",
                        color="hsl(240, 5%, 64.9%)",
                        margin_top="2px",
                        margin_bottom="4px",
                    ),
                    rx.input(
                        placeholder="email_id",
                        id="email_id",
                        border_color="hsl(240,3.7%,15.9%)",
                        justify_content="center",
                    ),
                    rx.text(
                        "Password",
                        color="hsl(240, 5%, 64.9%)",
                        margin_top="2px",
                        margin_bottom="4px",
                    ),
                    rx.input(
                        placeholder="password",
                        id="password",
                        border_color="hsl(240,3.7%,15.9%)",
                        justify_content="center",
                        type="password",
                    ),
                  
                    rx.box(
                        rx.button(
                            "Sign up",
                            type="submit",
                            width="100%",
                        ),
                        padding_top="14px",
                    ),
                ),
                on_submit=RegistrationState.handle_registration,
            ),
            rx.link("Login", href="/login"),
            align_items="center"
        ),
        padding="8rem 10rem",
        margin_top="10vh",
        margin_x="auto",
        border="2px solid black",
        border_color="gray.300",
        border_radius=10,
    )

    return rx.fragment(
        register_form
    )