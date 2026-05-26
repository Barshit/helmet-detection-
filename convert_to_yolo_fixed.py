import os
import xml.etree.ElementTree as ET

ANNOT_DIR = "annotations"
OUT_LABEL_DIR = "labels"
os.makedirs(OUT_LABEL_DIR, exist_ok=True)

class_to_id = {}

for xml_file in sorted(os.listdir(ANNOT_DIR)):
    if not xml_file.endswith(".xml"):
        continue
    tree = ET.parse(os.path.join(ANNOT_DIR, xml_file))
    root = tree.getroot()
    size = root.find("size")
    if size is None:
        continue
    img_w = float(size.find("width").text)
    img_h = float(size.find("height").text)
    txt_lines = []
    for obj in root.findall("object"):
        name_tag = obj.find("name")
        if name_tag is None or not name_tag.text:
            continue
        class_name = name_tag.text.strip()
        if class_name not in class_to_id:
            class_to_id[class_name] = len(class_to_id)
        cls_id = class_to_id[class_name]
        bbox = obj.find("bndbox")
        if bbox is None:
            continue
        xmin = float(bbox.find("xmin").text)
        ymin = float(bbox.find("ymin").text)
        xmax = float(bbox.find("xmax").text)
        ymax = float(bbox.find("ymax").text)
        x_center = (xmin + xmax) / 2.0 / img_w
        y_center = (ymin + ymax) / 2.0 / img_h
        w = (xmax - xmin) / img_w
        h = (ymax - ymin) / img_h
        txt_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
    with open(os.path.join(OUT_LABEL_DIR, xml_file.replace(".xml", ".txt")), "w") as f:
        f.writelines(txt_lines)

print("Conversion done. Class mapping (id -> name):")
for name, idx in class_to_id.items():
    print(f"{idx}: {name}")
