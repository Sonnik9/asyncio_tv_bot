import time

# def tp_sl_strategy_1_func(order_obj, open_order):

def tp_sl_strategy_1_func(enter_price, current_price, qnt, defender):
   
    depo = 200 # 20*10
    close_order = False
    profit = None #USDT
    sl_q = 0.00001
    tp_q = 0.000015
    qnt = depo/ enter_price
        
    if current_price:
        # print(enter_price, current_price)
        # if side == 'BUY':
        if defender == 1:
            if current_price >= enter_price + (enter_price*tp_q):   
            # if current_price != enter_price:             
                # close_order = order_obj.close_order(symbol, order_id)     
                profit = (current_price - enter_price)*qnt
                close_order = True   
     
            elif current_price <= enter_price - (enter_price*sl_q):
            #     # close_order = order_obj.close_order(symbol, order_id)
                profit = (current_price - enter_price)*qnt
      
        # elif side == 'SELL':
        elif defender == -1:
            if current_price != enter_price:
            # if current_price <= enter_price - (enter_price*tp_q):   
                # close_order = order_obj.close_order(symbol, order_id) 
                profit = (enter_price - current_price)*qnt
                close_order = True 
      
            elif current_price >= enter_price + (enter_price*sl_q):
                # close_order = order_obj.close_order(symbol, order_id)
                profit = (enter_price - current_price)*qnt     

    return profit, close_order