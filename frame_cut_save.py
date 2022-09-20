import argparse
import av


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
            frame.to_image().save(f'frame_{frame.index}.jpg')

    print("Успешно завершено")


parser = argparse.ArgumentParser()
parser.add_argument("--frames", default="100,200,224")
parser.add_argument("--i", default="develop_streem.ts")
args = parser.parse_args()
frames = args.frames
frames = result = list(map(int, frames.split(",")))
video = args.i

save_frame(video_path=video, list_frame=frames)
