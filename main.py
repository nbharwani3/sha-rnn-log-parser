import os
import csv

path = os.getcwd()
filepath = os.path.join(path, "fully_connected.log")
f = open(filepath, "r")

def addToValues(list, epoch, key, value):
    if (key == "epoch" or key == "endofepoch") and value not in list.keys():
        list[value] = {}
        return

    if key not in list[epoch].keys():
        list[epoch][key] = []
    list[epoch][key].append(value)



values_iteration = {}
values_end_of_iteration = {}
values_end_of_training = {}

for line in f.readlines():
    curr_epoch = -1
    if line[0] == '|':
        tokens = line.split('|')

        isEndEpochLine = False
        endOfTraining = False

        for token in tokens:
            words = token.split(' ')
            while "" in words:
                words.remove("")

            key = ''

            if len(words) == 0:
                continue

            value = words[-1]
            key = "".join(words[:-1])

            if 'Endoftraining' == "".join(words):
                endOfTraining = True
                continue

            if key == 'endofepoch':
                isEndEpochLine = True
                curr_epoch = float(value)

            if key == 'batches' or value == 'batches':
                continue

            if key == "time:":
                value = value[:-1]

            if key == "testbpc:" or key == 'bpc':
                value = value[:-1]

            if key == "epoch":
                curr_epoch = float(value)

            if not endOfTraining:
                if isEndEpochLine:
                    addToValues(values_end_of_iteration, curr_epoch, key, float(value))
                else:
                    addToValues(values_iteration, curr_epoch, key, float(value))
            else:
                if key == "testloss":
                    values_end_of_training[key] = value
                if key == "testppl":
                    values_end_of_training[key] = value
                if key == "testbpc":
                    values_end_of_training[key] = value




with open('epochs.csv', mode='w') as epochs_file:
    epochs = values_iteration.keys()
    tags = values_iteration[0].keys()

    epochs_writer = csv.writer(epochs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    titles = list(tags)

    epochs_writer.writerow(titles)

    for epoch in epochs:
        value = []
        for tag in tags:
            value.append(str(sum(values_iteration[epoch][tag]) / len(values_iteration[epoch][tag])))
        epochs_writer.writerow(value)


with open('end_of_epoch.csv', mode='w') as epochs_file:
    epochs = values_end_of_iteration.keys()
    tags = values_end_of_iteration[1.0].keys()

    epochs_writer = csv.writer(epochs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    titles = list(tags)

    epochs_writer.writerow(titles)

    for epoch in epochs:
        value = []
        for tag in tags:
            value.append(values_end_of_iteration[epoch][tag][0])
        epochs_writer.writerow(value)






