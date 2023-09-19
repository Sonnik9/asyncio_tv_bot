
def sl_tp_logic(main_stake):
    depo = 200 # 20*10    
    sl_q = 0.00001
    tp_q = 0.000015
    profit_flag = False

    for item1 in main_stake:
        if not item1['in_position']:
            # open_order func
            item1['in_position'] = True
    
    for item in main_stake:
        profit = None
        # profit, symbol, defender, enter_price, current_price, in_position, close_order
        if item['enter_price']:
            try:
                qnt = round((depo/item['enter_price']), 7)
            except Exception as ex:
                print(f"MONEY/stop_logic_1.py_str22:___{ex}")

        try:
            if item['defender'] == 1:

                if item['current_price'] >= item['enter_price'] + (item['enter_price']*tp_q):   
                    profit = (item['current_price'] - item['enter_price'])*qnt
                    # close_order func
                    item['close_order'] = True   
                    item['profit'] = profit
                    profit_flag = True

        
                elif item['current_price'] <= item['enter_price'] - (item['enter_price']*sl_q):            
                    profit = (item['current_price'] - item['enter_price'])*qnt
                    # close_order func
                    item['close_order'] = True   
                    item['profit'] = profit   
                    profit_flag = True   
        
            elif item['defender'] == -1:            
                if item['current_price'] <= item['enter_price'] - (item['enter_price']*tp_q):               
                    profit = (item['enter_price'] - item['current_price'])*qnt
                    # close_order func
                    item['close_order'] = True  
                    item['profit'] = profit 
                    profit_flag = True
        
                elif item['current_price'] >= item['enter_price'] + (item['enter_price']*sl_q):                
                    profit = (item['enter_price'] - item['current_price'])*qnt  
                    # close_order func
                    item['close_order'] = True  
                    item['profit'] = profit
                    profit_flag = True
        except Exception as ex:
            print(f"MONEY/stop_logic_1.py_str55:___{ex}")

    return main_stake, profit_flag

