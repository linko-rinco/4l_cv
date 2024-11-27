from ImageClicker import ImageClicker # type: ignore

yh_megumi=ImageClicker(r"picture\yh_megumi.png",retry_count=1,retry_interval=0.01,match_threshold=0.6)
hime=ImageClicker(r"picture\hime.png",retry_count=1,retry_interval=0.01,match_threshold=0.6)
k7m7=ImageClicker(r"picture\k7m7.png",retry_count=1,retry_interval=0.01,match_threshold=0.6,click=4)
syk=ImageClicker(r"picture\syk.png",retry_count=1,retry_interval=0.01,match_threshold=0.6)

def after_megumi():
    if hime.click_image():
        return
    else:
        k7m7.click_image()

def after_hime():
    if yh_megumi.click_image():
        return
    else:
        k7m7.click_image()

while True:
    if yh_megumi.click_image():
        after_megumi()
    else:
        after_hime()

# while True:
#     if yh_megumi.click_image():
#         after_megumi()
#     else:
#         after_hime()
        
