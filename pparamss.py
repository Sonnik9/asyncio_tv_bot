class Parameters:
    def __init__(self):
        self.max_threads = 12
        self.kline_time, self.time_frame = 4, 'h'
        self.interval = str(self.kline_time) + self.time_frame
        self.market = 'futures'
        # self.market = 'spot'
        # self.test_flag = False
        self.test_flag = True
        self.depo = 100
        self.main_strategy_number = 1
        self.sl_strategy_number = 2
        self.limit_selection_coins = 210

        # self.time_frame_list = [(2000, '15m'), (1000, '30m'), (500, '1h'), (100, '4h')] 
        # self.long_sell_strategy = ['long_short', 'long', 'short']

my_params = Parameters()
