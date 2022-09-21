import argparse
import av
import numpy as np

from my_yolox import main, get_exp_by_name

exp = get_exp_by_name("yolox_nano")


def save_frame(video_path: str, list_frame: list):
    """
    Функция сохранения определённых кадров из видео

    :param video_path: путь до файла
    :param list_frame: кадры, которые надо сохранить
    :return: сохранённые кадры в формате "frame_(frame.index).jpg"
    """
    container = av.open(video_path)

    for frame in container.decode(video=0):
        if frame.index in list_frame:
            open_cv_image = np.array(frame.to_image())
            open_cv_image = open_cv_image[:, :, ::-1].copy()
            main(exp=exp, image=open_cv_image, name_frame=f'frame_{frame.index}.jpg')

    print("Успешно завершено")


parser = argparse.ArgumentParser()
parser.add_argument("--frames", default="100,200,224")
parser.add_argument("--i", default="develop_streem.ts")
args = parser.parse_args()
frames = args.frames
frames = result = list(map(int, frames.split(",")))
video = args.i

save_frame(video_path=video, list_frame=frames)
