import reflex as rx
from sqlmodel import select

from ..base_state import State
from ..user import User
class LoginState(State):
    """Handle login form submission and redirect to proper routes after authentication."""

    error_message: str = ""
    redirect_to: str = ""

    def on_submit(self, form_data) -> rx.event.EventSpec:
        """Handle login form on_submit.

        Args:
            form_data: A dict of form fields and values.
        """
        self.error_message = ""
        email_id = form_data["email_id"]
        password = form_data["password"]
        with rx.session() as session:
            user = session.exec(
                select(User).where(User.email_id == email_id)
            ).one_or_none()
        if user is None or not user.verify(password):
            self.error_message = "There was a problem logging in, please try again."
            return rx.set_value("password", "")
        if (
            user is not None
            and user.id is not None
            and user.enabled
            and user.verify(password)
        ):
            # mark the user as logged in
            self._login(user.id)
        self.error_message = ""
        return LoginState.redir()  # type: ignore

    def redir(self):
        """Redirect to the redirect_to route if logged in, or to the login page if not."""
        if not self.is_hydrated:
            # wait until after hydration to ensure auth_token is known
            return LoginState.redir()  # type: ignore
        page = self.router.page.path
        print("page",page)
        if not self.is_authenticated and page != "/login":
            self.redirect_to = page
            return rx.redirect("/login")
        elif page == "/login":
            return rx.redirect(self.redirect_to or "/")

@rx.page(route="/login")
def login():
    return  rx.center(
   rx.vstack(
    rx.form(
        rx.vstack(
           rx.flex(
                rx.input.root(
                rx.input(
                    name="email_id",
                    placeholder="Enter your email id...",
                    bg="white",
                    style={"padding":"24px"}
                ),
                width="100%",
                style={"margin-bottom":"24px"}
            ),
               rx.input.root(
                rx.input(
                    name="password",
                    placeholder="Enter your password...",
                    bg="white",
                   style={"padding":"24px"}
                ),
                width="100%",
                style={"margin-bottom":"24px"}
            ),
            

            rx.button("Login", style={"padding":"24px"}),
                        rx.link("Signup", href="/register"),
            style={"flex-direction":"column","width":"100%"}
           )
        ),
        on_submit=LoginState.on_submit,
        reset_on_submit=True,
        width="100%",
    ),
      style={"margin": "80px", "width": "50%","padding":"36px", "border-radius":"12px","background-color":"rgba(237, 231, 225)"}
)
    )

def require_login(page):
    """Decorator to require authentication before rendering a page.

    If the user is not authenticated, then redirect to the login page.

    Args:
        page: The page to wrap.

    Returns:
        The wrapped page component.
    """
    def protected_page():
        return rx.cond(
            State.is_hydrated & State.is_authenticated,
            page(),
            rx.center(
                rx.cond(
                    State.is_authenticated == False,
                   login()
                    ,
                     rx.center(
                        rx.chakra.spinner(on_mount=LoginState.redir)
                    )
                )
            )
        )

    protected_page.__name__ = page.__name__ 
    return protected_page
