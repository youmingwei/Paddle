import unittest
import numpy as np
from paddle.v2.framework.op import Operator
from gradient_checker import GradientChecker, create_op
from op_test_util import OpTestMeta


class TestPadOp(unittest.TestCase):
    __metaclass__ = OpTestMeta

    def setUp(self):
        self.initTestCase()
        self.type = "pad"
        self.inputs = {'X': np.random.random(self.shape).astype("float32"), }
        self.attrs = {}
        self.attrs['paddings'] = np.array(self.paddings).flatten()
        self.attrs['pad_value'] = self.pad_value
        self.outputs = {
            'Out': np.pad(self.inputs['X'],
                          self.paddings,
                          mode='constant',
                          constant_values=self.pad_value)
        }

    def initTestCase(self):
        self.shape = (16, 16)
        self.paddings = [(0, 1), (2, 3)]
        self.pad_value = 0


class TestCase1(TestPadOp):
    def initTestCase(self):
        self.shape = (2, 3, 4, 4)
        self.paddings = [(0, 1), (2, 3), (2, 1), (1, 1)]
        self.pad_value = 0.5


class TestCase2(TestPadOp):
    def initTestCase(self):
        self.shape = (2, 2, 2)
        self.paddings = [(0, 0), (0, 0), (1, 2)]
        self.pad_value = 1


class TestCase3(TestPadOp):
    def initTestCase(self):
        self.shape = (8)
        self.paddings = [(0, 1)]
        self.pad_value = 0.9


class TestPadGradOp(GradientChecker):
    def setUp(self):
        self.initTestCase()
        self.op = Operator(
            type="pad",
            X="X",
            Out="Out",
            paddings=np.array(self.paddings).flatten(),
            pad_value=self.pad_value)
        self.inputs = {'X': np.random.random(self.shape).astype("float32"), }

    def initTestCase(self):
        self.shape = (16, 16)
        self.paddings = [(0, 1), (2, 3)]
        self.pad_value = 0

    def test_normal(self):
        self.check_grad(self.op, self.inputs, set(["X"]), "Out")

    def test_cpu_gpu_compare(self):
        self.compare_grad(self.op, self.inputs)


class TestiGradCase1(TestPadOp):
    def initTestCase(self):
        self.shape = (2, 3, 4, 4)
        self.paddings = [(0, 1), (2, 3), (2, 1), (1, 1)]
        self.pad_value = 0.5


class TestGradCase2(TestPadOp):
    def initTestCase(self):
        self.shape = (2, 2, 2)
        self.paddings = [(0, 0), (0, 0), (1, 2)]
        self.pad_value = 1


class TestGradCase3(TestPadOp):
    def initTestCase(self):
        self.shape = (8)
        self.paddings = [(0, 1)]
        self.pad_value = 0.9


if __name__ == '__main__':
    unittest.main()
