import numpy as np
def Write_remove_name(X,location_num):
    piece_to_value = {
        1: "p",
        2: "r",
        3: "N",
        4: "b",
        5: "q",
        6: "k",
        7: "P",
        8: "R",
        9: "N",
        10: "B",
        11: "Q",
        12: "K",
    }
    for key2, value2 in piece_to_value.items():
        X[value2] = X[key2]
        del X[key2]
    list1=[]
    count = 0
    # for ran in range(63):
    #     list_of_keys = [key
    #                     for key, list_of_values in X.items()
    #                     if ran in list_of_values]
    #     if list_of_keys:
    #         print()
    #         list1.append(count)
    #         list1.append(str(list_of_keys[0]))
    #         count=0
    #     else:
    #         if count/7==1:
    #             list1.append(count+1)
    #             count=0
    #         else:count=count+1
    # print(list1)
    list1=list(filter(lambda a: a != 0, list1))
    #print(list1[0:7]+"/"list1[8:15]+"/"list1[16:23]+"/"list1[24:31]+"/"list1[32:39]+"/"+list1[40:47]+"/"+list1[41:39]+" b KQkq - 0 4")


    for ran in range(64):
        list_of_keys = [key
                        for key, list_of_values in X.items()
                        if ran in list_of_values]
        if list_of_keys:
            list1.append(str(list_of_keys[0]))
            count=0
        else:
            list1.append(0)

    list1 = np.array(list1)
    shape = (8,8)
    list1=list1.reshape(shape)

    print(list1)
    return list1[location_num//8,location_num%8]
