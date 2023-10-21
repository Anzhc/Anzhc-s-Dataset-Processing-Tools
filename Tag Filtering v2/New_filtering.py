from fileinput import filename
import os
from pydoc import doc

def user_selection(prompt, valid_options):
    user_input = float(input(prompt))
    while user_input not in valid_options:
        user_input = float(input("Please enter a valid option number: "))
    return user_input

def read_unwanted_tags(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        unwanted_tags = [tag.strip().replace("_", " ") for tag in file]
    return set(unwanted_tags)  # Convert list to set


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


def process_tags_files(input_folder, output_folder, unwanted_tags):
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name)

            process_tags_file(input_file_path, unwanted_tags)

            os.replace(input_file_path, output_file_path)
    print("Done.")

def check_tags_in_lists(input_folder, tag_files):
    all_tags = set()  # Initialize as set
    for tag_file in tag_files.values():
        with open(tag_file, "r", encoding="utf-8") as file:
            all_tags.update({tag.strip().replace("_", " ") for tag in file})

    tags_not_in_list = set()  # Initialize as set
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            with open(os.path.join(input_folder, file_name), "r", encoding="utf-8") as file:
                tags = {tag.strip().replace("_", " ") for tag in file.read().split(",")}
                tags_not_in_list.update(tags - all_tags)  # Use set difference operator

    return list(tags_not_in_list)  # Convert set to list before returning

if __name__ == "__main__":
    tag_groups = {
        "general": "./General.txt",
        "artist": "./Artist.txt",
        "character": "./Character.txt",
        "copyright": "./Copyright.txt",
        "meta": "./Meta.txt"
    }

    tag_group_selections = []
    for tag_group in tag_groups:
        prompt = f"Do you want to use the {tag_group} tag list? 0 - No | 1 - Yes: "
        selection = user_selection(prompt, [0, 1])
        if selection == 1:
            tag_group_selections.append(tag_groups[tag_group])

    unwanted_tags = set()  # Initialize as set
    for tag_group_file in tag_group_selections:
        unwanted_tags |= read_unwanted_tags(tag_group_file)

    input_folder = "./input_tags"
    output_folder = "./output_tags"
    process_tags_files(input_folder, output_folder, unwanted_tags)

    userinput0 = user_selection("Do you want to do a second pass with another list? 0 - No | 1 - Yes: ", [0, 1])
    if userinput0 == 1:
        second_pass_list = "./unwanted_tags_2.txt"
        unwanted_tags_2 = read_unwanted_tags(second_pass_list)
        process_tags_files(output_folder, output_folder, unwanted_tags_2)

    tags_not_in_list = check_tags_in_lists(output_folder, tag_groups)  # use tag_groups instead of tag_group_selections
    print("Tags not in any list:", tags_not_in_list)

    userinput1 = user_selection("Do you want to remove tags not in any list? 0 - No | 1 - Yes: ", [0, 1])
    if userinput1 == 1:
        process_tags_files(output_folder, output_folder, tags_not_in_list)