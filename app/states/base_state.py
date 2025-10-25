import reflex as rx
from app.states.scene_state import SceneState
from app.utils.api_client import api_client
import logging


class BaseState(rx.State):
    is_authenticated: bool = False
    invite_code: str = ""
    access_token: str
    auth_mode: str = "login"
    loading: bool = False
    error_message: str = ""

    @rx.event
    def set_auth_mode(self, mode: str):
        self.auth_mode = mode
        self.error_message = ""

    @rx.event
    async def login(self, form_data: dict):
        self.loading = True
        self.error_message = ""
        phone_or_email = form_data.get("phone_or_email", "")
        password = form_data.get("password", "")
        if not phone_or_email or not password:
            self.error_message = "Email and password are required."
            self.loading = False
            return
        try:
            response = await api_client.post(
                "/api/v1/auth/login",
                data={
                    "phone_or_email": phone_or_email,
                    "password": password,
                    "name": "",
                },
            )
            access_token = response.get("access_token")
            if access_token:
                self.access_token = access_token
                self.is_authenticated = True
                self.loading = False
                return rx.redirect("/scene")
            else:
                self.error_message = "Login failed: No access token received."
        except Exception as e:
            logging.exception(f"Login error: {e}")
            if "404" in str(e) and "Not Found" in str(e):
                self.error_message = "User not found. Try a demo user like 'ahmed.khan@scene.com' (pw: test123)"
            else:
                self.error_message = (
                    "Login failed. Please check your credentials and try again."
                )
        finally:
            self.loading = False

    @rx.event
    async def signup(self, form_data: dict):
        self.loading = True
        self.error_message = ""
        name = form_data.get("name", "")
        phone_or_email = form_data.get("phone_or_email", "")
        password = form_data.get("password", "")
        invite_code = form_data.get("invite_code", "")
        if not name or not phone_or_email or (not password):
            self.error_message = "Name, email, and password are required."
            self.loading = False
            return
        try:
            response = await api_client.post(
                "/api/v1/auth/login",
                data={
                    "name": name,
                    "phone_or_email": phone_or_email,
                    "password": password,
                },
            )
            self.auth_mode = "login"
            self.error_message = ""
            rx.toast("Signup successful! Please log in.")
        except Exception as e:
            logging.exception(f"Signup error: {e}")
            self.error_message = "Signup failed. This email may already be in use."
        finally:
            self.loading = False

    @rx.event
    async def logout(self):
        scene_state = await self.get_state(SceneState)
        try:
            await api_client.post("/api/v1/auth/logout", token=self.access_token)
        except Exception as e:
            logging.exception(f"Logout error: {e}")
        finally:
            self.is_authenticated = False
            self.reset()
            scene_state.current_user_id = ""
            return rx.redirect("/")

    @rx.event
    async def check_auth(self):
        if not self.access_token:
            self.is_authenticated = False
            if self.router.page.path != "/":
                is_public_share_page = self.router.page.path.startswith(
                    "/activity/"
                ) or self.router.page.path.startswith("/event/")
                if not is_public_share_page:
                    return rx.redirect("/")
            return
        if not self.is_authenticated:
            try:
                user_data = await api_client.get(
                    "/api/v1/auth/me", token=self.access_token
                )
                if user_data:
                    self.is_authenticated = True
                    if self.router.page.path == "/":
                        return rx.redirect("/scene")
                else:
                    self.is_authenticated = False
                    if self.router.page.path != "/":
                        return rx.redirect("/")
            except Exception as e:
                logging.exception(f"Error checking auth: {e}")
                self.is_authenticated = False
                self.access_token = ""
                if self.router.page.path != "/":
                    return rx.redirect("/")

    @rx.event
    def go_to_scene(self):
        return rx.redirect("/scene")