#----------------------------------------------------#
#   将单张图片预测、摄像头检测和FPS测试功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
#----------------------------------------------------#
import time

import cv2
import numpy as np
from PIL import Image

from unet import Unet_ONNX, Unet
from utils.save_picture import save_original_and_prediction

if __name__ == "__main__":
    #-------------------------------------------------------------------------#
    #   如果想要修改对应种类的颜色，到__init__函数里修改self.colors即可
    #-------------------------------------------------------------------------#
    #----------------------------------------------------------------------------------------------------------#
    #   mode用于指定测试的模式：
    #   'predict'           表示单张图片预测，如果想对预测过程进行修改，如保存图片，截取对象等，可以先看下方详细的注释
    #   'video'             表示视频检测，可调用摄像头或者视频进行检测，详情查看下方注释。
    #   'fps'               表示测试fps，使用的图片是img里面的street.jpg，详情查看下方注释。
    #   'dir_predict'       表示遍历文件夹进行检测并保存。默认遍历img文件夹，保存img_out文件夹，详情查看下方注释。
    #   'export_onnx'       表示将模型导出为onnx，需要pytorch1.7.1以上。
    #   'predict_onnx'      表示利用导出的onnx模型进行预测，相关参数的修改在unet.py_346行左右处的Unet_ONNX
    #----------------------------------------------------------------------------------------------------------#
    mode = "predict"
    #-------------------------------------------------------------------------#
    #   count               指定了是否进行目标的像素点计数（即面积）与比例计算
    #   name_classes        区分的种类，和json_to_dataset里面的一样，用于打印种类和数量
    #
    #   count、name_classes仅在mode='predict'时有效
    #-------------------------------------------------------------------------#
    count           = False
    # name_classes    = ["background","aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    name_classes    = ["background","person"]
    #----------------------------------------------------------------------------------------------------------#
    #   video_path          用于指定视频的路径，当video_path=0时表示检测摄像头
    #                       想要检测视频，则设置如video_path = "xxx.mp4"即可，代表读取出根目录下的xxx.mp4文件。
    #   video_save_path     表示视频保存的路径，当video_save_path=""时表示不保存
    #                       想要保存视频，则设置如video_save_path = "yyy.mp4"即可，代表保存为根目录下的yyy.mp4文件。
    #   video_fps           用于保存的视频的fps
    #
    #   video_path、video_save_path和video_fps仅在mode='video'时有效
    #   保存视频时需要ctrl+c退出或者运行到最后一帧才会完成完整的保存步骤。
    #----------------------------------------------------------------------------------------------------------#
    video_path      = r"D:\Downloads\1602778235-1-16.mp4"
    video_save_path = r"D:\python_project\unet-pytorch\logs\last_epoch_weights.pth"
    video_fps       = 25.0
    #----------------------------------------------------------------------------------------------------------#
    #   test_interval       用于指定测量fps的时候，图片检测的次数。理论上test_interval越大，fps越准确。
    #   fps_image_path      用于指定测试的fps图片
    #   
    #   test_interval和fps_image_path仅在mode='fps'有效
    #----------------------------------------------------------------------------------------------------------#
    test_interval = 100
    fps_image_path  = r"D:\python_project\unet-pytorch\VOCdevkit\VOC2007\JPEGImages\2007_000648.jpg"
    #-------------------------------------------------------------------------#
    #   dir_origin_path     指定了用于检测的图片的文件夹路径
    #   dir_save_path       指定了检测完图片的保存路径
    #   
    #   dir_origin_path和dir_save_path仅在mode='dir_predict'时有效
    #-------------------------------------------------------------------------#
    dir_origin_path = "img/"
    dir_save_path   = "img_out/"
    #-------------------------------------------------------------------------#
    #   simplify            使用Simplify onnx
    #   onnx_save_path      指定了onnx的保存路径
    #-------------------------------------------------------------------------#
    simplify        = True
    onnx_save_path  = "model_data/models.onnx"

    if mode != "predict_onnx":
        unet = Unet()
    else:
        unet = Unet_ONNX()

    if mode == "predict":

        import pandas
        from utils.save_metrics import save_params
        from utils.get_acc_iou_dice import calculate_metrics
        # unet._defaults.update({"mix_type": 1})

        # img = input('Input image filename:')
        # with open(r"D:\python_project\unet-pytorch\mnt\d\data\koto\valid_list.txt", "r") as f:
        #     train_lines = f.readlines()
        # len = len(train_lines)
        # acc_sum, iou_sum, dice_sum = 0, 0, 0
        # acc_max, iou_max, dice_max = 0,0,0
        # acc_min, iou_min, dice_min = float("inf"), float("inf"), float("inf")
        import glob

        image_path = r"D:\python_project\unet_course\test_image\test"
        train_lines = glob.glob(f"{image_path}/*")
        # num_train = len(train_lines)

        for lines_list in train_lines:
            img = lines_list
            # img, png = lines_list.strip().split(" ")
            # img = r'D:\python_project\unet-pytorch\\' + img.replace('/','\\')
            # png = r'D:\python_project\unet-pytorch\\' + png.replace('/','\\')
            try:
                image = Image.open(img)
                # label = Image.open(png)
                # label = label.convert("L")
                # calculate_metrics()
            except Exception as e:
                print('Open Error! Try again!', e)
                continue
            else:
                r_image = unet.detect_image(image, count=count, name_classes=name_classes)
                r_image = r_image.convert("L")
                r_image = r_image.point(lambda p: 255 if p else 0)
                r_image = r_image.point(lambda p: 255 - p)
                save_original_and_prediction(image, r_image)
        #         result = calculate_metrics(np.array(r_image), np.array(label))
        #         acc,iou,dice = result["Accuracy"],result["IoU"],result["Dice"]
        #         acc_sum += acc
        #         iou_sum += iou
        #         dice_sum += dice
        #         save_params(acc, iou, dice)
        #         acc_max = max(acc_max, acc)
        #         iou_max = max(iou_max, iou)
        #         dice_max = max(dice_max, dice)
        #         acc_min = min(acc_min, acc)
        #         iou_min = min(iou_min, iou)
        #         dice_min = min(dice_min, dice)
        #
        # print("acc_sum{:.3f} iou_sum{:.3f} dice_sum{:.3f}".format(acc_sum/len, iou_sum/len, dice_sum/len))
        # print("acc_max{:.3f} iou_max{:.3f} dice_max{:.3f}".format(acc_max,iou_max,dice_max))
        # print("acc_min{:.3f} iou_min{:.3f} dice_min{:.3f}".format(acc_min,iou_min,dice_min))
                # r_image.show()


 