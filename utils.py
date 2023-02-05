from typing import AnyStr
import pandas as pd
import numpy
from statsmodels.tsa.arima.model import ARIMA


class FetchData:

    def read_data(self) -> pd.DataFrame:
        """
        Read data from a file
        :param input_path: The path to the file to be read
        :return: The data read from the file
        """
        return pd.read_csv(self.data_path, header=0)

    def __init__(self, data_path: AnyStr):
        self.data_path = data_path
        self.df = self.read_data()
        self.model = None
        self.model_fit = None
        self.X = None

    # def transform_df(self):
    #     """
    #     Transform the data
    #     :return:
    #     """
    #     self.df['Datetime'] = pd.to_datetime(pd.date_range(start='2021-01-01', end='2021-12-31'))
    #     self.df = self.df.set_index(['Datetime'])
    #
    #     self.df['month'] = self.df['# Date'].apply(lambda x: int(x.split('-')[1]))
    #     self.df['day'] = self.df['# Date'].apply(lambda x: int(x.split('-')[2]))
    #
    #     month_seasons = {1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3, 12: 0}
    #     self.df['season'] = self.df['month'].apply(lambda x: month_seasons[x])
    #
    #     self.df['Date'] = pd.to_datetime(self.df['# Date'], format='%Y/%m/%d')
    #     self.df['day_of_year'] = pd.DatetimeIndex(self.df['Date']).dayofyear
    #     self.df['week_of_year'] = pd.DatetimeIndex(self.df['Date']).weekofyear
    #     self.df['quarter'] = pd.DatetimeIndex(self.df['Date']).quarter
    #     self.df['dayofweek'] = pd.DatetimeIndex(self.df['Date']).dayofweek
    #     self.df['Sunday'] = self.df['dayofweek'].apply(lambda x: 1 if x == 6 else 0)
    #     self.df['Saturday'] = self.df['dayofweek'].apply(lambda x: 1 if x == 5 else 0)
    #
    #     # Assuming the data is for US
    #     self.df['hols'] = pd.Series(self.df.index).apply(
    #         lambda x: holidays.CountryHoliday('US', prov='NSW').get(x)).values
    #     self.df['hols'] = self.df['hols'].apply(lambda x: 1 if x != None else 0)
    #
    #     del self.df['# Date']

    def difference(self, interval=1):
        '''
        Since the data is non-stationary (which we discovered during EDA(check fetch-eda.ipynb)) 
        we use this function to find subsequent differences to mitigate that. This makes the data
        stationary (in our case atleast since the sales increase isnt exponential.)
        '''
        diff = list()
        for i in range(interval, len(self.X)):
            value = self.X[i][1] - self.X[i - interval][1]
            diff.append(value)
        return numpy.array(diff)

    def inverse_difference(self, history, yhat, interval=1):
        '''
        Since the model learns to predict the differences between current and next prediction,
        we'll have invert that calculation to get the sales of the next days.
        '''
        return yhat + history[-interval][1]

    def train(self):
        '''
        Train the model based on the data. 
        '''
        # seasonal difference
        self.X = self.df.values
        days_in_year = 1
        computed_difference = self.difference(days_in_year)
        # fit model
        self.model = ARIMA(computed_difference, order=(7, 0, 1))
        self.model_fit = self.model.fit()

    def predict(self):
        '''
        Predicting next year's data.
        '''
        forecast = self.model_fit.forecast(steps=365)
        # invert the differenced forecast to something usable
        history = [x for x in self.X]
        day = 1
        month_de = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        month_de_pro = [0]
        for i in range(1, len(month_de)):
            month_de_pro.append(month_de[i - 1] + month_de_pro[i - 1])
        month_de_pro.append(365)
        # month_de_pro = [ month_de[i]+month_de[i-1]  for i in range(1,len(month_de))]
        idx = 1
        summ = 0
        month_wise = []

        for yhat in forecast:
            inverted = self.inverse_difference(history, yhat, 1)
            #     print('Day %d: %f' % (day, inverted))
            summ += inverted
            if month_de_pro[idx] == day:
                month_wise.append(summ)
                summ = 0
                idx = idx + 1

            history.append(['Day %d: %f' % (day, inverted), inverted])
            day += 1
        return month_wise

