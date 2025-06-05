import tsplib95
import argparse
import os
import logging
from pathlib import Path
from multiprocessing import Pool, current_process


def setup_logger() -> logging.Logger:
    logger = logging.getLogger(str(current_process().pid))
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [PID %(process)d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger


logger = setup_logger()


def simplify_instance_pair(paths: tuple[Path, Path]) -> None:
    input_instance_path, output_instance_path = paths

    try:
        instance = tsplib95.load(input_instance_path)
        logger.info(f"Processing {instance.name}")

        with open(output_instance_path, "w") as file:
            file.write(f"{instance.name}\n")
            file.write(f"{instance.dimension}\n")
            for i in instance.get_nodes():
                for j in instance.get_nodes():
                    file.write(f"{instance.get_weight(i, j)}\t")
                file.write("\n")

        logger.info(f"Converted {input_instance_path} → {output_instance_path}")
    except Exception as e:
        logger.error(f"Failed to process {input_instance_path}: {e}")


def simplify_instance_dir(
    source_dir: Path,
    target_dir: Path,
    num_processes: int = 4,
    override: bool = False,
    min_dim: int | None = None,
    max_dim: int | None = None,
) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)

    tasks = []

    for file in source_dir.iterdir():
        if file.is_file():
            try:
                instance = tsplib95.load(file)
                dim = instance.dimension

                if (min_dim is not None and dim < min_dim) or (
                    max_dim is not None and dim > max_dim
                ):
                    continue

                target_file = target_dir / file.name
                if override or not target_file.exists():
                    tasks.append((file, target_file))

            except Exception as e:
                logger.error(f"Skipping {file.name}: failed to load ({e})")

    with Pool(processes=num_processes) as pool:
        pool.map(simplify_instance_pair, tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simplify the format of the TSPLIB instances using multiprocessing"
    )
    parser.add_argument(
        "source_dir", type=Path, help="Path to the source directory"
    )
    parser.add_argument(
        "target_dir", type=Path, help="Path to the target directory"
    )
    parser.add_argument(
        "-j", "--jobs", type=int, default=4, help="Number of processes to use"
    )
    parser.add_argument(
        "--override", action="store_true", help="Overwrite existing files"
    )

    parser.add_argument(
        "--min-dim", type=int, help="Minimum instance dimension to include"
    )
    parser.add_argument(
        "--max-dim", type=int, help="Maximum instance dimension to include"
    )

    args = parser.parse_args()

    simplify_instance_dir(
        args.source_dir,
        args.target_dir,
        args.jobs,
        args.override,
        args.min_dim,
        args.max_dim,
    )
