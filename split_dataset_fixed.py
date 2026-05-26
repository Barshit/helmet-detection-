import os, random, shutil

IMG_DIR = "images"
LBL_DIR = "labels"

TRAIN_IMG = "train/images"
TRAIN_LBL = "train/labels"
VAL_IMG = "val/images"
VAL_LBL = "val/labels"

for folder in [TRAIN_IMG, TRAIN_LBL, VAL_IMG, VAL_LBL]:
    os.makedirs(folder, exist_ok=True)

images = [f for f in os.listdir(IMG_DIR) if f.lower().endswith((".jpg",".png",".jpeg"))]
images.sort()
random.seed(42)
random.shuffle(images)

split_ratio = 0.8
train_count = int(len(images) * split_ratio)

train_files = images[:train_count]
val_files = images[train_count:]

def copy_list(files, img_out, lbl_out):
    for img in files:
        lbl = os.path.splitext(img)[0] + ".txt"
        shutil.copy(os.path.join(IMG_DIR, img), os.path.join(img_out, img))
        shutil.copy(os.path.join(LBL_DIR, lbl), os.path.join(lbl_out, lbl))

copy_list(train_files, TRAIN_IMG, TRAIN_LBL)
copy_list(val_files, VAL_IMG, VAL_LBL)

print("Split complete. Train images:", len(train_files), "Val images:", len(val_files))
