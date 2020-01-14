import copy
import os
import pickle


class AVLTree:
    """A basic AVL tree supporting insertions and deletions."""
    class _Node:
        """A single node in the AVL tree."""
        def __init__(self, value):
            """
            Create the node.

            :param value: The value of the node
            :type value: object
            """

            self.value = value
            self.left = None
            self.right = None
            self.height = 1

    def __init__(self):
        """Create the tree."""
        self.root = None

    def insert(self, value):
        """
        Insert a new value into the tree.

        :param value: A new value
        :type value: object
        :return: None
        """

        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        """
        Insert a new value into the subtree with the root `node`.

        :param node: A node
        :type node: AVLTree._Node
        :param value: A new value
        :type value: object
        :return: The root of the subtree after insertion
        :rtype: AVLTree._Node
        """

        if node is None:
            # create new leaf node
            return self._Node(value)
        elif value < node.value:
            # insert into left subtree
            node.left = self._insert(node.left, value)
        else:
            # insert into right subtree
            node.right = self._insert(node.right, value)

        # balance and return
        return self._balance(node)

    def delete(self, value):
        """
        Delete a value from the tree.

        :param value: The value to delete
        :type value: object
        :return: None
        """

        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        """
        Delete a value from the subtree with the root `node`.

        :param node: A node
        :type node: AVLTree._Node
        :param value: The value to delete
        :type value: object
        :return: The root of the subtree after deletion
        :rtype: AVLTree._Node
        """

        if node is None:
            return node
        elif value < node.value:
            # delete from left subtree
            node.left = self._delete(node.left, value)
        elif value > node.value:
            # delete from right subtree
            node.right = self._delete(node.right, value)
        else:
            # delete current node
            # if node has one child, return that child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # node has 2 children;
                # replace this node's value with the smallest value from
                # the right subtree, then delete that value from the
                # right subtree
                node.value = self._get_min_node(node.right).value
                node.right = self._delete(node.right, node.value)

        # balance and return
        return self._balance(node)

    def _balance(self, node):
        """
        Balance a subtree with the root `node`, such that the heights of
        the left and right subtrees differ by no more than one.

        :param node: A node
        :type node: AVLTree._Node
        :return: The balanced node
        :rtype: AVLTree._Node
        """

        self._update_height(node)
        balance = self._get_balance(node)
        if balance > 1:  # left heavy
            if self._get_balance(node.left) < 0:  # left right
                node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1:  # right heavy
            if self._get_balance(node.right) > 0:  # right left
                node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _left_rotate(self, node):
        """
        Perform a left rotation on `node`.

        :param node: Node to be rotated
        :type node: AVLTree._Node
        :return: The root node after rotation
        :rtype: AVLTree._Node
        """

        right_node = node.right
        right_left_node = right_node.left

        # rotate
        right_node.left = node
        node.right = right_left_node

        # update heights
        self._update_height(node)
        self._update_height(right_node)

        return right_node

    def _right_rotate(self, node):
        """
        Perform a right rotation on `node`.

        :param node: Node to be rotated
        :type node: AVLTree._Node
        :return: The root node after rotation
        :rtype: AVLTree._Node
        """

        left_node = node.left
        left_right_node = left_node.right

        # rotate
        left_node.right = node
        node.left = left_right_node

        # update heights
        self._update_height(node)
        self._update_height(left_node)

        return left_node

    @staticmethod
    def _get_height(node):
        """
        Get the height of the subtree with the root `node`.

        :param node: A node
        :type node: AVLTree._Node
        :return: The height of the subtree
        :rtype: int
        """

        if node is None:
            return 0
        return node.height

    def _update_height(self, node):
        """
        Update the height attribute of `node`.

        :param node: A node
        :type node: AVLTree._Node
        :return: None
        """

        node.height = 1 + max(
            self._get_height(node.left),
            self._get_height(node.right))

    def _get_balance(self, node):
        """
        Get the balance factor of `node`.
        The balance factor is equal to the height of the left subtree
        minus the height of the right subtree.

        :param node: A node
        :type node: AVLTree._Node
        :return: The balance factor
        :rtype: int
        """

        return self._get_height(node.left) - self._get_height(node.right)

    def _get_min_node(self, node):
        """
        Get the node with the smallest value from the subtree with the
        root `node`.

        :param node: A node
        :type node: AVLTree._Node
        :return: The node with the smallest value
        :rtype: AVLTree._Node
        """

        if node.left is None:
            return node
        return self._get_min_node(node.left)

    def to_list(self, preorder=False):
        """
        Get a list of all values in the tree.
        If `preorder` is True, the order of the list will represent a
        pre-order traversal of the tree.
        If `preorder` is False, the list will be sorted from least to
        greatest.

        :param preorder: True to get pre-order list, otherwise False,
                         defaults to False
        :type preorder: bool
        :return: List of values
        :rtype: list
        """

        return self._to_list(self.root, preorder=preorder)

    def _to_list(self, node, preorder=False):
        """
        Get a list of all values in the subtree with the root `node`.
        If `preorder` is True, the order of the list will represent a
        pre-order traversal of the tree.
        If `preorder` is False, the list will be sorted from least to
        greatest.

        :param node: A node
        :type node: AVLTree._Node
        :param preorder: True to get pre-order list, otherwise False,
                         defaults to False
        :type preorder: bool
        :return: List of values
        :rtype: list
        """

        if node is None:
            return []

        left = self._to_list(node.left, preorder=preorder)
        right = self._to_list(node.right, preorder=preorder)
        root = [node.value]

        if preorder:
            return root + left + right
        return left + root + right


