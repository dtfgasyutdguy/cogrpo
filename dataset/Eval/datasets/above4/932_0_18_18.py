# -*- coding: utf-8 -*-
class OuterClass:
    class NestedClass:
        def find_me(self):
            pass

    def nested_test(self):
        class WithinMethod:
            pass

        def func_within_func():
            pass
# b = OuterClass().NestedClass().find_me()

        a = self.NestedClass()  # noqa: F841



