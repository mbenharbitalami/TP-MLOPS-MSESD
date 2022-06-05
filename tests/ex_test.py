import pandas as pd
from src.train import get_feat_and_target

def test_get_feat_and_target():
    df = pd.DataFrame(columns=['A', 'B', 'C'])
    target = 'B'
    x, y = get_feat_and_target(df, target)
    assert all([a == b for a, b in zip(x.columns, ['A','C'])])
    assert all([a == b for a, b in zip(y.columns, ['B'])])

def somme(a,b):
    return a + b

def test_somme():
    a = 15
    b = 15
    assert somme(a,b) == 30