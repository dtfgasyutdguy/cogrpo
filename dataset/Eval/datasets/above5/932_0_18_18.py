# -*- coding: utf-8 -*-
class OuterClass:
    class NestedClass:
        def find_me(self):
            pass

    def nested_test(self):
        class WithinMethod:
            pass

        def func_within_func():
# b = OuterClass().NestedClass().find_me()
            pass

        a = self.NestedClass()  # noqa: F841



