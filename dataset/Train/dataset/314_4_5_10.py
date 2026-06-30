from typing import Annotated

from fastapi import Query




RepositoryNameQuery = Annotated[str, _RepositoryNameQuery]
OptionalRepositoryNameQuery = Annotated[str | None, _RepositoryNameQuery]
