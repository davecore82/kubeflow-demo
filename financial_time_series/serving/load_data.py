import numpy as np
#pylint: disable=no-name-in-module
import preprocess

def load_closing_data(es_endpoint):
  tickers = ['snp', 'nyse', 'djia', 'nikkei', 'hangseng', 'ftse', 'dax', 'aord']
  closing_data = preprocess.load_data(tickers, es_endpoint)
  return closing_data


def get_formatted_data(closing_data, preprocessed_data, date):
    index = closing_data.index.get_loc(date)
    print(closing_data.iloc[index, :])
    input_tensor = np.expand_dims(
      preprocessed_data[preprocessed_data.columns[2:]].values[index - 7],
      axis=0).astype(np.float32)
    return input_tensor

