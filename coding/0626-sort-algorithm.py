import pdb

def insert_sort(in_list):
    if len(in_list) == 1:
        return in_list
    for i in range(1, len(in_list)):
        for j in range(i-1, -1, -1):
            if in_list[j] > in_list[j+1]:
                in_list[j], in_list[j+1] = in_list[j+1], in_list[j]
    return in_list


def qs(input_list):
    return quick_sort(input_list, 0, len(input_list)-1)

def quick_sort(lst, left, right):
    if left >= right:
        return lst
    else:
        key = left
        lp = left
        rp = right
        while lp < rp:
            while lst[rp] >= lst[key] and lp < rp:
                rp = rp - 1
            while lst[lp] <= lst[key] and lp < rp:
                lp = lp + 1
            print(lst, lp, rp, key)
            lst[lp], lst[rp] = lst[rp], lst[lp]
        lst[left], lst[lp] = lst[lp], lst[left]
        lst = quick_sort(lst, left, lp)
        lst = quick_sort(lst, rp+1, right)
        return lst

def qs_dict(input_dict, rv=False):
    return dict_quick_sort(input_dict.items(), 0, len(input_dict)-1, rv=rv)

def dict_quick_sort(lst_dict, left, right, rv=False):
    """ if rv = False, output items ordered with key;
    if rv = True, return items ordered with values;
    """
    if left >= right:
        return lst_dict
    elif rv == True:
        lst = [j for i,j in lst_dict]
    else:
        lst = [i for i,j in lst_dict]
    key = left
    lp = left
    rp = right
    while lp < rp:
        while lst[rp] >= lst[key] and lp < rp:
            rp = rp - 1
        while lst[lp] <= lst[key] and lp < rp:
            lp = lp + 1
        print(lst_dict, lp, rp, key)
        lst_dict[lp], lst_dict[rp] = lst_dict[rp], lst_dict[lp]
    lst_dict[left], lst_dict[lp] = lst_dict[lp], lst_dict[left]
    lst_dict = dict_quick_sort(lst_dict, left, lp, rv=rv)
    lst_dict = dict_quick_sort(lst_dict, rp+1, right, rv=rv)
    return lst_dict


if __name__ == '__main__':
    test_list = [1,4,3,2,5,7,5,6]
    td = {'a':1, 'b':6, 'd':10, 'c':2}
    print(qs_dict(td, rv=True))
