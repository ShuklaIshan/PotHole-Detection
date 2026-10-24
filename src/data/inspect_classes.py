from pathlib import Path
import cv2

ROOT = Path(r"C:\Users\shukl\OneDrive\Desktop\archive\RDD_SPLIT")
IMAGE_DIR = ROOT / "train" / "images"
LABEL_DIR = ROOT / "train" / "labels"

# Find one India example for each class
examples = {}

for label_file in LABEL_DIR.glob("India_*.txt"):
    lines = label_file.read_text().splitlines()

    for line in lines:
        parts = line.split()
        if len(parts) == 5:
            class_id = int(parts[0])

            if class_id not in examples:
                examples[class_id] = (label_file, line)

    if len(examples) == 5:
        break

print("Examples found:")
for class_id, (label_file, line) in sorted(examples.items()):
    print(f"Class {class_id}: {label_file.name} -> {line}")

for class_id, (label_file, target_line) in sorted(examples.items()):

    image_file = IMAGE_DIR / f"{label_file.stem}.jpg"
    image = cv2.imread(str(image_file))

    if image is None:
        continue

    H, W = image.shape[:2]

    # Draw ONLY the selected class
    for line in label_file.read_text().splitlines():
        parts = line.split()

        if len(parts) != 5:
            continue

        cls, xc, yc, bw, bh = map(float, parts)

        if int(cls) != class_id:
            continue

        x1 = int((xc - bw / 2) * W)
        y1 = int((yc - bh / 2) * H)
        x2 = int((xc + bw / 2) * W)
        y2 = int((yc + bh / 2) * H)

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 4)

    cv2.putText(
        image,
        f"CLASS {class_id}",
        (20, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 255),
        3
    )

    cv2.imshow(f"Class {class_id}", image)

    print(f"\nShowing CLASS {class_id}")
    print(f"Image: {image_file.name}")
    print(f"Label: {target_line}")
    print("Press any key for the next class.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()