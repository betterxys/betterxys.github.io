def insert_sort(in_list):
    if len(in_list) == 1:
        return in_list
    for i in range(1, len(in_list)):
        for j in range(i-1, -1, -1):
            if in_list[j] > in_list[j+1]:
                in_list[j], in_list[j+1] = in_list[j+1], in_list[j]
    return in_list


def quick_sort(in_list):
    pass



if __name__ == '__main__':
    test_list = [6,3,3,2,7]
    print(insert_sort(test_list))
