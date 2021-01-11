import datetime

def fit_sentiment_days(sentiment_analysis, data):
    data['datatime'] = data.index
    list_data = data.values.tolist()
    list_data = sorted(list_data, key=lambda a: a[-1])

    list_sentiment_analysis = sentiment_analysis.values.tolist()
    list_sentiment_analysis = sorted(
        list_sentiment_analysis, key=lambda a: a[1])

    result = []
    actual_pos_sentiment = 0
    actual_date = datetime.date(list_data[0][-1])
    temp_list = [0]
    for i in list_data:

        if actual_date < datetime.date(i[-1]):
            actual_date = datetime.date(i[-1])
            temp_list = [0]

        if list_sentiment_analysis[actual_pos_sentiment][1] > i[-1]:
            result.append(
                [i[-1], float(sum(temp_list)) / float(len(temp_list))])
        else:
            if temp_list == [0]:
                temp_list = [list_sentiment_analysis[actual_pos_sentiment][-1]]
            else:
                temp_list.append(
                    list_sentiment_analysis[actual_pos_sentiment][-1])
            actual_pos_sentiment += 1

            while list_sentiment_analysis[actual_pos_sentiment+1][1] < i[-1]:
                temp_list.append(
                    list_sentiment_analysis[actual_pos_sentiment][-1])
                actual_pos_sentiment += 1
            result.append(
                [i[-1], float(sum(temp_list)) / float(len(temp_list))])

    df = pd.DataFrame(result, index=[i[0] for i in result],
                      columns=['DateTime', 'Average_news'])

    return df
