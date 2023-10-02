from pparamss import my_params

class SL_STRATEGYY():
    def __init__(self, sl_strategy_number, depo) -> None:
        self.sl_strategy_number = sl_strategy_number 
        self.depo = depo # 200 # 20*10     
        self.t_p = None
        self.s_l = None
        self.tralling_s_l = None
        self.counter = 1
        self.tralling_flag = False
        self.checkpoint = None

    def sl_controller(self, main_stake):
        # profit = None
        profit_flag = False
        qnt = None
        for item1 in main_stake:
            if not item1['in_position']:
                # open_order func
                item1['in_position'] = True
        
        for item in main_stake:
            profit = None
            # profit, symbol, defender, enter_price, current_price, in_position, close_order
            # if item['enter_price']:
            # try:
            #     qnt = round((self.depo/item['enter_price']), 7)
            # except Exception as ex:
            #     print(f"MONEY/stop_logic_1.py_str88:___{ex}")
            #     continue
                        
            try:
                defender = item['defender']                
                qnt = item['qnt']
                enter_price = item['enter_price']
                current_price = item['current_price']
                atr = item['atr']
            except Exception as ex:
                print(f"MONEY/stop_logic_1.py_str94:___{ex}")

            if self.sl_strategy_number == 1:
                profit_flag, profit = self.sl_strategy_one(defender, enter_price, current_price, qnt)
                if profit_flag:
                    item['close_order'] = True  
                item['profit'] = profit

            elif self.sl_strategy_number == 2:
                profit_flag, profit = self.sl_strategy_two(defender, enter_price, current_price, atr, qnt)
                if profit_flag:
                    item['close_order'] = True  
                item['profit'] = profit

            elif self.sl_strategy_number == 3:
                profit_flag, profit = self.sl_strategy_three(defender, enter_price, current_price, atr, qnt) 
                if profit_flag:
                    item['close_order'] = True   
                item['profit'] = profit

            return main_stake, profit_flag

    def sl_strategy_one(self, defender, enter_price, current_price, qnt): 
        profit = None
        self.t_p = 0.0015
        self.s_l = 0.001
        # self.t_p = 0.015
        # self.s_l = 0.007

        if defender == 1:             
            if current_price >= enter_price + enter_price*self.t_p:
                profit = (current_price - enter_price)*qnt
                return True, profit
            if current_price <= enter_price - enter_price*self.s_l:
                profit = (current_price - enter_price)*qnt
                return True, profit
        if defender == -1:                
            if current_price <= enter_price - enter_price*self.t_p:
                profit = (enter_price - current_price)*qnt
                return True, profit
            if current_price >= enter_price + enter_price*self.s_l:
                profit = (enter_price - current_price)*qnt
                return True, profit

        return False, profit
        
    def sl_strategy_two(self, defender, enter_price, current_price, atr, qnt):
            profit = None
            self.s_l = 0.01

            if defender == 1: 
                self.checkpoint = enter_price*(1 + self.counter/100)
                self.tralling_s_l = enter_price + ((self.checkpoint - enter_price)/2)
                if current_price > enter_price:
                    if current_price >= self.checkpoint:
                        self.tralling_flag = True
                        self.counter += 1
                        if self.counter == 2:
                            self.counter = 0
                            # print('realy i am here')
                            self.tralling_flag = False
                            profit = (current_price - enter_price)*qnt
                            return True, profit                   
                    if (current_price <= self.tralling_s_l) and self.tralling_flag:
                        self.counter = 0
                        # print('hi2')
                        self.tralling_flag = False
                        profit = (current_price - enter_price)*qnt
                        return True, profit  
                elif current_price < enter_price:
                    if current_price <= enter_price - atr*self.s_l:
                        # print('hi3')
                        self.counter = 0
                        self.tralling_flag = False
                        profit = (current_price - enter_price)*qnt
                        return True, profit
                    
            if defender == -1: 
                self.checkpoint = enter_price*(1 - self.counter/100)
                self.tralling_s_l = enter_price - ((enter_price - self.checkpoint)/2)
                if current_price < enter_price:
                    if current_price <= self.checkpoint:
                        self.tralling_flag = True
                        self.counter += 1
                        if self.counter == 2:
                            self.counter = 0
                            # print('realy i am here')
                            self.tralling_flag = False
                            profit = (enter_price - current_price)*qnt
                            return True, profit                 
                    if (current_price >= self.tralling_s_l) and self.tralling_flag:
                        self.counter = 0
                        self.tralling_flag = False
                        profit = (enter_price - current_price)*qnt
                        return True, profit  

                elif current_price > enter_price:                        
                    if current_price >= enter_price + atr*self.s_l:
                        # print('hi3')
                        self.counter = 0
                        self.tralling_flag = False
                        profit = (enter_price - current_price)*qnt
                        return True, profit
                    
            return False, profit
    
    def sl_strategy_three(self, defender, enter_price, current_price, atr, qnt):
        profit = None
        self.t_p = 0.015
        self.s_l = 0.007
        self.t_p = 0.0015
        self.s_l = 0.001
        
        if defender == 1:                
            if current_price >= enter_price + atr*self.t_p:
                profit = (current_price - enter_price)*qnt
                return True, profit
            if current_price <= enter_price - atr*self.s_l:
                profit = (current_price - enter_price)*qnt
                return True, profit
            
        if defender == -1:                
            if current_price <= enter_price - atr*self.t_p:
                profit = (enter_price - current_price)*qnt
                return True, profit
            if current_price >= enter_price + atr*self.s_l:
                profit = (enter_price - current_price)*qnt
                return True, profit

        return False, profit

sl_strategies = SL_STRATEGYY(my_params.sl_strategy_number, my_params.depo)
