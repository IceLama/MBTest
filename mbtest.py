import numpy as np
import pandas as pd
import time


test_data = pd.DataFrame({
    "customer_id": np.random.randint(1, 5, size=100),
    "product_id": np.random.randint(1000, 2000, size=100),
    "timestamp": np.arange(0, 5000, 50, dtype="datetime64[s]")
                        })
print(test_data)


def put_session_id(data: pd.DataFrame):
    customers = list(set(data["customer_id"].values))
    print(customers)
    session_id = pd.Series(np.zeros(len(data), dtype=int), name="session_id")
    pd.concat([data, session_id], axis=1)
    for i in customers:
        data.loc[data["customer_id"] == i, "session_id"] = i
        indexes = data.loc[data["customer_id"] == i].index
        for idx, index in np.ndenumerate(indexes):
            idx = idx[0]
            if (data["timestamp"][indexes[idx]] - data["timestamp"][indexes[idx - 1]]).total_seconds() < 180:
                pass
            else:
                data[index:].loc[data["customer_id"] == i, "session_id"] += 100
    return data


t0 = time.time()
data_1 = put_session_id(test_data)
t1 = time.time()
print(t1-t0)
print(data_1.loc[data_1["customer_id"] == 2])
print(data_1.loc[data_1["customer_id"] == 3])
print(data_1.loc[data_1["customer_id"] == 4])