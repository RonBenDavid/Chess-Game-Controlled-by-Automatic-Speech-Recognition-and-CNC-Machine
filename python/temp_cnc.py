

while True:
    f_remove_hash_1 = hashfile("remove.txt")
    while True:
        f_remove_hash_2 = hashfile("remove.txt")
        # Doing primitive string comparison to
        # check whether the two hashes match or not
        if (f_remove_hash_1 == f_remove_hash_2):
            break
        else:
            print("Files are different!")
            print(f"Hash of File 1_remove: {f1_hash}")
            print(f"Hash of File 2_remove: {f2_hash}")
            f_remove_hash_1 = f_remove_hash_2
            file_remove = open("remove.txt", "r+")
            file1 = open("x.txt", "r+")
            file2 = open("y.txt", "r+")
            if(os.stat("remove.txt").st_size != 0):
                name_of_piece = file1.read()
                x = int(file1.read())
                y = int(file2.read())
                if name_of_piece=='p':
                    cnc_remove(y, p_arry[p_count])
                    p_count+=1
                    
                if name_of_piece=='P':
                    cnc_remove(y, P_arry[P_count])
                    P_count+=1
                    print("remove piceeee!!!")
                    cnc1(x,y)
                    
                if name_of_piece=='r':
                    cnc_remove(y, r_arry[r_count])
                    r_count+=1
                    
                if name_of_piece=='R':
                    cnc_remove(y, R_arry[R_count])
                    R_count+=1
                    
                if name_of_piece=='n':
                    cnc_remove(y, n_arry[n_count])
                    n_count+=1
                    
                if name_of_piece=='N':
                    cnc_remove(y, N_arry[N_count])
                    N_count+=1
                    
                if name_of_piece=='b':
                    cnc_remove(y, b_arry[b_count])
                    b_count+=1
                    
                if name_of_piece=='B':
                    cnc_remove(y, B_arry[B_count])
                    B_count+=1
                    
                if name_of_piece=='q':
                    cnc_remove(y, q_arry)
                    
                if name_of_piece=='Q':
                    cnc_remove(y, Q_arry)
                    
                if name_of_piece=='k':
                    cnc_remove(y, k_arry)
                    
                if name_of_piece=='K':
                    cnc_remove(y, K_arry)
                print("bbdbdd")
        file1.close()
        file2.close()
        file_remove.close()






