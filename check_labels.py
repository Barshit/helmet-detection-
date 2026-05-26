# check_labels.py
import os

def count(folder):
    img_dir = os.path.join(folder, "images")
    lbl_dir = os.path.join(folder, "labels")
    imgs = [f for f in os.listdir(img_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    lbls = [f for f in os.listdir(lbl_dir) if f.lower().endswith(".txt")]
    return len(imgs), len(lbls), imgs[:5], lbls[:5]

for d in ("train", "val"):
    img_count, lbl_count, img_sample, lbl_sample = count(d)
    print(f"{d}: images={img_count}, labels={lbl_count}")
    print(f" sample images: {img_sample}")
    print(f" sample labels: {lbl_sample}\n")

# list val images missing labels
val_img_dir = os.path.join("val","images")
val_lbl_dir = os.path.join("val","labels")
missing = []
for fn in os.listdir(val_img_dir):
    if not fn.lower().endswith((".jpg",".jpeg",".png")):
        continue
    label_fn = os.path.splitext(fn)[0] + ".txt"
    if not os.path.exists(os.path.join(val_lbl_dir,label_fn)):
        missing.append(fn)
print("val images without label (first 20):", missing[:20])
print("total missing labels in val:", len(missing))