class MyTree(AVLTree):
    """
    My modified version of an AVL tree.

    This tree is kept more strictly balanced than an AVL tree, so that
    the tree's height is always as small as possible.

    This balance is enforced by checking the difference between the
    minimum height and the maximum height of a given subtree. If the
    minimum and maximum height differ by more than 1, the subtree is
    rebalanced as follows:

    If the tree is left-heavy:
        1. Remove the largest value from the left subtree.
        2. Change the root node's value to this value.
        3. Insert the root node's old value into the right subtree.
    If the tree is right-heavy:
        1. Remove the smallest value from the right subtree.
        2. Change the root node's value to this value.
        3. Insert the root node's old value into the left subtree.
    """

    class _Node(AVLTree._Node):
        """
        A single node in the tree.
        This is the same as an AVLTree node except that it also has the
        attribute `min_height`.
        """

        def __init__(self, value):
            """
            Create the node.

            :param value: The value of the node
            :type value: object
            """

            super().__init__(value)
            self.min_height = 1

    def _balance(self, node):
        """
        Balance a subtree with the root `node` according to AVL
        balance rules, then balance such that the subtree's minimum
        height and maximum height differ by no more than one.

        :param node: A node
        :type node: MyTree._Node
        :return: The balanced node
        :rtype: MyTree._Node
        """

        # first, balance according to AVL rules
        node = super()._balance(node)

        if (self._get_height(node) - self._get_min_height(node)) > 1:
            # the tree is a valid AVL tree, but not perfectly balanced
            if (
                    self._get_min_height(node.left)
                    - self._get_min_height(node.right)
                    > 0):
                # left heavy
                node = self._right_shift(node)
            else:
                # right heavy
                node = self._left_shift(node)

        return node

    def _right_shift(self, root):
        """
        Balance the `root` node by:
            1. Removing the largest value from the left subtree
            2. Changing the `root` node's value to the value from step 1
            3. Inserting the root node's old value into the right
               subtree

        :param root: A node to be balanced
        :type root: MyTree._Node
        :return: The root node after balancing
        :rtype: MyTree._Node
        """

        def insert_min(node, value):
            """
            Insert a value into a subtree, assuming that it is the
            smallest value without comparing it to any other nodes.

            :param node: The root node of the subtree
            :type node: MyTree._Node
            :param value: The value to be inserted
            :type value: object
            :return: The root node after insertion
            :rtype: MyTree._Node
            """

            if node is None:
                # create new leaf node
                return self._Node(value)
            # insert into left subtree
            node.left = insert_min(node.left, value)
            # balance and return
            return self._balance(node)

        def delete_max(node):
            """
            Delete the largest value from the subtree with the root
            `node`.

            :param node: The root node of the subtree
            :type node: MyTree._Node
            :return: The root node after deletion
            :rtype: MyTree._Node
            """

            if node is None:
                return node
            if node.right is None:
                # this is the maximum node, replace with its left child
                return node.left
            node.right = delete_max(node.right)
            return self._balance(node)

        # copy next greatest value to root node
        root_value = root.value
        root.value = self._get_max_node(root.left).value

        # delete value from left tree
        root.left = delete_max(root.left)

        # insert old root value into right tree
        root.right = insert_min(root.right, root_value)

        self._update_height(root)
        return root

    def _left_shift(self, root):
        """
        Balance the `root` node by:
            1. Removing the smallest value from the right subtree
            2. Changing the `root` node's value to the value from step 1
            3. Inserting the root node's old value into the left subtree

        :param root: A node to be balanced
        :type root: MyTree._Node
        :return: The root node after balancing
        :rtype: MyTree._Node
        """

        def insert_max(node, value):
            """
            Insert a value into a subtree, assuming that it is the
            largest value without comparing it to any other nodes.

            :param node: The root node of the subtree
            :type node: MyTree._Node
            :param value: The value to be inserted
            :type value: object
            :return: The root node after insertion
            :rtype: MyTree._Node
            """

            if node is None:
                # create new leaf node
                return self._Node(value)
            # insert into right subtree
            node.right = insert_max(node.right, value)
            # balance and return
            return self._balance(node)

        def delete_min(node):
            """
            Delete the smallest value from the subtree with the root
            `node`.

            :param node: The root node of the subtree
            :type node: MyTree._Node
            :return: The root node after deletion
            :rtype: MyTree._Node
            """

            if node is None:
                return node
            if node.left is None:
                # this is the minimum node, replace with its right child
                return node.right
            node.left = delete_min(node.left)
            return self._balance(node)

        # copy next lowest value to root node
        root_value = root.value
        root.value = self._get_min_node(root.right).value

        # delete value from right tree
        root.right = delete_min(root.right)

        # insert old root value into left tree
        root.left = insert_max(root.left, root_value)

        self._update_height(root)
        return root

    @staticmethod
    def _get_min_height(node):
        """
        Get the minimum height of the subtree with the root `node`.

        :param node: A node
        :type node: MyTree._Node
        :return: The minimum height of the subtree
        :rtype: int
        """

        if node is None:
            return 0
        return node.min_height

    def _update_height(self, node):
        """
        Update the height and min_height attributes of `node`.

        :param node: A node
        :type node: MyTree._Node
        :return: None
        """

        super()._update_height(node)
        node.min_height = 1 + min(
            self._get_min_height(node.left),
            self._get_min_height(node.right))

    def _get_max_node(self, node):
        """
        Get the node with the largest value from the subtree with the
        root `node`.

        :param node: A node
        :type node: MyTree._Node
        :return: The node with the largest value
        :rtype: MyTree._Node
        """

        if node.right is None:
            return node
        return self._get_max_node(node.right)


