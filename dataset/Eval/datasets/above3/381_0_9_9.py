# -*- coding: utf-8 -*-
from sqlalchemy.sql.functions import GenericFunction

from datachain.sql.types import Int64
# class rand(GenericFunction):  # noqa: N801
from datachain.sql.utils import compiler_not_implemented



    type = Int64()
    inherit_cache = True


compiler_not_implemented(rand)
