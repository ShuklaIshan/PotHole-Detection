from pathlib import Path
import random
import csv

import cv2


DATASET = Path("data/india_pothole")
IMAGE_DIR = DATASET / "images/train"
LABEL_DIR = DATASET / "labels/train"

NUM_SAMPLES = 100
OUTPUT = Path("outputs/audit_results.csv")


def draw_boxes(image_path):
    image = cv2.imread(str(image_path))

    label_path = LABEL_DIR / f"{image_path.stem}.txt"

    h, w = image.shape[:2]

    if label_path.exists():
        for line in label_path.read_text().splitlines():
            parts = line.split()

            if len(parts) != 5:
                continue

            _, xc, yc, bw, bh = map(float, parts)

            x1 = int((xc - bw / 2) * w)
            y1 = int((yc - bh / 2) * h)
            x2 = int((xc + bw / 2) * w)
            y2 = int((yc + bh / 2) * h)

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 3)

    return image


def main():
    images = list(IMAGE_DIR.glob("*.jpg"))

    samples = random.sample(images, min(NUM_SAMPLES, len(images)))

    OUTPUT.parent.mkdir(exist_ok=True)

    results = []

    cv2.namedWindow("Pothole Audit", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Pothole Audit", 1200, 800)

    for index, image_path in enumerate(samples, start=1):

        image = draw_boxes(image_path)

        text = f"{index}/{len(samples)}   P=Pothole  N=Not pothole  U=Unclear  Q=Quit"

        cv2.putText(
            image,
            text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
        )

        cv2.imshow("Pothole Audit", image)

        while True:
            key = cv2.waitKey(0) & 0xFF

            if key in [ord("p"), ord("P")]:
                decision = "pothole"
                break

            if key in [ord("n"), ord("N")]:
                decision = "not_pothole"
                break

            if key in [ord("u"), ord("U")]:
                decision = "unclear"
                break

            if key in [ord("q"), ord("Q")]:
                cv2.destroyAllWindows()

                with open(OUTPUT, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["image", "decision"])
                    writer.writerows(results)

                print(f"Audit stopped early. Results saved to {OUTPUT}")
                return

        results.append([image_path.name, decision])

    cv2.destroyAllWindows()

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image", "decision"])
        writer.writerows(results)

    potholes = sum(r[1] == "pothole" for r in results)
    not_potholes = sum(r[1] == "not_pothole" for r in results)
    unclear = sum(r[1] == "unclear" for r in results)

    print("\n===== AUDIT COMPLETE =====")
    print(f"Potholes:     {potholes}")
    print(f"Not potholes: {not_potholes}")
    print(f"Unclear:      {unclear}")
    print(f"Results:      {OUTPUT}")


if __name__ == "__main__":
    main()