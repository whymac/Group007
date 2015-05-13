import pandas as pd
import pandas.stats.ols as ols
import numpy as np
import scikits
import sys

def reg(filename):

    df = pd.DataFrame
    data = pd.read_csv(filename)

    # saveDf is the dataframe
    saveDf = df()

    regress = ols.OLS(y = np.log(data['revenue']), x = np.log(data['income']), intercept = True)

    print regress


def main():
    filename = sys.argv[1]
    reg(filename)


if __name__ == '__main__':
    main()