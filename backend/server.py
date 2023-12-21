#імпорт бібліотек
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from backend.services.data_pipeline import DataPipeline
from backend.services.read.read_service import ReadService
from backend.config.config_path import ConfigPath

# ===========================================================================
TRAIN_EXISTING_DF_COMBINED = ReadService.read_csv(ConfigPath.TRAIN_EXISTING_FILE_COMBINED_PATH)
TEST_EXISTING_DF_COMBINED = ReadService.read_csv(ConfigPath.TEST_EXISTING_FILE_COMBINED_PATH)
train_weather, test_weather, train_merged, test_merged = DataPipeline().merge_dfs_for_server()

app = Flask(__name__)
CORS(app)


def request(number):
    number_product = number

    train_selected_data = train_weather[train_weather['item_nbr'] == number_product]

    test_selected_data = test_weather[test_weather['item_nbr'] == number_product]

    # якщо в рядку codesum є значення дощу (RA) і в рядку preciptotal значення більше 1
    # або в рядку codesum є значення снігу (SN) і в рядку preciptotal значення більше 2
    train_poor_weather = train_selected_data[((train_selected_data['codesum'].str.contains('RA')) & (train_selected_data['preciptotal'] > 1)) | ((train_selected_data['codesum'].str.contains('SN')) & (train_selected_data['preciptotal'] > 2))]
    train_poor_weather=train_poor_weather.sort_values(by=['date'])

    test_poor_weather = test_selected_data[((test_selected_data['codesum'].str.contains('RA')) & (test_selected_data['preciptotal'] > 1)) | ((test_selected_data['codesum'].str.contains('SN')) & (test_selected_data['preciptotal'] > 2))]
    test_poor_weather=test_poor_weather.sort_values(by=['date'])

    # вибіраємо наступні 3 дні після снігу чи дощу
    train_existing_df = pd.DataFrame({'date': [], 'store_nbr': [], 'item_nbr':[],'units': [], 'station_nbr': [], 'codesum':[], 'preciptotal':[]})

    for i in range(len(train_poor_weather)):
        train_d1=train_selected_data[(train_selected_data['date'] == train_poor_weather['date'].iloc[i] + pd.DateOffset(days=1)) & (train_selected_data['store_nbr'] == train_poor_weather['store_nbr'].iloc[i])]
        train_existing_df= pd.concat([train_existing_df, train_d1], ignore_index=True)

        train_d2=train_selected_data[(train_selected_data['date'] == train_poor_weather['date'].iloc[i] + pd.DateOffset(days=2)) & (train_selected_data['store_nbr'] == train_poor_weather['store_nbr'].iloc[i])]
        train_existing_df = pd.concat([train_existing_df, train_d2], ignore_index=True)

        train_d3=train_selected_data[(train_selected_data['date'] == train_poor_weather['date'].iloc[i] + pd.DateOffset(days=3)) & (train_selected_data['store_nbr'] == train_poor_weather['store_nbr'].iloc[i])]
        train_existing_df = pd.concat([train_existing_df, train_d3], ignore_index=True)


    # вибіраємо наступні 3 дні після снігу чи дощу
    test_existing_df = pd.DataFrame({'date': [], 'store_nbr': [], 'item_nbr':[],'units': [], 'station_nbr': [], 'codesum':[], 'preciptotal':[]})

    for i in range(len(test_poor_weather)):
        test_d1=test_selected_data[(test_selected_data['date'] == test_poor_weather['date'].iloc[i] + pd.DateOffset(days=1)) & (test_selected_data['store_nbr'] == test_poor_weather['store_nbr'].iloc[i])]
        test_existing_df= pd.concat([test_existing_df, test_d1], ignore_index=True)

        test_d2=test_selected_data[(test_selected_data['date'] == test_poor_weather['date'].iloc[i] + pd.DateOffset(days=2)) & (test_selected_data['store_nbr'] == test_poor_weather['store_nbr'].iloc[i])]
        test_existing_df = pd.concat([test_existing_df, test_d2], ignore_index=True)

        test_d3=test_selected_data[(test_selected_data['date'] == test_poor_weather['date'].iloc[i] + pd.DateOffset(days=3)) & (test_selected_data['store_nbr'] == test_poor_weather['store_nbr'].iloc[i])]
        test_existing_df = pd.concat([test_existing_df, test_d3], ignore_index=True)


    # видаляєм однакові дані
    train_existing_df = train_existing_df.drop_duplicates()

    test_existing_df = test_existing_df.drop_duplicates()


    # заміна NaN значень
    train_existing_df.iloc[:, train_existing_df.columns.get_loc('preciptotal')].fillna(0.00, inplace=True)
    test_existing_df.iloc[:, test_existing_df.columns.get_loc('preciptotal')].fillna(100, inplace=True)

    # Для відправки даних з серверу
    SERVER_train_existing_df = train_existing_df
    SERVER_test_existing_df = test_existing_df


    # Обчислюємо суму стовпця "units"
    train_total_units = train_existing_df['units'].sum()
    test_total_units = test_existing_df['units'].sum()

    # plt.figure(figsize=(20, 5))
    # plt.plot(train_existing_df['date'], train_existing_df['units'], label = 'Train data')
    # plt.plot(test_existing_df['date'], test_existing_df['units'], label = 'Test data')
    # plt.legend()
    # plt.close()


    # Створюємо нову ознаку - день у році
    train_existing_df['dayofyear'] = train_existing_df['date'].dt.dayofyear
    test_existing_df['dayofyear'] = test_existing_df['date'].dt.dayofyear

    x_train = pd.DataFrame()
    x_train['dayofyear'] = train_existing_df['dayofyear']
    x_test = pd.DataFrame()
    x_test['dayofyear'] = test_existing_df['dayofyear']

    y_train = train_existing_df['units']
    y_test = test_existing_df['units']


    model = LinearRegression()
    model.fit(x_train, y_train)


    # Прогноз для тренувальних даних
    pred_train = model.predict(x_train)
    # Прогноз для даних, які модель ще не бачила
    pred_test = model.predict(x_test)


    # Перевіряємо якість чисельно
    # mean_squared_error - середня сума квадратів відхилень (менше -> краще)

    rmsle_train = mean_squared_error(y_train, pred_train)**0.5
    rmsle_test = mean_squared_error(y_test, pred_test)**0.5

    # plt.figure(figsize=(20, 5))
    # plt.scatter(x_train['dayofyear'], y_train, label='Train y(x)')
    # plt.scatter(x_test['dayofyear'], y_test, label='Test y(x)')
    # plt.scatter(x_test['dayofyear'], pred_test, label='Test predict', color='red')
    # plt.legend()
    return train_total_units, test_total_units, rmsle_train, rmsle_test, SERVER_train_existing_df, SERVER_test_existing_df, x_train, y_train, x_test, y_test, pred_test