class UndoTree(MyTree):
    """A MyTree that allows any comparison to be undone."""
    class UndoClicked(Exception):
        """Raise this exception to undo a comparison."""
        pass

    class _Undo(Exception):
        """
        Raised by the recursive method :meth:`_insert` after an
        :class:`UndoClicked` exception is caught, so that the previous
        iteration can handle it.
        """

        pass

    class _Redo(Exception):
        """
        Raised by the recursive method :meth:`_redo` if it catches an
        :class:`_Undo` exception, so that the previous iteration can
        handle it.
        """

        pass

    class _Cancel(Exception):
        """
        Raised when an undo operation has to go back past the current
        root of the tree, so that the :meth:`insert` method does not
        change the root again when the function finishes.
        """

        pass

    def __init__(self):
        """Create the tree."""
        super().__init__()

        # store the state of the tree before each insertion
        self.roots = []

        # list of lists: for each value inserted, keep a list of nodes
        # that the value was compared to
        self.nodes = []

        # list of each value that has been inserted
        self.values = []

        # when undo goes back to insertion of a previous value, add the
        # current value to this list to be resumed later
        self.resume = []

    def insert(self, value):
        """
        Insert a new value into the tree.

        :param value: A new value
        :type value: object
        :return: None
        """

        self.nodes.append([])  # new sub-list of comparisons
        self.values.append(value)

        try:
            super().insert(value)
        except self._Cancel:
            pass  # root has already been affected elsewhere

        # check if any values were moved to self.resume
        if self.resume:
            self.insert(self.resume.pop())

    def _insert(self, node, value):
        """
        Insert a new value into the subtree with the root `node`.

        :param node: A node
        :type node: MyTree._Node
        :param value: A new value
        :type value: object
        :return: The root of the subtree after insertion
        :rtype: MyTree._Node
        """

        if node is None:
            if self.root:
                # store a copy of the current root before insertion
                self.roots.append(copy.deepcopy(self.root))
        else:
            # keep track of the comparison to this node
            self.nodes[-1].append(node.value)

        try:
            return super()._insert(node, value)
        except self.UndoClicked:
            if node == self.root:  # need to undo past the current root
                # get rid of comparisons to the current value
                self.nodes.pop()

                if not self.roots:
                    # this is the first value, can't go back further
                    # just do insertion again
                    self.insert(self.values.pop())
                else:
                    # move current value to self.resume
                    self.resume.append(self.values.pop())
                    # go back to previous state of root
                    self.root = self.roots.pop()
                    # redo insertion of the previous value
                    self.root = self._redo(
                        self.root, self.values[-1], self.nodes[-1])

                # prevent insert method from assigning root again
                raise self._Cancel
            else:
                # just go back to parent node
                self.nodes[-1].pop()  # discard this comparison
                raise self._Undo  # caught by _insert on parent node
        except self._Undo:
            # discard this comparison since it will be added again
            self.nodes[-1].pop()
            return self._insert(node, value)  # do comparison again

    def _redo(self, node, value, path):
        """
        Redo the insertion of `value` into `node`.

        To avoid comparing any values on the way down the tree, the list
        `path` is used to specify the path from the root `node` down to
        the desired node. The first value of `path` should equal the
        value of the root `node`, and the last value will be the value
        compared to the parameter `value`.

        :param node: A node
        :type node: MyTree._Node
        :param value: The value to insert
        :type value: object
        :param path: List of values representing the path down the tree
        :type path: list
        :return: The root node after insertion
        :rtype: MyTree._Node
        """

        try:
            if len(path) <= 1:  # last node in path reached
                self.nodes[-1].pop()  # discard the last comparison
                return self._insert(node, value)  # insert node
            if node.left and node.left.value == path[1]:
                # next value in path is on the left
                # call redo on left child
                node.left = self._redo(node.left, value, path[1:])
            elif node.right and node.right.value == path[1]:
                # next value in path is on the right
                # call redo on right child
                node.right = self._redo(node.right, value, path[1:])

            # balance and return
            return self._balance(node)
        except self._Undo:
            # go back to previous/parent node
            raise self._Redo
        except self._Redo:
            # insert into this node
            return self._redo(node, value, path[:1])


