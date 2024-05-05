import matplotlib.pyplot as plt
import pandas as pd
import requests
def get_data(station, element, elem_name, time, id_file='frost_client-id.txt'):
    client_id = open(id_file).read().strip()
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {'sources': station,
                  'elements': element,
                  'referencetime': time}
    frost_response = requests.get(endpoint, parameters, auth=(client_id, ' '))
    assert frost_response.status_code == 200
    frost_payload = frost_response.json()
    temp_data = [{'Time': pd.to_datetime(entry['referenceTime']),
                  elem_name: entry['observations'][0]['value']}
                 for entry in frost_payload['data']                 ]
    return pd.DataFrame.from_records(temp_data).set_index('Time')

if __name__ == '__main__':
    t_aas = get_data('SN17850', 'mean(air_temperature P1D)',
    'T_avg', '2021-01-01/2021-09-26')
    t_oslo = get_data('SN18700', 'mean(air_temperature P1D)',
    'T_avg', '2021-01-01/2021-09-26')
    plt.figure()
    plt.plot(t_aas.index, t_aas.T_avg, label='Ås')
    plt.plot(t_oslo.index, t_oslo.T_avg, label='Blindern')
    plt.title('Daily Average Temperature')
    plt.legend()
    # Displays the legend in the plot
    plt.figure()
    plt.scatter(t_aas.T_avg, t_oslo.T_avg)
    plt.xlabel('Ås')
    plt.ylabel('Blindern')
    t_all = pd.merge(t_aas, t_oslo, left_index=True, right_index=True,
    suffixes=(' Ås', ' Blindern'))
    t_all.plot(title='Daily Average Temperature')
    t_all.plot(kind='scatter', x='T_avg Ås', y='T_avg Blindern')
    plt.show()