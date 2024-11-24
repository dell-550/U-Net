import io
import os
import time
import cv2
import sys

# from utils.save_picture import save_original_and_prediction

product_path = os.getcwd()
sys.path.append(product_path)
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from flask import Flask, request, render_template
import json
from web.unet_model import UNetModel
from moviepy import VideoFileClip

app = Flask(__name__, template_folder='templates', static_folder='static')



@app.route('/')
def video():
    return render_template('home.html')
@app.route('/test')
def test():
    return render_template('test.html')
@app.route('/video')
def index():
    return render_template('video.html')

@app.route('/mask-image', methods=['POST'])
def mask_image():
    data = request.data
    data = json.loads(data)
    time = data.get('time')
    fps  =  data.get('fps')
    fps = request.args.get('fps', type=int)

    # clip = VideoFileClip('web\static\807427488-1-208.mp4')
    # def get_frame_by_time(time_in_seconds):
    # # 获取指定时间点的帧 (返回的是一个 NumPy 数组)
    #     frame = clip.get_frame(time_in_seconds)  
    #     return frame
    
    # frame = get_frame_by_time(time)


    
    # unet_model = UNetModel()
    # unet = unet_model.get_net()
    # r_image = unet.detect_image(frame, name_classes=2)
    
    # r_image.save(f'./static/mask_image_{time}.png')
    data = {
            "path":f'./static/mask_image_{time}.svg'
        }
    return {"data": data,"message":"success","status": 200}


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            print(image.filename)

            image_bytes = image.read()
            # 使用 BytesIO 将字节数据转换为文件对象，再打开图片
            image_stream = io.BytesIO(image_bytes)
            images = Image.open(image_stream)

            unet_model = UNetModel()
            unet = unet_model.get_net()

            start_time = time.time()
            # images = Image.open(r'D:\python_project\unet-pytorch\web\static\OIP.jpg')
            r_image = unet.detect_image(images, name_classes=2)
            image_path = os.path.join(r'D:\python_project\unet_course\web\static\predict', image.filename)
            end_time = time.time()
            r_image.save(image_path)
            # save_original_and_prediction(images,r_image)
            data = {
                "path":'static\predict\\'+image.filename,
                "model_name" : "U-Net",
                "deal_type" : "语义分割",
                "image_size" : images.size,
                "times" : f"{end_time-start_time:.2f}s",
                "model_path" : unet.model_path,
            }
            return {"data": data,"message":"success","status": 200}


if __name__ == '__main__':
    app.run()

