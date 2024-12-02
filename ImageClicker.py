import cv2
import numpy as np
import pyautogui
import time

sift=cv2.SIFT_create()

class ImageMatcher:
    def __init__(self,target_image_path=None,target_image=None,kp=None,des=None,region=(0,0,2560,1440),stop_pos=(1602,129),stop=True):
        self.region=region
        self.stop=stop
        if self.stop:
            self.stop_pos=stop_pos
            
        if target_image_path!=None:
            self.target_image = cv2.imread(target_image_path).astype("uint8")
        else:
            self.target_image=target_image
        if kp!=None:
            self.kp,self.des=kp,des
        self.kp,self.des=sift.detectAndCompute(self.target_image,None)

    def macth(self,match_threshold=0.75):
        # 获取浏览器窗口截图
        screenshot = pyautogui.screenshot(region=self.region)
        if self.stop:
            pyautogui.click(self.stop_pos[0],self.stop_pos[1])
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
 
        # 提取截图的 SIFT 特征
        kp, des = sift.detectAndCompute(screenshot, None)
 
        # 进行特征匹配
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(self.des, des, k=2)

        # 使用 Lowe's Ratio Test 筛选匹配结果
        good = []
        for m, n in matches:
            if m.distance < match_threshold * n.distance:  # 使用 match_threshold 阈值
                good.append([m])
 
        # 计算目标元素的位置
        if len(good) > 0:
            src_pts = np.float32([self.kp[m[0].queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp[m[0].trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            h, w = self.target_image.shape[:2]
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            # print(dst[0],dst[1],dst[2],dst[3])
            # 0 3
            # 1 2
            return (float(dst[0][0][0]),float(dst[0][0][1])),(float(dst[2][0][0]),float(dst[2][0][1]))
        return False

def get_hand_stop_and_continue_pos():
    time.sleep(10)
    cards=ImageMatcher(target_image_path=r"picture\cards.png",stop=False)
    stop=ImageMatcher(target_image_path=r"picture\stop.png",stop=False)

    cards_pos=cards.macth(match_threshold=0.95)
    stop_pos=stop.macth(match_threshold=0.95)

    hand_pos=(cards_pos[0][0],cards_pos[1][1])
    hand_hight,hand_width=stop_pos[1][0]-hand_pos[0],1440-hand_pos[1]
    stop_pos=(int((stop_pos[0][0]+stop_pos[1][0])/2),int((stop_pos[0][1]+stop_pos[1][1])/2))

    pyautogui.click(stop_pos[0],stop_pos[1])
    continue_=ImageMatcher(target_image_path=r"picture\continue.png",stop=False)
    continue_pos=continue_.macth(match_threshold=0.95)
    continue_pos=(int((continue_pos[0][0]+continue_pos[1][0])/2),int((continue_pos[0][1]+continue_pos[1][1])/2))
    pyautogui.click(continue_pos[0],continue_pos[1])
    with open(r"data\positons.txt","w",encoding="utf8") as f:
        f.write(f"{hand_pos[0]} {hand_pos[1]}\n")
        f.write(f"{hand_hight} {hand_width}\n")
        f.write(f"{stop_pos[0]} {stop_pos[1]}\n")
        f.write(f"{continue_pos[0]} {continue_pos[1]}\n")

    return hand_pos,(hand_hight,hand_width),stop_pos,continue_pos

def load_hand_stop_and_continue_pos():
    with open(r"data\positons.txt","r",encoding="utf8") as f:
        lines=f.read().split("\n")
        hands_region=[int(float(i)) for i in lines[0].split()]
        hands_region+=[int(float(i)) for i in lines[1].split()]
        stop_pos=[int(i) for i in lines[2].split()]
        continue_pos=[int(i) for i in lines[3].split()]
    return tuple(hands_region),tuple(stop_pos),tuple(continue_pos)


class ImageClicker:
    def __init__(self, target_image_path, retry_count=3, retry_interval=1, match_threshold=0.75,
                 click=2,region=(0,0,2560,1440),stop_pos=None,continue_pos=(1279,949),stop=False
                 ):
        self.target_image_path = target_image_path
        self.retry_count = retry_count
        self.retry_interval = retry_interval
        self.match_threshold = match_threshold
        self.click=click
        self.stop=stop
        if self.stop:
            self.continue_pos=continue_pos
 
        # 加载目标图片
        self.target_image = cv2.imread(self.target_image_path).astype("uint8")
 
        # 提取目标图片的 SIFT 特征
        self.sift = cv2.SIFT_create()
        self.kp, self.des = self.sift.detectAndCompute(self.target_image, None)

        # 建立图片匹配对象
        self.matcher=ImageMatcher(target_image=self.target_image,kp=self.kp,des=self.des,
                                  match_threshold=match_threshold,
                                  region=region,stop=stop,stop_pos=stop_pos
                                  )
 
    def click_image(self):
        for i in range(self.retry_count):
            try:
                dst=self.matcher.macth()
                if dst:
                    # 计算点击坐标
                    x = int((dst[0][0]+dst[1][0])/2)  # 计算水平方向的中间位置
                    y = int((dst[0][1]+dst[1][1])/2)  # 计算垂直方向的中间位置
 
                    # 点击目标元素
                    if self.stop:
                        pyautogui.click(self.continue_pos[0],self.continue_pos[1])
                for i in range(self.click):
                    pyautogui.click(x,y)
                    time.sleep(0.08)
                return True  # 点击成功
 
            except Exception as e:
                print(f"点击失败：{e}")
                time.sleep(self.retry_interval)
 
        return False  # 点击失败

if __name__ == "__main__": 
    # hands_region,stop_pos,continue_pos=load_hand_stop_and_continue_pos()

    # image_clicker = ImageClicker(r"test.png",
    #                              retry_count=10,
    #                             retry_interval=0.1,
    #                             match_threshold=0.8,
    #                             click=2,
    #                             region=hands_region,
    #                             stop=True,
    #                             stop_pos=stop_pos,
    #                             continue_pos=continue_pos
    #                             )
    # if image_clicker.click_image():
    #     print("点击成功！")
    # else:
    #     print("点击失败！")

    # image_matcher=ImageMatcher(target_image_path=r"test.png")
    # pos=image_matcher.macth()
    # print(pos)

    pos=get_hand_stop_and_continue_pos()
    print(pos)