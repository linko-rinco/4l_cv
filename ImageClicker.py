import cv2
import numpy as np
import pyautogui
import time
 
class ImageClicker:
    def __init__(self, target_image_path, retry_count=3, retry_interval=1, match_threshold=0.75,click=2):
        self.target_image_path = target_image_path
        self.retry_count = retry_count
        self.retry_interval = retry_interval
        self.match_threshold = match_threshold
        self.click=click
 
        # 加载目标图片
        self.target_image = cv2.imread(self.target_image_path).astype("uint8")
 
        # 提取目标图片的 SIFT 特征
        self.sift = cv2.SIFT_create()
        self.kp1, self.des1 = self.sift.detectAndCompute(self.target_image, None)
 
    def click_image(self):
        for i in range(self.retry_count):
            try:
                # 获取浏览器窗口截图
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
 
                # 提取截图的 SIFT 特征
                kp2, des2 = self.sift.detectAndCompute(screenshot, None)
 
                # 进行特征匹配
                bf = cv2.BFMatcher()
                matches = bf.knnMatch(self.des1, des2, k=2)
 
                # 使用 Lowe's Ratio Test 筛选匹配结果
                good = []
                for m, n in matches:
                    if m.distance < self.match_threshold * n.distance:  # 使用 match_threshold 阈值
                        good.append([m])
 
                # 计算目标元素的位置
                if len(good) > 0:
                    src_pts = np.float32([self.kp1[m[0].queryIdx].pt for m in good]).reshape(-1, 1, 2)
                    dst_pts = np.float32([kp2[m[0].trainIdx].pt for m in good]).reshape(-1, 1, 2)
                    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                    h, w = self.target_image.shape[:2]
                    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                    dst = cv2.perspectiveTransform(pts, M)
 
                    # 计算点击坐标
                    # x = int((dst[0][0][0] + dst[2][0][0]) / 2)  # 计算水平方向的中间位置
                    x = dst[2][0][0]
                    y = int((dst[0][0][1] + dst[2][0][1]) / 2)  # 计算垂直方向的中间位置
 
                    # 点击目标元素
                    for i in range(self.click):
                        pyautogui.click(x,y)
                        time.sleep(0.08)
                    return True  # 点击成功
 
            except Exception as e:
                print(f"点击失败：{e}")
                time.sleep(self.retry_interval)
 
        return False  # 点击失败

if __name__ == "__main__": 
    # 使用示例
    image_clicker = ImageClicker("test.png", retry_count=10,
                                retry_interval=0.1,
                                match_threshold=0.8,click=3)  # 设置 match_threshold 为 0.8
    if image_clicker.click_image():
        print("点击成功！")
    else:
        print("点击失败！")