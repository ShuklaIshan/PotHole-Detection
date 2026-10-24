from pathlib import Path
import random

import cv2
import matplotlib.pyplot as plt


DATASET = Path("data/india_pothole")
IMAGE_DIR = DATASET / "images/train"
LABEL_DIR = DATASET / "labels/train"

NUM_SAMPLES = 20
COLS = 4


def draw_boxes(image_path):
    image = cv2.imread(str(image_path))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    label_path = LABEL_DIR / f"{image_path.stem}.txt"

    h, w = image.shape[:2]

    if label_path.exists():
        for line in label_path.read_text().splitlines():
            cls, xc, yc, bw, bh = map(float, line.split())

            x1 = int((xc - bw / 2) * w)
            y1 = int((yc - bh / 2) * h)
            x2 = int((xc + bw / 2) * w)
            y2 = int((yc + bh / 2) * h)

            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(
                image,
                "pothole",
                (x1, max(y1 - 5, 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2,
            )

    return image


def main():
    images = list(IMAGE_DIR.glob("*.jpg"))

    samples = random.sample(images, min(NUM_SAMPLES, len(images)))

    rows = (len(samples) + COLS - 1) // COLS

    fig, axes = plt.subplots(rows, COLS, figsize=(16, 4 * rows))
    axes = axes.flatten()

    for ax, image_path in zip(axes, samples):
        image = draw_boxes(image_path)

        ax.imshow(image)
        ax.set_title(image_path.name)
        ax.axis("off")

    for ax in axes[len(samples):]:
        ax.axis("off")

    plt.tight_layout()

    output = Path("outputs/dataset_samples.jpg")
    output.parent.mkdir(exist_ok=True)

    plt.savefig(output, dpi=150)
    plt.show()

    print(f"Saved visualization to: {output}")


if __name__ == "__main__":
    main()