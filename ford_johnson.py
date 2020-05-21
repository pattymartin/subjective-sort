def jacobsthal_generator():
    """
    Generate numbers following the sequence of Jacobsthal numbers:
    0, 1, 1, 3, 5, 11, 21, 43, 85, 171...

    :return: A generator object
    """

    i = 0
    yield i
    j = 1
    yield j

    while True:
        k = j + (2 * i)
        yield k
        i = j
        j = k


def _insertion_order():
    """
    Generate indices following the insertion order for the final step of
    the merge-insertion algorithm.

    This order is generated based on the Jacobsthal numbers: start
    by getting the next Jacobsthal number, then count backwards until
    you reach the previous Jacobsthal number. Subtract 1 from each
    number to account for zero-based indexing.

    The resulting sequence:
    0, 2, 1, 4, 3, 10, 9, 8, 7, 6, 5, 20...

    :return: A generator object
    """

    prev_index = -1
    jacobsthal = jacobsthal_generator()

    while True:
        next_index = next(jacobsthal) - 1  # subtract 1 for zero-based index
        for i in range(next_index, prev_index, -1):
            yield i
        prev_index = next_index


def binary_search(list_, item, start, end, key=None):
    """
    Find the index where `item` should be inserted in `list_`, between
    the indices `start` and `end`.
    If specified, `key` is a function used to extract a comparison key
    from each item.

    :param list_: A list
    :param item: The item to insert
    :param start: The starting index
    :param end: The ending index
    :param key: A function used to extract a comparison key
    :return: The index, as an integer
    """

    if not list_ or end <= start:
        return start

    if end - start <= 1:
        this_item, that_item = item, list_[start]
        if key:
            this_item, that_item = key(this_item), key(that_item)

        if this_item < that_item:
            return start
        else:
            return start + 1

    mid = (start + end) // 2
    this_item, that_item = item, list_[mid]
    if key:
        this_item, that_item = key(this_item), key(that_item)

    if that_item == this_item:
        return mid - 1
    elif that_item < this_item:
        return binary_search(list_, item, mid + 1, end, key=key)
    else:
        return binary_search(list_, item, start, mid, key=key)


def _pairs(list_, key=None):
    """
    Split a list into pairs, each pair ordered in ascending order.
    Returns a tuple of the form (pairs, odd_one_out). If the length of
    the list is odd, odd_one_out will be the unpaired final item.
    Otherwise, odd_one_out will be None.

    If specified, `key` is a function used to extract a comparison key
    from each item.

    :param list_: The list to split into pairs
    :param key: A function used to extract a comparison key
    :return: A tuple of the form (pairs, odd_one_out)
    """

    pairs = []
    odd_one_out = None

    for i in range(0, len(list_), 2):
        try:
            item1, item2 = key1, key2 = list_[i:i+2]
            if key:
                key1, key2 = key(item1), key(item2)

            # append original items, not the keys
            if key1 > key2:
                pairs.append((item2, item1))
            else:
                pairs.append((item1, item2))
        except ValueError:
            odd_one_out = list_[i]

    return pairs, odd_one_out


def _binary_insertion(sorted_pairs, odd_one_out=None, key=None):
    """
    Perform the binary insertion step of the merge-insertion sorting
    algorithm:

    - Take `sorted_pairs` to be a list of pairs which is sorted by the
      highest value in each pair. Create a list from these
      already-sorted high values.
    - Insert the lower, unsorted values from each pair into this sorted
      list, following the insertion order specified by the function
      `_insertion_order`.

    If there are an odd number of items and one cannot be paired,
    pass the final, unpaired item as `odd_one_out`.

    If specified, `key` is a function used to extract a comparison key
    from each item.

    :param sorted_pairs: A list of pairs, sorted by their highest values
    :param odd_one_out: An unpaired item
    :param key: A function used to extract a comparison key
    :return: The final sorted list
    """

    sorted_list = []
    low_values = []

    # the pairs are already sorted by their highest values.
    # Make sorted_list out of the high values
    # then later insert the low values into sorted_list
    for pair in sorted_pairs:
        lesser, greater = pair
        sorted_list.append(greater)
        low_values.append(lesser)

    # the odd one out is unsorted, add to the end of the low_values list
    if odd_one_out is not None:
        low_values.append(odd_one_out)

    num_inserted = 0
    insertion_order = _insertion_order()

    # insert following insertion order
    for next_index in insertion_order:
        if num_inserted >= len(low_values):
            break
        if next_index < len(low_values):
            # we know the item is less than its paired item
            # so only insert before that item
            insert_item = low_values[next_index]
            # the index of the paired item is offset by the number of
            # items that have already been inserted
            before_index = next_index + num_inserted

            # perform binary search and insert
            insert_index = binary_search(
                list_=sorted_list[:before_index], item=insert_item,
                start=0, end=before_index,
                key=key)
            sorted_list = (
                    sorted_list[:insert_index]
                    + [insert_item]
                    + sorted_list[insert_index:])

            num_inserted += 1

    return sorted_list


def merge_insertion_sort(list_, key=None):
    """
    Sort a list using merge-insertion sort, also known as the
    Ford-Johnson Algorithm.
    If specified, `key` is a function used to extract a comparison key
    from each item.

    :param list_: The list to be sorted
    :param key: A function used to extract a comparison key
    :return: The sorted list
    """

    if len(list_) <= 1:
        return list_

    # Step 1: split into ordered pairs
    # If there is an odd number of elements, leave one element unpaired
    pairs, odd_one_out = _pairs(list_, key=key)

    # Step 2: Recursively sort the pairs by their highest value
    def get_last(items):
        item = items
        if isinstance(item, tuple):
            try:
                item = get_last(items[-1])
            except TypeError:
                pass

        return key(item) if key else item

    sorted_pairs = merge_insertion_sort(pairs, key=get_last)

    # Step 3: Create a list with the higher values from step 2,
    # and insert the smaller values into this list
    return _binary_insertion(sorted_pairs, odd_one_out, key=key)
