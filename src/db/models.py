from datetime import datetime
from typing import List

from sqlalchemy import (
    DateTime,
    ForeignKey,
    SmallInteger,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class SiteHistory(Base):
    __tablename__ = "site_history"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    site_id: Mapped[int] = mapped_column(
        ForeignKey("site_to_check.id", ondelete="CASCADE")
    )
    is_alive: Mapped[bool] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    site: Mapped["SiteToCheck"] = relationship(
        back_populates="history", passive_deletes=True
    )


class SiteToCheck(Base):
    __tablename__ = "site_to_check"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(255), index=True)
    expected_code: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    history: Mapped[List[SiteHistory]] = relationship(
        back_populates="site",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class SiteDowntimeCache(Base):
    __tablename__ = "site_downtime_cache"

    site_id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
