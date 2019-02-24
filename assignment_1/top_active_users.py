
from urllib.request import urlopen


def find_active_users(data):
    """
    :param data: file data
    :return: 3 most activate users from conversation based on average of total appearance of person and involvement of
     the person in conversation
    """
    total_occurence, total_characters, conv_data = conversation_data(data)
    final_data ={}
    for key, value in conv_data.items():
        per_occ = round(conv_data[key]['occurrence'] * 100 /total_occurence, 2)
        per_char= round(conv_data[key]['characters'] * 100 / total_characters, 2)
        final_data[key] = round((per_occ + per_char) / 2, 2)

    top_3_active_people =[i[0] for i in sorted(final_data.items(), key=lambda x: -x[1])[:3]]
    return top_3_active_people


def conversation_data(data):
    """
    :param data: file data
    :return: total occurrence of people, total characters, and individual count of this two of respective people from the conversation
    """
    conv_data = {}
    total_occurrence = 0
    total_characters = 0

    for line in data:
        line = line.decode('UTF-8')

        if line.rstrip():
            person, conversation = get_person_name(line), get_conversation(line)

            if person in conv_data:
                conv_data[person]['occurrence'] = conv_data[person]['occurrence'] + 1
                conv_data[person]['characters'] = conv_data[person]['characters'] + len(conversation)
            else:
                conv_data[person] = {'occurrence': 1, 'characters': len(conversation)}

            total_occurrence += 1
            total_characters += len(conversation)

    return total_occurrence, total_characters, conv_data

def get_person_name(line):
    """
    :param line: conversation line with speaker
    :return: name of the speaker
    """
    return line.split("<")[1].split(">")[0]

def get_conversation(line):
    """
    :param line: conversation line with speaker
    :return: only conversation
    """
    return line.split(":")[1].strip()


if __name__ == "__main__":
    data = urlopen("https://s3.ap-south-1.amazonaws.com/haptikinterview/chats.txt")
    active_people = find_active_users(data)
    print("3 most active users in the conversation are {}".format(', '.join(active_people)))