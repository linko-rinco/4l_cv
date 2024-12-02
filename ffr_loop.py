from ImageClicker import ImageMatcher,ImageClicker,load_hand_stop_and_continue_pos # type: ignore
import time
import pyautogui
hands_region,stop_pos,continue_pos=load_hand_stop_and_continue_pos()

# ffr_hime=ImageClicker(r"picture\ffr_hime.png",retry_count=1,retry_interval=0.01,
#                       match_threshold=0.6,region=hands_region,click=8,
#                       stop=True,stop_pos=stop_pos,continue_pos=continue_pos
#                       )
# ffr_megu=ImageClicker(r"picture\ffr_megu.png",retry_count=1,retry_interval=0.01,retry_count=1,retry_interval=0.01,
#                       match_threshold=0.6,region=hands_region,click=4,
#                       stop=True,stop_pos=stop_pos,continue_pos=continue_pos
#                       )
# ffr_hime_unfire=ImageClicker(r"picture\ffr_hime_unfire.png",retry_count=1,retry_interval=0.01,retry_count=1,retry_interval=0.01,
#                       match_threshold=0.6,region=hands_region,
#                       stop=True,stop_pos=stop_pos,continue_pos=continue_pos
#                       )
# ffr_megu_unfire=ImageClicker(r"picture\ffr_megu_unfire.png",retry_count=1,retry_interval=0.01,retry_count=1,retry_interval=0.01,
#                       match_threshold=0.6,region=hands_region,
#                       stop=True,stop_pos=stop_pos,continue_pos=continue_pos
#                       )
# zzl=ImageClicker(r"picture\zzl.png",retry_count=1,retry_interval=0.01,retry_count=1,retry_interval=0.01,
#                       match_threshold=0.6,region=hands_region,
#                       stop=True,stop_pos=stop_pos,continue_pos=continue_pos
#                       )

ffr_hime=ImageMatcher(target_image_path=r"picture\ffr_hime.png",
                      stop=True,stop_pos=stop_pos
                      )
ffr_megu=ImageMatcher(target_image_path=r"picture\ffr_megu.png",
                      stop=True,stop_pos=stop_pos
                      )
# zzl=ImageMatcher(target_image_path=r"picture\zzl.png",
#                  stop=True,stop_pos=stop_pos
#                 )

time.sleep(10)
pyautogui.click(continue_pos[0],continue_pos[1])

ffr_hime_pos=ffr_hime.macth()
ffr_hime_pos=(int(ffr_hime_pos[1][0]),int((ffr_hime_pos[0][1]+ffr_hime_pos[1][1])/2))
pyautogui.click(continue_pos[0],continue_pos[1])
for i in range(8):
  pyautogui.click(ffr_hime_pos[0],ffr_hime_pos[1])
  time.sleep(0.072)

ffr_megu_pos=ffr_megu.macth()
ffr_megu_pos=(int(ffr_megu_pos[1][0]),int((ffr_megu_pos[0][1]+ffr_megu_pos[1][1])/2))
pyautogui.click(continue_pos[0],continue_pos[1])
for i in range(4):
  pyautogui.click(ffr_megu_pos[0],ffr_megu_pos[1])
  time.sleep(0.072)

for j in range(10):
  for i in range(8):
    pyautogui.click(ffr_hime_pos[0],ffr_hime_pos[1])
    time.sleep(0.072)
  for i in range(4):
    pyautogui.click(ffr_megu_pos[0],ffr_megu_pos[1])
    time.sleep(0.072)
pyautogui.click(stop_pos[0],stop_pos[1])