import cairosvg
import cv2
import numpy as np
import svgwrite

def image_to_svg(image_path, output_svg_path):
    # Step 1: 加载图片并二值化
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)

    # Step 2: 轮廓检测
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 3: 创建 SVG 文件
    height, width = binary.shape
    dwg = svgwrite.Drawing(output_svg_path, profile='tiny', size=(f"{width}px", f"{height}px"))
    dwg.viewbox(0, 0, width, height)

    # Step 4: 将轮廓信息转换为路径数据
    for contour in contours:
        path_data = "M" + " ".join(f"{x},{y}" for x, y in contour.squeeze(axis=1))
        path_data += " Z"  # 闭合路径
        dwg.add(dwg.path(d=path_data, fill="black", stroke="none"))

    # Step 5: 保存 SVG 文件
    dwg.save()
    print(f"SVG file saved to {output_svg_path}")
    cairosvg.svg2png(url='output_image.svg', write_to='output_image.png')

# 示例用法
image_path = r'D:\python_project\unet_course\web\static\mask_image_1.png'
output_svg_path = "output_image.svg"  # 输出 SVG 文件路径
image_to_svg(image_path, output_svg_path)

    # image_to_svg(r'D:\python_project\unet_course\web\static\predict\image2.png', 'output.svg', cfg)