from fileinput import filename
import os
from pydoc import doc

userinput0 = float(input("What are we removing today? 0 - general sfw dataset | 1 - general nsfw dataset | 2 - just informational duplication removal: "))
while userinput0 not in [0,1,2]:
   userinput0 = float(input("please, enter a valid option number: "))

if userinput0 == 0:
    wanted_tags_file = "./unwanted_tags.txt"
elif userinput0 == 1:
    wanted_tags_file = "./unwanted_tags_2.txt"
elif userinput0 == 2:
    wanted_tags_file = "./unwanted_zero.txt"

def read_unwanted_tags(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        unwanted_tags = [tag.strip() for tag in file]
    return unwanted_tags

def remove_unwanted_tags(tags, unwanted_tags):
    filtered_tags = []
    for tag in tags:
        tag = tag.replace("_", " ")
        if tag not in unwanted_tags:
            filtered_tags.append(tag)
            
    return filtered_tags
   


def remove_repeated_tags(tags):
    filtered_tags = []
    for tag in tags:
        tag_words = tag.split(" ")
        is_more_specific = True
        for other_tag in tags:
            if tag != other_tag:
                other_tag_words = other_tag.split(" ")
                if all(word in other_tag_words for word in tag_words):
                    is_more_specific = False
                    break
        if is_more_specific:
            filtered_tags.append(tag)
    return filtered_tags

def process_tags_file(file_path, unwanted_tags):
    with open(file_path, "r", encoding="utf-8") as file:
        tag_string = file.read().strip()
    tags = [tag.strip().replace("_", " ") for tag in tag_string.split(",")]

    filtered_tags = remove_unwanted_tags(tags, unwanted_tags)
    filtered_tags = remove_repeated_tags(filtered_tags)
    print("Processed unwanted tags:", filtered_tags)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(",".join(filtered_tags))

    return filtered_tags


def process_tags_files(input_folder, output_folder, unwanted_tags_file):
    unwanted_tags = read_unwanted_tags(unwanted_tags_file)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name)

            process_tags_file(input_file_path, unwanted_tags)

            os.replace(input_file_path, output_file_path)

    print("Done.")

if __name__ == "__main__":
    input_folder = "./input_tags"
    output_folder = "./output_tags"
    unwanted_tags_file = "./unwanted_tags.txt"
    process_tags_files(input_folder, output_folder, unwanted_tags_file)
