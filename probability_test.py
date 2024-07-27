import pandas as pd

from gameplay.humanoid import Humanoid

def confidence_test(n=10000):
    # test distribution of highest probabilities
    results = []
    for _ in range(n):
        h = Humanoid(None, None)
        results.append(max(h.raw_probs))
    s = pd.Series(results)
    print(s.describe())

def job_dist_test(n=10000):
    # test distribution of jobs assigned
    results = {'doctor':0, 'engineer':0, 'normal':0, 'thug':0, 'fatty':0, 'pessimist':0}
    for _ in range(n):
        h = Humanoid(None, None)
        if h.get_job() in results:
            results[h.get_job()] += 1
    print(results)

def pred_dist_test(n=10000):
    # test distribution of which job has highest probability
    results = {'doctor':0, 'engineer':0, 'normal':0, 'thug':0, 'fatty':0, 'pessimist':0}
    for _ in range(n):
        h = Humanoid(None, None)
        job = list(results.keys())[h.raw_probs.index(max(h.raw_probs))]
        results[job] += 1
    print(results)

if __name__ == "__main__":
    pred_dist_test()