
def sl_tp_logic(main_stake):
    depo = 200 # 20*10    
    sl_q = 0.00001
    tp_q = 0.000015

    {'profit': None, 'symbol': 'FLMUSDT', 'defender': 1, 'enter_price': None, 'current_price': None, 'in_position': False, 'close_order': False}
    for key in main_stake:
        if not key['in_position']:
            # open_order func
            key['in_position'] = True
    
    for key in main_stake:
        profit = None
        # profit, symbol, defender, enter_price, current_price, in_position, close_order
        if key['enter_price']:
            qnt = round((depo/key['enter_price']), 7)
        else:
            continue
        if key['defender'] == 1:
            if key['current_price'] >= key['enter_price'] + (key['enter_price']*tp_q):   
                profit = (key['current_price'] - key['enter_price'])*qnt
                # close_order func
                key['close_order'] = True   
                key['profit'] = profit
     
            elif key['current_price'] <= key['enter_price'] - (key['enter_price']*sl_q):            
                profit = (key['current_price'] - key['enter_price'])*qnt
                # close_order func
                key['close_order'] = True   
                key['profit'] = profit      
       
        elif key['defender'] == -1:            
            if key['current_price'] <= key['enter_price'] - (key['enter_price']*tp_q):               
                profit = (key['enter_price'] - key['current_price'])*qnt
                # close_order func
                key['close_order'] = True  
                key['profit'] = profit 
      
            elif key['current_price'] >= key['enter_price'] + (key['enter_price']*sl_q):                
                profit = (key['enter_price'] - key['current_price'])*qnt  
                # close_order func
                key['close_order'] = True  
                key['profit'] = profit

    return main_stake