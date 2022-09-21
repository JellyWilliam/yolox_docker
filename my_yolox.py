import importlib
import os

import cv2
import torch

from yolox.data.data_augment import ValTransform
from yolox.data.datasets import COCO_CLASSES
from yolox.utils import postprocess, vis

IMAGE_EXT = [".jpg", ".jpeg", ".webp", ".bmp", ".png"]


def get_exp_by_name(exp_name):
    exp = exp_name.replace("-", "_")
    module_name = ".".join(["yolox", "exp", "default", exp])
    exp_object = importlib.import_module(module_name).Exp()
    return exp_object


class Predictor(object):
    def __init__(self, model, exp, cls_names=COCO_CLASSES, device="cpu"):
        self.model = model
        self.cls_names = cls_names
        self.num_classes = exp.num_classes
        self.confthre = exp.test_conf
        self.nmsthre = exp.nmsthre
        self.test_size = exp.test_size
        self.device = device
        self.preproc = ValTransform(legacy=False)

    def inference(self, img, name_frame):
        img_info = {"id": 0}
        if isinstance(img, str):
            img_info["file_name"] = os.path.basename(name_frame)
        else:
            img_info["file_name"] = None

        height, width = img.shape[:2]
        img_info["height"] = height
        img_info["width"] = width
        img_info["raw_img"] = img

        ratio = min(self.test_size[0] / img.shape[0], self.test_size[1] / img.shape[1])
        img_info["ratio"] = ratio

        img, _ = self.preproc(img, None, self.test_size)
        img = torch.from_numpy(img).unsqueeze(0)
        img = img.float()

        with torch.no_grad():
            outputs = self.model(img)
            outputs = postprocess(outputs, self.num_classes, self.confthre, self.nmsthre, class_agnostic=True)
        return outputs, img_info

    def visual(self, output, img_info, cls_conf=0.35):
        ratio = img_info["ratio"]
        img = img_info["raw_img"]

        output = output.cpu()

        bboxes = output[:, 0:4]
        bboxes /= ratio

        cls = output[:, 6]
        scores = output[:, 4] * output[:, 5]

        vis_res = vis(img, bboxes, scores, cls, cls_conf, self.cls_names)
        return vis_res


def image_demo(predictor, vis_folder, image, path, save_frame):
    outputs, img_info = predictor.inference(image, path)
    result_image = predictor.visual(outputs[0], img_info, predictor.confthre)
    if save_frame:
        os.makedirs(vis_folder, exist_ok=True)
        save_file_name = os.path.join(vis_folder, os.path.basename(path))
        cv2.imwrite(save_file_name, result_image)
        return None
    else:
        return result_image


def main(exp, image, name_frame, save_frame=True, conf=.25, nms=.45, tsize=640, ckpt="YOLOX/models/yolox_nano.pth"):
    vis_folder = os.path.join("MY_YOLOX_OUT")
    if save_frame:
        os.makedirs(vis_folder, exist_ok=True)

    exp.test_conf = conf
    exp.nmsthre = nms
    exp.test_size = (tsize, tsize)

    model = exp.get_model()
    model.eval()

    ckpt_file = ckpt
    ckpt = torch.load(ckpt_file, map_location="cpu")
    model.load_state_dict(ckpt["model"])

    predictor = Predictor(
        model, exp, COCO_CLASSES
    )

    image_yolox = image_demo(predictor, vis_folder, image, name_frame, save_frame)
    return image_yolox
