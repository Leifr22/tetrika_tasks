import inspect
import unittest
def strict(func):
    sig=inspect.signature(func)
    def wrapper(*args,**kwargs):
        bound=sig.bind(*args,**kwargs)
        bound.apply_defaults()

        for n,v in bound.arguments.items():
            expected_type = sig.parameters[n].annotation
            if expected_type is not inspect._empty:
                if type(v) is not expected_type:
                    raise TypeError(
                        f"Argument '{n}' must be {expected_type.__name__}, got {type(v).__name__}"
                    )
        return func(*args,**kwargs)
    return wrapper
@strict
def sum_two(a: int, b: int) -> int:
    return a + b

# print(sum_two(1, 2))
# print(sum_two(1, 2.4))


class TestDecorator(unittest.TestCase):
    def test_first(self):
        with self.assertRaises(TypeError):
            sum_two(3,2.6)
    def test_second(self):
        with self.assertRaises(TypeError):
            sum_two('3',3)
    def test_third(self):
        sum_two(2,3)
    def test_fourth(self):
        with self.assertRaises(TypeError):
            sum_two(True,5)
if __name__ == '__main__':
    unittest.main()



