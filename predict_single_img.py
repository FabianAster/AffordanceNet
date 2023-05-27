import tensorflow as tf
import sys
from os import walk
from tensorflow import keras
from utils import io_utils, data_utils, train_utils, bbox_utils, drawing_utils, eval_utils
from models import affordancenet
import os
import numpy as np
import pickle
import importlib
from PIL import Image


if __name__ == '__main__':
    keras.backend.clear_session()

    # Read config file
    args = io_utils.handle_args()
    # print('Config file:', args.config_file)
    config = importlib.import_module('config_files.' + args.config_file)
    cfg = config.ConfigIitTest()

    # import backbone
    if cfg.BACKBONE == "mobilenet_v2":
        from models.rpn_mobilenet_v2 import get_model as get_rpn_model
    else:
        from models.rpn_vgg16 import get_model as get_rpn_model

    imdb, roidb = data_utils.combined_roidb(
        cfg.IMDB_NAME, cfg.PROPOSAL_METHOD, cfg.USE_FLIPPED, mode="inference")
    labels = imdb.classes
    print(labels)
    base_anchors = bbox_utils.generate_base_anchors(cfg)

    # Create models and load weights
    rpn_model, feature_extractor = get_rpn_model(cfg)
    frcnn_model = affordancenet.get_affordance_net_model(
        feature_extractor, rpn_model, cfg, base_anchors, mode="inference")
    status = frcnn_model.load_weights(cfg.WEIGHTS_FILE, by_name=True)

    # import dummy data for visualization
    # out_types = data_utils.get_data_types()
    # test_data = tf.data.Dataset.from_generator(iit_data_to_tf_dataset, output_types=out_types)
    # test_data = test_data.map(load_imgs_and_masks, num_parallel_calls=6)
    # data_shapes = data_utils.get_data_shapes(cfg.MASK_REG)
    # padding_values = data_utils.get_padding_values(cfg.MASK_REG)
    # test_data = test_data.padded_batch(cfg.BATCH_SIZE, padded_shapes=data_shapes, padding_values=padding_values, drop_remainder=True)
    # test_feed = train_utils.iit_generator_inference_no_resize(test_data, cfg)
    # 
    # image_data = test_feed[0]
    # img_daf, image_shape, true_bboxes, true_labels, true_masks, mask_ids = image_data

    # TODO: load image
    # img = tf.keras.preprocessing.image.load_img("./imgs/TestImage_00976.png")
    # print(img)

    img_mask_check = tf.io.read_file("../data/cache/GTsegmask_VOC_2012_train_images/3736_1_segmask.png")
    tensor_img_mask = tf.io.decode_image(img_mask_check, channels=3, dtype=tf.dtypes.float32)
    np.set_printoptions(threshold=sys.maxsize) 

    filenames = next(walk("./testRobotImages"), (None, None, []))[2]  # [] if no file
    
    for filename in filenames:
        img = tf.io.read_file("./testRobotImages/"+filename)

# convert to tensor (specify 3 channels explicitly since png files contains additional alpha channel)
# set the dtypes to align with pytorch for comparison since it will use uint8 by default
        tensor = tf.io.decode_image(img, channels=3, dtype=tf.dtypes.float32)
# (384, 470, 3)

# resize tensor to 224 x 224
# (224, 224, 3)

# add another dimension at the front to get NHWC shape
        img = tf.expand_dims(tensor, axis=0)
# (1, 224, 224, 3)


        pred_bboxes, pred_labels, pred_scores, pred_masks = frcnn_model.predict([img], verbose=1)

        img = tf.squeeze(img, axis=0)
        pred_bboxes = tf.squeeze(pred_bboxes, axis=0)
        pred_labels = tf.squeeze(pred_labels, axis=0)
        pred_scores = tf.squeeze(pred_scores, axis=0)

        pred_masks = tf.squeeze(pred_masks, axis=0)
        
        print("after squeezing ready to visualize")
        drawing_utils.draw_predictions_with_masks(img, pred_bboxes, pred_labels, pred_scores,
                                       labels, cfg.BATCH_SIZE, cfg.MASK_REG, pred_masks, cfg.AFFORDANCE_LABELS, 'iit')
