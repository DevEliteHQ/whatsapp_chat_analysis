import re
import pandas as pd

def preprocessor(chat: str):
    pattern = r"(?P<datetime>\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s?[ap]m)\s*-\s*(?:(?P<sender>.*?):\s*)?(?P<message>.*)"
    matches = re.findall(pattern, chat, re.MULTILINE)

    datetime_str = []
    sender = []
    message = []

    for match in matches:
        datetime_str.append(match[0])

        if match[1] == "":
            sender.append("group_notification")
        else:
            sender.append(match[1])
        message.append(match[2])

    df = pd.DataFrame({"date_time": datetime_str, "user": sender, "message": message})
    # df.sort_values(by=["date_time"], inplace=True)
    df["date_time"] = pd.to_datetime(df["date_time"], format="%d/%m/%y, %I:%M %p")

    # cleaned data
    df['year'] = df['date_time'].dt.year
    df['month'] = df['date_time'].dt.month_name()
    df['day'] = df['date_time'].dt.day
    df['month_num'] = df['date_time'].dt.month
    df['date'] = df['date_time'].dt.date
    df['day_name'] = df['date_time'].dt.day_name()
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute
    
    period = []

    for hour in df['hour']:
        if hour == 23:
            period.append(f'{hour}-00')
        elif hour == 0:
            period.append(f'00-{hour+1}')
        else:
            period.append(f'{hour}-{hour+1}')

    df['period'] = period
    
    df.drop(columns=['date_time'], axis = 1, inplace=True)
    
    return df
