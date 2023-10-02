
def asum_counter(total_raport_list):
    # print(total_raport_list)
    profitt = [x['profit'] for x in total_raport_list]
    win_rate = sum([1 for x in profitt if x >0])
    lose_rate = sum([1 for x in profitt if x <0])
    total = sum(profitt)
    win_per = (win_rate * 100)/(win_rate + lose_rate)
    result = f"Total: {total}$ \nWin_per: {win_per}%"
    with open('result.txt', 'w') as txt_file:
        txt_file.write(result) 