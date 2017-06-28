def insert_sort(in_list):
    if len(in_list) == 1:
        return in_list
    for i in range(1, len(in_list)):
        for j in range(i-1, -1, -1):
            if in_list[j] > in_list[j+1]:
                in_list[j], in_list[j+1] = in_list[j+1], in_list[j]
    return in_list

a = insert_sort([6,3,2,7])
print(a)
