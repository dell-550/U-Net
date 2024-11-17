import io
import os
import time

import sys
sys.path.append("..")
print(sys.path)
from PIL import Image
from flask import Flask, request, render_template

from web.unet_model import UNetModel

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
    return render_template('home.html')


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
            image_path = os.path.join(r'D:\python_project\unet-pytorch\web\static\predict', image.filename)
            end_time = time.time()
            r_image.save(image_path)
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