@app.route('/get_data_and_plot', methods=['POST'])
def get_data_and_plot():
    data = request.json
    number = data['number']
    train_total_units, test_total_units, rmsle_train, rmsle_test, train_existing_df, test_existing_df, x_train, y_train, x_test, y_test, pred_test = request(number)
    train_existing_json = train_existing_df.to_json(orient='records')
    test_existing_json = test_existing_df.to_json(orient='records')
    x_train_json = x_train.to_json(orient='records')
    y_train_json = y_train.to_json(orient='records')
    x_test_json = x_test.to_json(orient='records')
    y_test_json = y_test.to_json(orient='records')

    TRAIN_EXISTING_DF_COMBINED_json = TRAIN_EXISTING_DF_COMBINED.to_json(orient='records')
    TEST_EXISTING_DF_COMBINED_json = TEST_EXISTING_DF_COMBINED.to_json(orient='records')
    pred_test_list = pred_test.tolist()
    response_data = {
        'train_total_units': train_total_units,
        'test_total_units': test_total_units,
        'rmsle_train': rmsle_train,
        'rmsle_test': rmsle_test,
        'train_existing_df': train_existing_json,
        'test_existing_df': test_existing_json,
        'x_train': x_train_json,
        'y_train': y_train_json,
        'x_test': x_test_json,
        'y_test': y_test_json,
        'TRAIN_EXISTING_DF_COMBINED': TRAIN_EXISTING_DF_COMBINED_json,
        'TEST_EXISTING_DF_COMBINED': TEST_EXISTING_DF_COMBINED_json,
        'pred_test': pred_test_list,
        }
    return jsonify(response_data)


@app.route('/get_train_and_test_data', methods=['GET'])
def get_train_and_test_data():
    TRAIN_EXISTING_DF_COMBINED_json = TRAIN_EXISTING_DF_COMBINED.to_json(orient='records')
    TEST_EXISTING_DF_COMBINED_json = TEST_EXISTING_DF_COMBINED.to_json(orient='records')
    response_data = {
        'TRAIN_EXISTING_DF_COMBINED': TRAIN_EXISTING_DF_COMBINED_json,
        'TEST_EXISTING_DF_COMBINED': TEST_EXISTING_DF_COMBINED_json,
        }
    return jsonify(response_data)


if __name__ == '__main__':
    app.run()






