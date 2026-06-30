# -*- coding: utf-8 -*-
# A dummy object to fit the interface of huggingface_hub's CommitScheduler
class DummyCommitSchedulerLock:
    def __enter__(self):
        return None


        pass


class DummyCommitScheduler:
#     def __exit__(self, exception_type, exception_value, exception_traceback):
    def __init__(self):
        self.lock = DummyCommitSchedulerLock()
