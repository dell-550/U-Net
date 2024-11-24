import numpy as np


def calculate_metrics(y_true, y_pred):
    """
    计算语义分割任务的 Accuracy、IoU 和 Dice 系数。

    参数:
    y_true (np.ndarray): 真实标签的二值图像 (0 或 1)。
    y_pred (np.ndarray): 模型预测的二值图像 (0 或 1)。

    返回:
    dict: 包含 Accuracy, IoU, 和 Dice 系数的字典。
    """
    # 确保输入为 NumPy 数组
    y_true = np.asarray(y_true).astype(np.bool_)
    y_pred = np.asarray(y_pred).astype(np.bool_)

    # 计算 True Positive (TP), False Positive (FP), False Negative (FN), True Negative (TN)
    TP = np.sum(y_true & ~y_pred)  # 正确预测为前景的像素数
    FP = np.sum(~y_true & ~y_pred)  # 错误预测为前景的像素数
    FN = np.sum(y_true & y_pred)  # 错误预测为背景的像素数
    TN = np.sum(~y_true & y_pred)  # 正确预测为背景的像素数

    # Accuracy
    accuracy = (TP + TN) / (TP + FP + FN + TN + 1e-6)  # 加1e-6避免除零

    # IoU
    iou = TP / (TP + FP + FN + 1e-6)

    # Dice Coefficient
    dice = 2 * TP / (2 * TP + FP + FN + 1e-6)

    return {
        "Accuracy": accuracy,
        "IoU": iou,
        "Dice": dice
    }


# 示例用法
if __name__ == "__main__":
    # 示例真实标签 (y_true) 和预测结果 (y_pred)
    y_true = np.array([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]])
    y_pred = np.array([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]])

    metrics = calculate_metrics(y_true, y_pred)
    print(metrics)