class SaveStateTree(UndoTree):
    """
    An UndoTree that can save its current state to a file, to be resumed
    at a later time.
    """

    class Exit(Exception):
        """
        Raise this exception to save the tree to file before quitting.
        """

        pass

    def __init__(self, filename):
        """
        Create the tree. When necessary, the tree will be saved to
        `filename`. If the file exists at the time of initialization,
        the tree will be loaded from the file.

        :param filename: Name of the file to save to
        :type filename: str
        """

        super().__init__()
        self.filename = filename
        try:
            with open(self.filename, 'rb') as f:
                # get tree from file
                tree = pickle.load(f)
                # copy tree to self
                self.__dict__ = tree.__dict__
                # resume where previously left off
                self.root = self._redo(
                    self.root, self.values[-1], self.nodes[-1])
        except self.Exit:
            self.exit()
        except self._Cancel:
            pass  # root has already been affected elsewhere
        except FileNotFoundError:
            pass  # file does not exist, create new tree

        # check if any values were moved to self.resume
        if self.resume:
            self.insert(self.resume.pop())

    def insert(self, value):
        """
        Insert a new value into the tree.

        :param value: A new value
        :type value: object
        :return: None
        """

        try:
            super().insert(value)
        except self.Exit:
            self.exit()

    def delete_file(self):
        """
        Delete the file used to store the tree.

        :return: None
        """

        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass

    def exit(self):
        """
        Save the tree to file and raise the Exit exception.

        :return: None
        """

        with open(self.filename, 'wb') as f:
            pickle.dump(self, f)
        raise self.Exit
