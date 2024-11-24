import matplotlib.pyplot as plt


def save_original_and_prediction(original_image, predicted_image, save_path = r"D:\Downloads",
                                 original_title="Origin", predicted_title="Predicted", cmap=None):
    """
    显示并保存原图和预测图。

    参数:
        original_image: ndarray
            原始图像数据。
        predicted_image: ndarray
            预测图像数据。
        save_path: str
            图像保存的路径（包括文件名和扩展名，例如 'output.png'）。
        original_title: str, 可选
            原图的标题，默认值为 "Original Image"。
        predicted_title: str, 可选
            预测图的标题，默认值为 "Predicted Image"。
        cmap: str, 可选
            用于显示图像的颜色映射，默认为 None（彩色图像）。
    """
    name = original_image.filename.rsplit('\\',1)

    original_image.save(r"D:\python_project\unet_course\test_image\image\\" + name[-1])
    predicted_image.save(r"D:\python_project\unet_course\test_image\test_pred\\" + name[-1])
    # plt.figure(figsize=(10, 5))
    #
    # # 显示原图
    # plt.subplot(1, 2, 1)  # 1 行 2 列，第 1 个
    # plt.imshow(original_image)
    # plt.title("Original Image")
    # plt.axis("off")  # 隐藏坐标轴
    #
    # # 显示预测图
    # plt.subplot(1, 2, 2)  # 1 行 2 列，第 2 个
    # plt.imshow(predicted_image, cmap="gray")  # 使用颜色映射
    # plt.title("Predicted Image")
    # plt.axis("off")  # 隐藏坐标轴
    #
    # # 调整布局并显示
    # plt.tight_layout()
    # plt.savefig('./out.png')

