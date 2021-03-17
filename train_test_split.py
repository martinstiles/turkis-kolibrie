from sklearn.model_selection import train_test_split

def get_train_test_split(df):
    columns = []  # Insert columns
    data = df[columns]
    labels = df["labels"]

    x_train, x_test, y_train, y_test = train_test_split(
        data,
        labels,
        test_size = 0.33,
        random_state = 69
    )

    return x_train, x_test, y_train, y_test
