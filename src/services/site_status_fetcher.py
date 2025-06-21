import asyncio
from abc import ABC, abstractmethod
from typing import Any, Sequence

import httpx

from src.db.models import SiteToCheck
from src.responses import FetchedSiteStatusResponse


class StatusFetcher(ABC):
    @abstractmethod
    def fetch_statuses(self, objects_to_check: Sequence[Any]) -> Any: ...


class SiteStatusFetcher(StatusFetcher):
    def __init__(self) -> None:
        super().__init__()
        self.client = httpx.AsyncClient(verify=False)

    async def fetch_statuses(
        self, objects_to_check: Sequence[SiteToCheck]
    ) -> list[FetchedSiteStatusResponse]:
        """
        Fetch statuses for multiple sites concurrently.

        Args:
            objects_to_check (Sequence[SiteToCheck]): List of sites to check.

        Returns:
            list[FetchedSiteStatusResponse]: List of status responses for each site.
        """
        async with self.client as client:
            tasks = (self.fetch_status(site, client) for site in objects_to_check)
            return await asyncio.gather(*tasks)

    async def fetch_status(
        self, site: SiteToCheck, client: httpx.AsyncClient
    ) -> FetchedSiteStatusResponse:
        """
        Fetch the HTTP status of a given site asynchronously.

        Sends a GET request to the site's URL and compares the HTTP status code
        with the expected status code to determine if the site is alive.

        Args:
            site (SiteToCheck): The site entity containing URL and expected status code.

        Returns:
            FetchedSiteStatusResponse: The result including whether the site is alive,
                                       the site itself, and any error message.
        """
        try:
            response: httpx.Response = await client.get(site.url, timeout=5.0)
            is_alive = response.status_code == site.expected_code
            return FetchedSiteStatusResponse(
                is_alive=is_alive,
                site=site,
            )
        except httpx.RequestError as e:
            return FetchedSiteStatusResponse(
                is_alive=False,
                site=site,
                error=str(e),
            )
        except asyncio.TimeoutError:
            return FetchedSiteStatusResponse(
                is_alive=False,
                site=site,
                error="Request timeout",
            )
