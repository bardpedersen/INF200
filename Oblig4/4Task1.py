def to_records(data):
    recs = []
    keys = list(data.keys())
    num_keys = len(list(data.keys()))
    num_rec = len(next(iter(data.values())))

    for nr in range(num_rec):
        records = {}
        for key in keys:
            records[key] = data[key][nr]
        recs.append(records)
    print(recs)

if __name__ == '__main__':
    data = {'name': ['Joe', 'Pia', 'Even', 'Abdul'],'age': [22, 24, 21, 23],'phone': ['12345678', '23456789', '34567890', '45678901']}
    to_records(data)