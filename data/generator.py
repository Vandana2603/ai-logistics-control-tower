import pandas as pd
import random

def generate_data(n=800):
    data = []

    for _ in range(n):
        orders = random.randint(50, 500)
        workers = random.randint(5, 50)
        safety = random.randint(0, 5)
        productivity = random.randint(60, 100)

        delay = 1 if (orders / workers > 10 or safety > 3) else 0

        data.append([orders, workers, safety, productivity, delay])

    df = pd.DataFrame(data, columns=[
        "orders", "workers", "safety", "productivity", "delay"
    ])

    return df