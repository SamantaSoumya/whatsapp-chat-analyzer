import re
import pandas as pd

def preprocess(data):
    # seperate pattern for 12 hour formate  and 24 hour formate
    if re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s', data):
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'
    else:
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)

    df=pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date']=df['message_date'].str.replace('pm', 'PM').str.replace('am', 'AM')

    # Try all known date formats; fall back to mixed parsing for pandas 3.x compatibility
    is_12hr = re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s', df['message_date'].iloc[0])
    parsed = False
    if is_12hr:
        for fmt in ['%d/%m/%y, %I:%M %p - ', '%d/%m/%Y, %I:%M %p - ',
                    '%m/%d/%y, %I:%M %p - ', '%m/%d/%Y, %I:%M %p - ']:
            try:
                df['message_date'] = pd.to_datetime(df['message_date'], format=fmt)
                parsed = True
                break
            except Exception:
                continue
    else:
        for fmt in ['%d/%m/%y, %H:%M - ', '%d/%m/%Y, %H:%M - ',
                    '%m/%d/%y, %H:%M - ', '%m/%d/%Y, %H:%M - ']:
            try:
                df['message_date'] = pd.to_datetime(df['message_date'], format=fmt)
                parsed = True
                break
            except Exception:
                continue
    if not parsed:
        # Last resort: let pandas infer format
        df['message_date'] = pd.to_datetime(df['message_date'], format='mixed', dayfirst=True)

    df.rename(columns={'message_date':'date'},inplace=True)

    users=[]
    messages=[]
    for message in df['user_message']:
        entry=re.split(r'([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df.drop(columns=['user_message'],inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year']=df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df