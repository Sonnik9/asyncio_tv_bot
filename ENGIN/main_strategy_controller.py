from pparamss import my_params
from ENGIN.ind_strategy_1 import get_orders_stek_1
from ENGIN.ind_strategy_2 import get_orders_stek_2

def main_strategy_control_func(top_coins):
    main_stake = None
    my_params.ind_strategy_number    

    if my_params.ind_strategy_number == 1:
        main_stake = get_orders_stek_1.get_tv_signals(top_coins, my_params.interval)
    elif my_params.ind_strategy_number == 2:
        main_stake = get_orders_stek_2.get_udf_strategy_signals(top_coins, my_params.interval)
    return main_stake

