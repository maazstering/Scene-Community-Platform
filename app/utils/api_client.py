import httpx
import reflex as rx
from typing import Optional
import logging


class APIClient:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.timeout = 30.0

    def _get_headers(self, token: Optional[str] = None) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    async def _handle_response(self, response: httpx.Response):
        try:
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logging.exception(f"HTTP error occurred: {e}")
            raise

    async def get(
        self, endpoint: str, token: Optional[str] = None, params: Optional[dict] = None
    ) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(token),
                params=params,
            )
            return await self._handle_response(response)

    async def post(
        self, endpoint: str, token: Optional[str] = None, data: Optional[dict] = None
    ) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(token),
                json=data,
            )
            return await self._handle_response(response)

    async def patch(
        self, endpoint: str, token: Optional[str] = None, data: Optional[dict] = None
    ) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.patch(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(token),
                json=data,
            )
            return await self._handle_response(response)

    async def delete(self, endpoint: str, token: Optional[str] = None) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.delete(
                f"{self.base_url}{endpoint}", headers=self._get_headers(token)
            )
            return await self._handle_response(response)


api_client = APIClient()