import sys
import cv2
import numpy as np

import anchor_decode

#from anchor_decode import decode_bbox
import nms
#from anchor_generator import generate_anchors
import anchor_generator

# anchor configuration
feature_map_sizes = [[33, 33], [17, 17], [9, 9], [5, 5], [3, 3]]
anchor_sizes = [[0.04, 0.056], [0.08, 0.11], [0.16, 0.22], [0.32, 0.45], [0.64, 0.72]]
anchor_ratios = [[1, 0.62, 0.42]] * 5

# generate anchors
anchors =anchor_generator.generate_anchors(feature_map_sizes, anchor_sizes, anchor_ratios)

# for inference , the batch size is 1, the model output shape is [1, N, 4],
# so we expand dim for anchors to [1, anchor_num, 4]
anchors_exp = np.expand_dims(anchors, axis=0)

id2class = {0: 'Mask', 1: 'NoMask'}

def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def detect_mask(image_path, conf_thresh=0.5, iou_thresh=0.4, target_shape=(160, 160)):
 
    
    Net = cv2.dnn.readNet('./models/face_mask_detection.caffemodel','./models/face_mask_detection.prototxt')
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    height, width, _ = img.shape
    blob = cv2.dnn.blobFromImage(img, scalefactor=1/255.0, size=target_shape)
    Net.setInput(blob)
    y_bboxes_output, y_cls_output = Net.forward(getOutputsNames(Net))
    # remove the batch dimension, for batch is always 1 for inference.
    y_bboxes = anchor_decode.decode_bbox(anchors_exp, y_bboxes_output)[0]
    y_cls = y_cls_output[0]
    # To speed up, do single class NMS, not multiple classes NMS.
    bbox_max_scores = np.max(y_cls, axis=1)
    bbox_max_score_classes = np.argmax(y_cls, axis=1)

    # keep_idx is the alive bounding box after nms.
    keep_idxs = nms.single_class_non_max_suppression(y_bboxes, bbox_max_scores, conf_thresh=conf_thresh, iou_thresh=iou_thresh)
    result = "该学生未佩戴口罩。"
    results = []
    for idx in keep_idxs:
        conf = float(bbox_max_scores[idx])
        class_id = bbox_max_score_classes[idx]
        if class_id == 0:
            result = "该学生已佩戴口罩！"
            
        else:
            result = "该学生未佩戴口罩。"
           

    return result
