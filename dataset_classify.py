import os
import shutil
from xml.etree import ElementTree as ET

# Defining the path to the dataset folder
dataset_folder = "C:\\Users\\nitee\\Downloads\\RDD2022_India\\India\\train"
 

# Defining the output folders for each class
output_folder = "C:\\Users\\nitee\\Downloads\\output"  
classes = ["D00", "D10", "D20", "D40"]

def create_class_folders(output_folder, classes):
    # Creating folders for each class if they do not exist
    for cls in classes:
        cls_folder = os.path.join(output_folder, cls)
        if not os.path.exists(cls_folder):
            os.makedirs(cls_folder)

def get_class_label(obj):
    # Getting the class label from the XML structure
    name_elem = obj.find("name")
    if name_elem is not None:
        return name_elem.text
    return None

def move_images(dataset_folder, output_folder):
    # Iterating through each image and its corresponding annotation
    for root, _, files in os.walk(dataset_folder):
        for file in files:
            if file.endswith(".xml"):
                
                xml_file = os.path.join(root, file)
                tree = ET.parse(xml_file)
                root_elem = tree.getroot()

                # Getting the image filename and path
                image_file = root_elem.find(".//filename").text
                image_path = os.path.join(root, image_file)

                # Getting the class label
                class_label = None
                for obj in root_elem.findall(".//object"):
                    class_label = get_class_label(obj)
                    if class_label is not None:
                        break

                # If class label is not found, skip the file
                if class_label is None:
                    print(f"Error: No class label found in {file}")
                    continue

                # Defining the destination folder based on the class label
                dest_folder = os.path.join(output_folder, class_label)

                # Creating the class folder if it does not exist
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)

                # Moving the image to the corresponding class folder
                if os.path.exists(image_path):
                    shutil.copy(image_path, dest_folder)

# calling the create_class_folders function folders for each class
create_class_folders(output_folder, classes)

# calling the Move_images to corresponding class folders
move_images(dataset_folder, output_folder)
