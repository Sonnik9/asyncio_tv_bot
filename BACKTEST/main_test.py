# import backtrader as bt
# from datetime import datetime 

# def calculate_signals(data):
#     # Рассчитываем индикаторы Боллинджера
#     bollinger = bt.indicators.BollingerBands(data.close)

#     # Рассчитываем индикатор MACD
#     macd = bt.indicators.MACD(data.close)

#     # Проверяем условия для сигналов
#     if bollinger.lines.bot > data.close and macd.lines.macd > macd.lines.signal:
#         return "buy"  # Сигнал на покупку
#     elif bollinger.lines.top < data.close and macd.lines.macd < macd.lines.signal:
#         return "sell"  # Сигнал на продажу
#     else:
#         return "neutral"  # Нейтральный сигнал

# class MyStrategy(bt.Strategy):
#     params = (
#         ("take_profit_percent", 0.03),  # Уровень тейк-профита в процентах
#         ("stop_loss_percent", 0.02),    # Уровень стоп-лосса в процентах
#     )

#     def __init__(self):
#         self.signal = None  # Переменная для хранения сигнала

#     def next(self):
#         # Вызываем функцию для расчета сигнала
#         self.signal = calculate_signals(self.data)

#         # Проверка сигнала для входа и выхода из позиции
#         if self.signal == "buy" and not self.position:
#             # Рассчитываем размер позиции (пример - 10 контрактов)
#             position_size = 10
#             self.buy(size=position_size)

#         elif self.signal == "sell" and not self.position:
#             # Рассчитываем размер позиции (пример - 10 контрактов)
#             position_size = 10
#             self.sell(size=position_size)

#         elif self.signal == "neutral" and self.position:
#             self.close()  # Закрыть текущую позицию

# if __name__ == "__main__":
#     cerebro = bt.Cerebro()

#     # Загрузка данных из файла CSV
#     data = bt.feeds.GenericCSVData(
#         dataname='your_data.csv',
#         fromdate=datetime(2020, 1, 1),
#         todate=datetime(2021, 12, 31),
#         nullvalue=0.0,
#         dtformat=('%Y-%m-%d'),
#         datetime=0,
#         high=2,
#         low=3,
#         open=1,
#         close=4,
#         volume=5,
#         openinterest=-1
#     )

#     cerebro.adddata(data)
#     cerebro.addstrategy(MyStrategy)

#     # Установка начального капитала
#     cerebro.broker.set_cash(100000)

#     # Установка размера позиции
#     cerebro.addsizer(bt.sizers.SizerFix, stake=10)

#     # Установка комиссии и спреда (если требуется)
#     cerebro.broker.setcommission(commission=0.001)

#     # Запуск бэктестинга
#     cerebro.run()

#     # Вывод результатов
#     print(f"Итоговый баланс: {cerebro.broker.getvalue()}")

# from datetime import datetime
# import backtrader as bt

# class SmaSignal(bt.Signal):
#     param = (('period', 20), )

#     def __init__(self):
#         self.lines.signal = self.data - bt.ind.SMA(period=self.p.period)

# data = bt.feeds.YahooFinanceData(dataname='AAPL',
#                                 fromdate=datetime(2018, 1, 1),
#                                 todate=datetime(2018, 12, 31))
# cerebro = bt.Cerebro(stdstats=False)
# cerebro.adddata(data)
# cerebro.broker.setcash(1000.0)
# cerebro.add_signal(bt.SIGNAL_LONG, SmaSignal)
# cerebro.addobserver(bt.observers.BuySell)
# cerebro.addobserver(bt.observers.Value)

# print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
# cerebro.run()
# print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')
# cerebro.plot(iplot=True, volume=False)

from datetime import datetime
import backtrader as bt
import yfinance as yf
import pandas as pd

# Определите класс стратегии
class MyStrategy(bt.Strategy):
    params = (
        ("sma_period", 20),
    )

    def __init__(self):
        self.data_close = self.datas[0].close
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.sma_period)

    def next(self):
        if self.data_close[0] > self.sma[0]:
            # Реализуйте ваше торговое действие здесь, например, покупку
            self.buy()

# Создайте объект Cerebro (основной класс backtrader)
if __name__=="__main__":


    # Задаем символ акции и временной интервал
    symbol = 'MSFT'
    start_date = '2020-01-01'
    end_date = '2022-12-31'

    # Загружаем исторические данные с Yahoo Finance
    data = yf.download(symbol, start=start_date, end=end_date)

    # Сохраняем данные в CSV-файл
    data.to_csv(f'{symbol}_historical_data.csv')

    cerebro = bt.Cerebro()

    # Добавьте стратегию к Cerebro
    cerebro.addstrategy(MyStrategy)

    # Загрузите данные из CSV-файла
    data = bt.feeds.GenericCSVData(
        dataname= f'{symbol}_historical_data.csv',
        fromdate=datetime(2023, 1, 1),
        todate=datetime(2023, 12, 31),
        nullvalue=0.0,
        dtformat=('%Y-%m-%d'),
        datetime=0,
        high=-1,
        low=-1,
        open=-1,
        close=1,
        volume=-1,
        openinterest=-1
    )

    cerebro.adddata(data)

    # Настройте параметры брокера и начальный капитал
    cerebro.broker.set_cash(100000)  # Установите начальный капитал
    cerebro.broker.setcommission(commission=0.001)  # Установите комиссию

    # Запустите бэктест
    cerebro.run()

    # Выведите результаты
    print(f"Итоговый капитал: {cerebro.broker.getvalue():.2f}")

    # Отобразите графики (опционально)
    # cerebro.plot()


# python -m BACKTEST.main_test
