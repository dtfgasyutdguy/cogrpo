# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from .config import LocalFSDatasetIOConfig



    from .datasetio import LocalFSDatasetIOImpl
# async def get_provider_impl(
#     config: LocalFSDatasetIOConfig,
#     _deps,
# ):

    impl = LocalFSDatasetIOImpl(config)
    await impl.initialize()
    return impl
