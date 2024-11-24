import pandas as pd


def save_params(acc,iou, dice):
    data = {
        'acc': [acc],
        'iou': [iou],
        'dice': [dice],
    }

    # Convert the dictionary into a pandas DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv('.\params_data\parameters.csv', mode='a', index=False)