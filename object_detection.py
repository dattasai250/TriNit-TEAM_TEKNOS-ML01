import cv2
import numpy as np
import os

# Load YOLO
net = cv2.dnn.readNet("C:\\Users\\nitee\\Downloads\\archive\\yolov3.weights", "C:\\Users\\nitee\\Downloads\\yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i- 1] for i in net.getUnconnectedOutLayers()]

# Function to perform object detection
def detect_objects(image_path):
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Unable to read the image. Please check the image path.")
        return
    height, width, _ = img.shape

    # Detect objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected is a road
                if class_id == 67:  # Assuming class_id 67 is for roads (You need to confirm this)
                    # Get coordinates of the object
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

    # Non-maximum suppression to remove overlapping boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Save the image with detected objects
    output_image = "detected_objects.jpg"
    cv2.imwrite(output_image, img)
    print("Detected objects image saved as '{}'".format(output_image))

    # Get the current working directory
    current_dir = os.getcwd()
    # Create the absolute path to the output image
    output_image_path = os.path.join(current_dir, output_image)
    print("Link to the detected objects image: file://{}".format(output_image_path.replace("\\", "/")))

# Call the function with the path to the image
detect_objects("C:\\Users\\nitee\\Downloads\\RDD2022_India\\India\\test\\images\\India_000015.jpg")
