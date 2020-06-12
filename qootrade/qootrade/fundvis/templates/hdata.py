with open('world.csv', 'r') as f:
    print('var data0 = [')
    lines = f.readlines()
    cnt = 1
    d = 0
    print('{day:' + '0' + ',val:' + str(lines[0].split(',')[2])+'},')
    for idx in range(1, len(lines)):
        if lines[idx].split(',')[1] != lines[idx-1].split(',')[1]:
            print(']')
            print('\n')
            print('var data' + str(cnt) + '= [')
            cnt = cnt + 1
            d = 0
        print('{day:' + str(d) + ', val:' + str(lines[idx].split(',')[2]) + '},')
        d = d + 1
        
