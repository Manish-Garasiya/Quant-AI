def walk_forward_windows(df, train_years=3, test_years=1):
    df = df.copy().sort_index()
    years = sorted(df.index.year.unique())

    windows = []
    for i in range(len(years) - train_years - test_years + 1):
        train_start_year = years[i]
        train_end_year = years[i + train_years - 1]
        test_end_year = years[i + train_years + test_years - 1]

        train = df[(df.index.year >= train_start_year) & (df.index.year <= train_end_year)]
        test = df[(df.index.year == test_end_year)]

        if len(train) > 0 and len(test) > 0:
            windows.append((train, test))

    return windows