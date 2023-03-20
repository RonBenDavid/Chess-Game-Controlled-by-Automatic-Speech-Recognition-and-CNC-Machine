import numpy as np
def Write_location(X):
    piece_to_value = {
        1: "P",
        2: "R",
        3: "N",
        4: "B",
        5: "Q",
        6: "K",
        7: "p",
        8: "r",
        9: "n",
        10: "b",
        11: "q",
        12: "k",
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
    list1.reverse()
    list1 = np.array(list1)
    shape = (8,8)
    list1=list1.reshape(shape)
    rows=[]
    for x in range(8):
        rows.append(''.join(str(item) for item in list1[x,]))
    rows2=rows[0]
    str1=[]
    count=0
    new_list=[]
    for y in range(8):
        rows2 = rows[y]
        str1 = []
        count = 0
        for x in range(8):
            if rows2[x]=='0':
                count=count+1
                if((count>1) and (x>=1)):
                    str1.pop()
                str1.append(count)

            else:
                    str1.append(rows2[x])
                    count=0

        new_list.append(str1)
    new_list2=[]
    for x in range(8):
        new_list[x].reverse()
        new_list2.append(''.join(str(item) for item in new_list[x]))
    new_string=new_list2[0]+"/"+new_list2[1]+"/"+new_list2[2]+"/"+new_list2[3]+"/"+new_list2[4]+"/"+new_list2[5]+"/"+new_list2[6]+"/"+new_list2[7]+" b KQkq - 0 4"
    return new_string