from datetime import datetime
from typing import Iterable, Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.db.models import SiteHistory, SiteToCheck
from src.responses import FetchedSiteStatusResponse
from src.services.site_status_fetcher import SiteStatusFetcher


class SiteRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[SiteToCheck]:
        result = await self.db.execute(select(SiteToCheck))
        return result.scalars().all()

    async def _fetch_site_statuses(
        self, sites: Sequence[SiteToCheck]
    ) -> list[FetchedSiteStatusResponse]:
        return await SiteStatusFetcher().fetch_statuses(objects_to_check=sites)

    def _create_site_history_records(
        self, responses: list[FetchedSiteStatusResponse], timestamp: datetime
    ) -> list[SiteHistory]:
        return [
            SiteHistory(
                site_id=resp["site"].id, is_alive=resp["is_alive"], created_at=timestamp
            )
            for resp in responses
        ]

    async def _save_site_history(self, site_history: list[SiteHistory]) -> None:
        self.db.add_all(site_history)
        await self.db.commit()

    async def _get_recent_history_by_ids(
        self, ids: Iterable[int]
    ) -> Sequence[SiteHistory]:
        result = await self.db.execute(
            select(SiteHistory)
            .options(joinedload(SiteHistory.site))
            .filter(SiteHistory.id.in_(ids))
            .order_by(SiteHistory.created_at.desc())
        )
        return result.scalars().all()

    async def fetch_statuses(self) -> Sequence[SiteHistory]:
        sites_to_check = await self.get_all()
        responses = await self._fetch_site_statuses(sites_to_check)

        fetch_time = datetime.now()
        site_history = self._create_site_history_records(responses, fetch_time)

        await self._save_site_history(site_history)

        ids = (history.id for history in site_history)
        history = await self._get_recent_history_by_ids(ids)

        return history

    async def create(self, site_url: str, expected_status_code: int) -> SiteToCheck:
        new_site = SiteToCheck(url=site_url, expected_code=expected_status_code)
        self.db.add(new_site)
        await self.db.commit()
        await self.db.refresh(new_site)
        return new_site

    async def get_by_id(self, site_id: int) -> SiteToCheck:
        result = await self.db.execute(
            select(SiteToCheck).where(SiteToCheck.id == site_id)
        )
        return result.scalar_one()

    async def get_url_by_id(self, site_id: int) -> str:
        site = await self.get_by_id(site_id)
        return site.url

    async def delete_by_id(self, site_id: int) -> bool:
        result = await self.db.execute(
            delete(SiteToCheck).where(SiteToCheck.id == site_id)
        )
        await self.db.commit()
        return result.rowcount > 0
