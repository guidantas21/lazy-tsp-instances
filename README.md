# Lazy TSP instances

The TSPLIB instance format is quite annoying to parse, and it is annoying to write a parser for each lprgramming language. Therefore, the idea is to simplify the instance to the most format basic format possible, so writting a instance reader is awalays trivial and does not take a lot of time. This script simplifies TSPLIB instance files by extracting the distance matrix and saving it in a simpler format. It supports parallel processing and filtering based on instance dimensions.

## Lazy instance format

The format contains only the instance name, dimension and weight matrix:

```
<instance name>
<dimension>
<weight matrix (dimension x dimension)>
```

## Example

Original TSPLIB format:

```
NAME: toy5
TYPE: TSP
COMMENT: 17-city problem (Groetschel)
DIMENSION: 5
EDGE_WEIGHT_TYPE: EXPLICIT
EDGE_WEIGHT_FORMAT: FULL_MATRIX 
EDGE_WEIGHT_SECTION
    0   3   1   2   4
    3   0   3   4   6
    1   3   0   2   5
    2   4   2   0   1
    4   6   5   1   0
EOF
```

Lazy format:


```
toy5
5
0   3   1   2   4
3   0   3   4   6
1   3   0   2   5
2   4   2   0   1
4   6   5   1   0
```


Here’s a **Usage** section you can include in your `README.md`:

---

## Usage



### Command-line arguments

```bash
python3 main.py SOURCE_DIR TARGET_DIR [options]
```

### Positional arguments

* `SOURCE_DIR`: Path to the directory containing the original TSPLIB instances.
* `TARGET_DIR`: Path to the directory where simplified instances will be saved.

### Optional flags

| Flag           | Description                                        | Default |
| -------------- | -------------------------------------------------- | ------- |
| `-j`, `--jobs` | Number of processes to use for parallel processing | 4       |
| `--override`   | Overwrite existing files in the target directory   | Off     |
| `--min-dim`    | Minimum number of nodes (dimension) to process     | None    |
| `--max-dim`    | Maximum number of nodes (dimension) to process     | None    |

### Example

```bash
python3 main.py ./tsplib95-instances ./simplified-instances --min-dim 50 --max-dim 500 --override -j 8
```

This command processes all instances in `./tsplib95-instances` with dimensions between 50 and 500 (inclusive), using 8 parallel processes, and writes the simplified files to `./simplified-instances`, overwriting any existing files there.


