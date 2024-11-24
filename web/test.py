from moviepy import VideoFileClip
from PIL import Image
import numpy as np
import os
import sys
sys.path.append(os.getcwd())
from web.unet_model import UNetModel
from web.image2svg import image_to_svg

clip = VideoFileClip('web\static\807427488-1-208.mp4')
def get_frame_by_time(time_in_seconds):
# 获取指定时间点的帧 (返回的是一个 NumPy 数组)
    frame = clip.get_frame(time_in_seconds)  
    return frame

def numpy_to_pil(frame):
    """
    将视频帧（NumPy 数组格式）转换为 PIL 图像格式
    """
    # 检查输入类型是否为 NumPy 数组
    if not isinstance(frame, np.ndarray):
        raise TypeError("frame 必须是 NumPy 数组格式")
    
    # OpenCV 使用 BGR 格式，而 PIL 使用 RGB 格式，需要转换颜色通道
    frame_rgb = frame[:, :, ::-1]  # BGR 转 RGB
    
    # 将 NumPy 数组转换为 PIL 图像
    pil_image = Image.fromarray(frame_rgb)
    return pil_image

unet_model = UNetModel()
unet = unet_model.get_net()
times = int(clip.duration)
for time in range(times):
    frame = get_frame_by_time(time)
    frame = numpy_to_pil(frame)

    r_image = unet.detect_image(frame, name_classes=2)
    
    r_image.save(f'./web/static/mask_image_{time+1}.png')
    image_to_svg(f'./web/static/mask_image_{time+1}.png',f"./web/static/mask_image_{time+1}.svg")