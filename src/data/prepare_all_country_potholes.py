from pathlib import Path
import shutil
import hashlib
import random

# --------------------------------------------------
# PATHS
# --------------------------------------------------

SOURCE = Path(
    r"C:\Users\shukl\OneDrive\Desktop\archive\RDD_SPLIT"
)

DEST = Path(
    r"C:\Users\shukl\OneDrive\Desktop\PotHole-Detection"
    r"\data\all_countries_pothole"
)

# Original RDD_SPLIT mapping: class 4 = Pothole
POTHOLE_CLASS_ID = 4
NEW_CLASS_ID = 0

SPLITS = ("train", "val", "test")


def image_hash(path):
    """Return a hash to help identify duplicate image contents."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Original dataset not found: {SOURCE}"
        )

    if DEST.exists() and any(DEST.iterdir()):
        raise FileExistsError(
            f"Destination is not empty: {DEST}\n"
            "Move or rename it before running this script again. "
            "The script will not overwrite existing data."
        )

    # Validate the original structure before copying anything.
    for split in SPLITS:
        image_dir = SOURCE / split / "images"
        label_dir = SOURCE / split / "labels"

        if not image_dir.is_dir() or not label_dir.is_dir():
            raise FileNotFoundError(
                f"Missing images or labels for split: {split}"
            )

    image_hashes = {}
    counts = {}

    # --------------------------------------------------
    # FILTER AND COPY IMAGES/LABELS
    # --------------------------------------------------

    for split in SPLITS:
        source_images = SOURCE / split / "images"
        source_labels = SOURCE / split / "labels"

        dest_images = DEST / "images" / split
        dest_labels = DEST / "labels" / split

        dest_images.mkdir(parents=True, exist_ok=True)
        dest_labels.mkdir(parents=True, exist_ok=True)

        image_files = sorted(
            p for p in source_images.iterdir()
            if p.is_file() and p.suffix.lower() in
            {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        )

        kept_images = 0
        kept_boxes = 0
        missing_labels = 0

        for image_path in image_files:
            label_path = source_labels / (
                image_path.stem + ".txt"
            )

            if not label_path.is_file():
                missing_labels += 1
                continue

            pothole_boxes = []

            with label_path.open("r", encoding="utf-8") as file:
                for line in file:
                    fields = line.strip().split()

                    if not fields:
                        continue

                    try:
                        class_id = int(fields[0])
                    except ValueError:
                        raise ValueError(
                            f"Invalid class ID in {label_path}: {line}"
                        )

                    if class_id != POTHOLE_CLASS_ID:
                        continue

                    if len(fields) != 5:
                        raise ValueError(
                            f"Expected 5 YOLO fields in {label_path}: "
                            f"{line}"
                        )

                    # Preserve box coordinates; remap class 4 -> 0.
                    pothole_boxes.append(
                        "0 " + " ".join(fields[1:])
                    )

            # This dataset contains only images with potholes.
            if not pothole_boxes:
                continue

            digest = image_hash(image_path)

            # Record duplicates across splits for review.
            previous_split = image_hashes.get(digest)
            if previous_split and previous_split != split:
                print(
                    "WARNING: Duplicate image content across splits:",
                    image_path.name,
                    f"({previous_split} and {split})"
                )
            else:
                image_hashes[digest] = split

            shutil.copy2(
                image_path,
                dest_images / image_path.name
            )

            with (
                dest_labels / f"{image_path.stem}.txt"
            ).open("w", encoding="utf-8") as file:
                file.write("\n".join(pothole_boxes) + "\n")

            kept_images += 1
            kept_boxes += len(pothole_boxes)

        counts[split] = (kept_images, kept_boxes)

        print(
            f"{split}: {kept_images} images, "
            f"{kept_boxes} pothole boxes, "
            f"{missing_labels} missing label files"
        )

    # --------------------------------------------------
    # WRITE YOLO DATASET CONFIGURATION
    # --------------------------------------------------

    yaml_path = DEST / "data.yaml"

    yaml_path.write_text(
        f"path: {DEST.as_posix()}\n"
        "train: images/train\n"
        "val: images/val\n"
        "test: images/test\n"
        "nc: 1\n"
        "names:\n"
        "  0: pothole\n",
        encoding="utf-8"
    )

    print("\nDataset preparation complete.")
    print(f"Dataset: {DEST}")
    print(f"Configuration: {yaml_path}")
    print("\nSummary:")

    total_images = 0
    total_boxes = 0

    for split, (images, boxes) in counts.items():
        print(f"  {split}: {images} images, {boxes} boxes")
        total_images += images
        total_boxes += boxes

    print(f"  TOTAL: {total_images} images, {total_boxes} boxes")


if __name__ == "__main__":
    main()

