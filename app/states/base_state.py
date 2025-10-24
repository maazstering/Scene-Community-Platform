import reflex as rx
from app.states.scene_state import SceneState
from app.utils.api_client import api_client
import logging


class BaseState(rx.State):
    is_authenticated: bool = False
    invite_code: str = ""
    access_token: str = ""

    @rx.event
    async def login(self, form_data: dict):
        scene_state = await self.get_state(SceneState)
        phone_or_email = form_data.get("phone_or_email", "")
        name = form_data.get("name", "")
        if not phone_or_email or not name:
            return rx.window_alert("Phone/Email and Name are required.")
        try:
            scene_state.loading = True
            response = await api_client.post(
                "/api/v1/auth/login",
                data={"phone_or_email": phone_or_email, "name": name},
            )
            access_token = response.get("access_token")
            if access_token:
                self.access_token = access_token
                self.is_authenticated = True
                scene_state.loading = False
                return [
                    rx.Cookie(
                        name="access_token",
                        value=access_token,
                        max_age=response.get("expires_in", 3600),
                    ),
                    rx.redirect("/scene"),
                ]
            else:
                scene_state.error_message = "Login failed: No access token received."
        except Exception as e:
            logging.exception(f"Login error: {e}")
            scene_state.error_message = "Login failed. Please try again."
        finally:
            scene_state.loading = False

    @rx.event
    async def logout(self):
        scene_state = await self.get_state(SceneState)
        try:
            await api_client.post("/api/v1/auth/logout", token=self.access_token)
        except Exception as e:
            logging.exception(f"Logout error: {e}")
        finally:
            self.is_authenticated = False
            self.access_token = ""
            scene_state.current_user_id = ""
            return [rx.remove_cookie("access_token"), rx.redirect("/")]

    @rx.event
    async def check_auth(self, cookies: dict[str, str] | None = None):
        token = ""
        if cookies:
            token = cookies.get("access_token", "")
        self.access_token = token
        is_public_share_page = self.router.page.path.startswith(
            "/activity/"
        ) or self.router.page.path.startswith("/event/")
        self.is_authenticated = bool(token)
        if (
            self.router.page.path != "/"
            and (not self.is_authenticated)
            and (not is_public_share_page)
        ):
            return rx.redirect("/")
        if self.router.page.path == "/" and self.is_authenticated:
            return rx.redirect("/scene")

    @rx.event
    def go_to_scene(self):
        return rx.redirect("/scene")