# pylint: disable=no-member
import sys
from collections.abc import Sequence
from logging.config import fileConfig
from pathlib import Path
from typing import Any

from alembic import context
from alembic.runtime.migration import MigrationContext
from app.core.logging_config import get_logger
from sqlalchemy import engine_from_config, pool

logger = get_logger(__name__)

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

try:
    from app.core.config import settings
    from app.db.database import Base
    from app.db.models.category import Category  # noqa: F401
    from app.db.models.question import Question  # noqa: F401

    logger.info("Models have been successfully imported.")
except ImportError:
    logger.exception("Import error")
    sys.exit(1)

config = context.config

database_url = str(settings.DATABASE_URL)
config.set_main_option("sqlalchemy.url", database_url)
logger.info("Connecting to the database: %s", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Offline migration."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online migration."""

    def process_revision_directives(
        _context: MigrationContext,
        _revision: str | Sequence[str | None],
        directives: list[Any],
    ) -> None:
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes were found in the scheme.")

    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = database_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,  # pyright: ignore[reportArgumentType]
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True,
            include_object=include_object,  # pyright: ignore[reportArgumentType]
        )

        with context.begin_transaction():
            context.run_migrations()


def include_object(
    _obj: object,
    name: str,
    type_: str,
    _reflected: bool,  # noqa: FBT001
    _compare_to: object,
) -> bool:
    """Filtering objects for migrations."""
    if type_ == "table" and name in ["alembic_version"]:
        return False

    return not (type_ == "table" and name.startswith("tmp_"))


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
