"""
Top-level State for the App.

Authentication data is stored in the base State class so that all substates can
access it for verifying access to event handlers and computed vars.
"""
import datetime

from sqlmodel import select

import reflex as rx

from .auth_session import AuthSession
from .user import User
from typing import List, Dict
from .todo import Todo


AUTH_TOKEN_LOCAL_STORAGE_KEY = "_auth_token"
DEFAULT_AUTH_SESSION_EXPIRATION_DELTA = datetime.timedelta(days=7)


class State(rx.State):
    # The auth_token is stored in local storage to persist across tab and browser sessions.
    auth_token: str = rx.LocalStorage(name=AUTH_TOKEN_LOCAL_STORAGE_KEY)
    todos: List[Dict[str, str]] = [{"text": "Learning", "completed": False}]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        
        # Initialize state variables
        self.todos = []
        self.load_todos()  

    def load_todos(self):
        # Fetch todos from the database
        with rx.session() as session:
            todos = session.exec(select(Todo)).all()
            self.todos=todos
            return todos


    def add_todo(self, form_data: dict[str, str]):
        new_item = form_data.get("new_item")
        user_id = self.authenticated_user.id
        if new_item:
          with rx.session() as session:
            
            session.add(
                Todo(  # type: ignore
                    user_id=user_id,
                    todo=new_item,
                    is_completed=False
                )
            )
            session.commit()
            self.todos.append(                Todo(  # type: ignore
                    user_id=user_id,
                    todo=new_item,
                    is_completed=False
                ))

    def remove_todo(self, todo):
        with rx.session() as session:
            removeTodo = session.exec(
                select(Todo).where(
                    Todo.todo == todo["todo"]
                )
            ).first()
            if(removeTodo):
                 session.delete(removeTodo)
                 session.commit()
            self.todos.remove(todo)

    def toggle_completed(self, todo):
        # Find the index of the todo item in the list
        for idx, item in enumerate(self.todos):
            if item == todo:
                # Toggle the completion status
                self.todos[idx]["completed"] = not self.todos[idx]["completed"]
                break


    @rx.cached_var
    def authenticated_user(self) -> User:
        """The currently authenticated user, or a dummy user if not authenticated.

        Returns:
            A User instance with id=-1 if not authenticated, or the User instance
            corresponding to the currently authenticated user.
        """
        with rx.session() as session:
            result = session.exec(
                select(User, AuthSession).where(
                    AuthSession.session_id == self.auth_token,
                    AuthSession.expiration
                    >= datetime.datetime.now(datetime.timezone.utc),
                    User.id == AuthSession.user_id,
                ),
            ).first()
            if result:
                user, session = result
                return user
        return User(id=-1)  # type: ignore

    @rx.cached_var
    def is_authenticated(self) -> bool:
        """Whether the current user is authenticated.

        Returns:
            True if the authenticated user has a positive user ID, False otherwise.
        """
        return self.authenticated_user.id >= 0

    def do_logout(self) -> None:
        """Destroy AuthSessions associated with the auth_token."""
        with rx.session() as session:
            for auth_session in session.exec(
                select(AuthSession).where(AuthSession.session_id == self.auth_token)
            ).all():
                session.delete(auth_session)
            session.commit()
        self.auth_token = self.auth_token

    def _login(
        self,
        user_id: int,
        expiration_delta: datetime.timedelta = DEFAULT_AUTH_SESSION_EXPIRATION_DELTA,
    ) -> None:
        """Create an AuthSession for the given user_id.

        If the auth_token is already associated with an AuthSession, it will be
        logged out first.

        Args:
            user_id: The user ID to associate with the AuthSession.
            expiration_delta: The amount of time before the AuthSession expires.
        """
        if self.is_authenticated:
            self.do_logout()
        if user_id < 0:
            return
        self.auth_token = self.auth_token or self.router.session.client_token
        with rx.session() as session:
            session.add(
                AuthSession(  # type: ignore
                    user_id=user_id,
                    session_id=self.auth_token,
                    expiration=datetime.datetime.now(datetime.timezone.utc)
                    + expiration_delta,
                )
            )
            session.commit()