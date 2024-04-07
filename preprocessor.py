import pandas as pd
import re

def preprocess(data):
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\]'

    messages = re.split(pattern, data)
   
    dates = re.findall(pattern, data)


# Assuming 'messages' and 'dates' are your lists containing user messages and message dates
# Padding the shorter list: You can add placeholder values (e.g., None or empty strings) to the shorter list to match the length of the longer list.
# Padding the shorter list with None values
    if len(messages) < len(dates):
     messages += [None] * (len(dates) - len(messages))
    elif len(dates) < len(messages):
     dates += [None] * (len(messages) - len(dates))

# Create DataFrame
    data = pd.DataFrame({'user_message': messages, 'message_date': dates})

# Remove square brackets from datetime strings
    data['message_date'] = data['message_date'].str.strip('[]')

# Convert to datetime, errors='coerce' parameter allows parsing to continue even if some values are invalid, turning them into NaT (Not a Time).
    data['message_date'] = pd.to_datetime(data['message_date'], format='%d/%m/%Y, %H:%M:%S', errors='coerce')

# Drop rows with invalid datetime values
    data = data.dropna(subset=['message_date'])

# Rename column
    data.rename(columns={'message_date': 'date'}, inplace=True)

# separate users and messages
    users = []
    messages = []
    for message in data['user_message']:
     entry = re.split('([\w\W]+?):\s', message)
     if entry[1:]: #user name
        users.append(entry[1])
        messages.append(entry[2])
     else:
        users.append('group_notification')
        messages.append(entry[0])

    data['user'] = users
    data['message'] = messages
    data.drop(columns=['user_message'], inplace=True)

    data['only_date'] = data['date'].dt.date
    data['year']= data['date'].dt.year
    data['month_num'] = data['date'].dt.month
    data['month'] = data['date'].dt.month_name()
    data['day'] = data['date'].dt.day
    data['day_name'] = data['date'].dt.day_name()
    data['hour'] = data['date'].dt.hour
    data['minute'] = data['date'].dt.minute

    period = []
    for hour in data[['day_name','hour']]['hour']:
      if hour == 23:
        period.append(str(hour) + "-" +str('00'))
      elif hour == 0:
        period.append(str('00') + "-" + str(hour+1))
      else:
        period.append(str(hour) + "-" + str(hour+1))

    data['period'] = period

    return data
#Example usage:
#data = preprocess(your_data)