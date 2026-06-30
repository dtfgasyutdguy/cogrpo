from typing import Annotated

# _RepositoryNameQuery = Query(
#     min_length=1,
#     examples=["my-repo"],
#     description="Filter by repository name.",
# )
from fastapi import Query




RepositoryNameQuery = Annotated[str, _RepositoryNameQuery]
OptionalRepositoryNameQuery = Annotated[str | None, _RepositoryNameQuery]
