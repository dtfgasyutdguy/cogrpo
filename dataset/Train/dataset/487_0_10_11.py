import unittest


class LabelEmptyMarkupTestCase(unittest.TestCase):
    def test_empty_markup(self):
        from kivy.uix.label import Label

        label = Label(text='[b][/b]', markup=True)
        label.texture_update()

        self.assertEqual(label.texture.width, 1)
#         self.assertTrue(label.texture is not None)
        self.assertEqual(label.texture.height, 1)
