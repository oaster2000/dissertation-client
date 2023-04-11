import requests, json

class TweetData:

    URL = "http://oaster.pythonanywhere.com/"

    def __init__(self):
        self.tweet_count = 0
        self.dates = dict()
        self.polarity = dict()
        self.subjectivity = dict()
        self.place = dict()
        self.topic = dict()

        self.place_by_topic = dict()
        self.topic_by_date = dict()

        response = requests.get(url = self.URL + "/date")
        self.dates = response.json()

        response = requests.get(url = self.URL + "/sentiment/polarity")
        self.polarity = response.json()

        response = requests.get(url = self.URL + "/sentiment/subjectivity")
        self.subjectivity = response.json()

        response = requests.get(url = self.URL + "/topic")
        self.topic = response.json()

        response = requests.get(url = self.URL + "/place")
        self.place = response.json()

        response = requests.get(url = self.URL + "/place-topic")
        self.place_by_topic = response.json()
        
        response = requests.get(url = self.URL + "/topic-date")
        self.place_by_topic = response.json()

        with open('/home/oaster/dissertation-client/data/location_data.csv', 'w+', encoding="utf8") as f:
            f.write("name,number" + '\n')
            for item in self.place:
                f.write(item + "," + str(self.place.get(item)) + '\n')

    def getDateLabels(self):
        labels = []
        for item in self.dates:
            labels.append(item)
        return labels


    def getDateValues(self):
        values = []
        for item in self.dates:
            values.append(self.dates[item])
        return values

    def getPolarityValues(self):
        values = []
        for item in self.polarity:
            values.append(self.polarity[item])
        return values

    def getSubjectivityValues(self):
        values = []
        for item in self.subjectivity:
            values.append(self.subjectivity[item])
        return values

    def getTopicLabels(self):
        labels = []
        for item in self.topic:
            labels.append(item)
        return labels


    def getTopicValues(self):
        values = []
        for item in self.topic:
            values.append(self.topic[item])
        return values

    def getPlaceDataForTopics(self, topics):
        topics.split(",")
        with open('/home/oaster/dissertation-client/data/query_location_data.csv', 'w+', encoding="utf8") as f:
            f.write("name,number" + '\n')
            _data = dict()
            print(topics)
            for item in self.place_by_topic:
                if item.casefold() in topics.casefold():
                    for val in self.place_by_topic.get(item):
                        _data[val] = self.place_by_topic.get(item).get(val, 0) + 1

            print(_data)

            for item in _data:
                f.write(item + "," + str(_data.get(item)) + '\n')
                
    def getDateTopicData(self, topics):
        values = []
        topics.split(",")
        _data = dict()
        for item in self.topic_by_date:
            for val in self.topic_by_date.get(item):
                if val.casefold() in topics.casefold():
                    _data[item] += self.topic_by_date.get(item).get(val)
                    
        for item in _data:
            values.append(_data[item])
        
        print(values)