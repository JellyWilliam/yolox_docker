import argparse
import av
import numpy as np
import cv2

from my_yolox import main, get_exp_by_name

exp = get_exp_by_name("yolox_nano")


def save_frame(video_path: str, fps_out_video=25, frame_size_out_video=(1920, 1080)):
    """
    Функция использования YOLOX для видео

    :param video_path: путь до файла
    :param fps_out_video: количество кадров в секунду в видео
    :param frame_size_out_video: размер кадра для выходного видео

    :return: сохранённое видео в формате "(video_name)_YOLOX.(video_extension)"
    """
    container = av.open(video_path)
    video_arr = video_path.split("/")[-1].split(".")
    video_name = ".".join(video_arr[:-1])
    video_extension = video_arr[-1]
    out = cv2.VideoWriter(f'{video_name}_YOLOX.{video_extension}', cv2.VideoWriter_fourcc(*"mp4v"), fps_out_video, frame_size_out_video)

    for frame in container.decode(video=0):
        open_cv_image = np.array(frame.to_image())
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        image = main(exp=exp, image=open_cv_image, name_frame=f'frame_{frame.index}.jpg', save_frame=False)
        out.write(image)

    out.release()

    print("Успешно завершено")


parser = argparse.ArgumentParser()
parser.add_argument("--video", default="develop_streem.ts")
parser.add_argument("--fps", default="25")
parser.add_argument("--frame_size", default="1920,1080")
args = parser.parse_args()
video = args.video
fps = int(args.fps)
frame_size = args.frame_size
frame_size = tuple(map(int, frame_size.split(",")))

save_frame(video_path=video, fps_out_video=fps, frame_size_out_video=frame_size)
