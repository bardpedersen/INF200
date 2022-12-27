import pandas as pd


def funksjon(data):
    a = pd.DataFrame.from_dict(data, orient='columns', dtype=None, columns=None)
    df = pd.DataFrame(data)
    df['age'] = df['age'].astype(float)
    return df['age'].sum()


if __name__ == '__main__':

    data = [{'name': 'Joe', 'age': 22, 'phone': '12345678'},
            {'name': 'Pia', 'age': 24, 'phone': '23456789'},
            {'name': 'Even', 'age': 21, 'phone': '34567890'},
            {'name': 'Abdul', 'age': 23, 'phone': '45678901'}]

    print(funksjon(data))
