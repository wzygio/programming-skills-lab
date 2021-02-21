import unittest

from sequence import Sequence #从sequence模块中导入sequence类


class SequenceTestCase(unittest.TestCase):

    def test_get_nucleotides(self):
        sequence_str = "GATTACCA"
        sequence = Sequence(sequence_str) 
        # 创建了一个sequence对象；
        # 当字符串被填入对象后，会自动运行__init__方法初始化
        self.assertEqual(sequence_str, sequence.nucleotides,
                         msg="Nucleotides returned were not those given")

    def test_get_weight(self):
        sequence = Sequence("G")
        self.assertAlmostEqual(Sequence.WEIGHTS['G'],
                               sequence.get_weight(),
                               delta=0.01,
                               msg="Weight returned was unexpected")

    def test_calculate_weight(self):
        sequence = Sequence("G")
        self.assertAlmostEqual(Sequence.WEIGHTS['G'],
                               Sequence.calculate_weight(sequence),
                               delta=0.01,
                               msg="Weight returned was unexpected")
		# self.assertAlmostEqual(比较对象1，比较对象2，threshold，如果出现错误返回的信息)
		
