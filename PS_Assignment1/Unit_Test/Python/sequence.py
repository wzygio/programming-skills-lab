import sys

class Sequence: # 虽然此处没有形参，但是可以输入一个变量作为self
    """
    DNA sequence consisting of A, C, G, T sequences.
    """

    WEIGHTS = {'A': 131.2, 'C': 289.2, 'G': 329.2, 'T': 304.2}
    """dict of str or unicode to float: nucleotide molecular weights"""

    def __init__(self, sequence=""):
        """Initialise Sequence with a string. The string must only
        contain letters in the set a,A,c,C,g,G,t,T.
        
        :param sequence: sequence
        :type sequence: str or unicode
        :raises AssertionError: if sequence contains an invalid letter
        调用：is_valid方法
        功能：如果是有效的序列，就将所有字母变为大写
        """
        assert Sequence.is_valid(sequence), \
            "Sequence should only contain A, C, G and T"
        self._nucleotides = sequence.upper() # 处理对象.方法

    @staticmethod
    def is_valid(nucleotides):
        """Is a given string a valid sequence of nucleotides? Does it
        only contain letters in the set a,A,c,C,g,G,t,T?
        
        :param nucleotides: nucleotides
        :type nucleotides: str or unicode
        :return: True if so, else False
        :rtype: bool
        调用：WEIGHT变量
        """
        upper = nucleotides.upper() # 将所有的nucleotides变为大写字母
        is_valid = True
        # 逐个检查序列中的每个nucleotide是否被包含在WEIGHT中，
        # 因为用了and，所有只要有一个false，最终结果就会为false
        for c in upper:
            is_valid = is_valid and c in Sequence.WEIGHTS # 变量：类.变量名称
        return is_valid

    @property
    def nucleotides(self):
        """Get nucleotides of this sequence, in upper-case.
    
        :return: nucleotides
        :rtype: str or unicode
        """
        return self._nucleotides # 将字符串变作一个列表

    def get_weight(self):
        """Calculate molecular weight of this DNA sequence.
    
        :return: molecular weight
        :rtype: float
        调用：calculate_weight方法
        """
        return Sequence.calculate_weight(self)

    @staticmethod
    def calculate_weight(sequence):
        """Calculate molecular weight of a DNA sequence.
        
        :param sequence:
        :type sequence: Sequence
        :return: molecular weight
        :rtype: float
        调用：nucleotides方法，WEIGHT dict
        """
        weight = 0
        for c in sequence.nucleotides: # 处理对象.方法；代表一个序列中元素的变量用一个字母代表即可
            weight += Sequence.WEIGHTS[c] # 叠加nucleotide在WEIGHT dict中对应的重量
        return weight

if __name__ == "__main__":
    sequence = Sequence(sys.argv[1])
    print(sequence.get_weight())

