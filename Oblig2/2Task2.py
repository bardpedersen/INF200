def weather(file):
    data = []
    with open(file, encoding='latin-1') as w_file:
        w_file.readline()  # skip header of CSV file
        while line := w_file.readline():
            tokens = line.split(';')
            day, month, year = tokens[0].split('.')
            record = {'Date': f'{int(year):04d}-{int(month):02d}-{int(day):02d}',
                      'T_avg': float(tokens[1]),
                      'T_min': float(tokens[2]),
                      'T_max': float(tokens[3]),
                      'Glob': float(tokens[4]),
                      'UV_rel': float(tokens[5])}
            data.append(record)
    return data

if __name__ == '__main__':
    a = weather('weather_umb_2012.csv')
    for rec in a[::53]:
        print(rec)