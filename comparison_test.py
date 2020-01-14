import random
import time

from trees import AVLTree, MyTree


class AVLTest(AVLTree):
    def __init__(self):
        self.comparisons = 0
        super().__init__()

    def _insert(self, node, value):
        if node is not None:
            self.comparisons += 1
        return super()._insert(node, value)


class MyTreeTest(AVLTest, MyTree):
    pass


def test(n_items):
    list_ = random.sample(range(n_items), n_items)
    print("Sorting {} items.".format(n_items))

    avl_tree = AVLTest()
    start_time1 = time.time()
    for item in list_:
        avl_tree.insert(item)
    end_time1 = time.time()

    my_tree = MyTreeTest()
    start_time2 = time.time()
    for item in list_:
        my_tree.insert(item)
    end_time2 = time.time()

    print(("{:>6}{:>15}    {}\n" * 3).format(
        "", "Comparisons", "Seconds",
        "AVL", avl_tree.comparisons, end_time1 - start_time1,
        "MyTree", my_tree.comparisons, end_time2 - start_time2
    ))


if __name__ == '__main__':
    for i in range(5):
        test(10)
        test(25)
        test(50)
        test(100)
        test(1000)
        test(10000)
