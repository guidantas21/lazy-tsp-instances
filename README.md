# Lazy TSP Instances

The [TSPLIB 95 format](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) is widely used for representing instances of the Traveling Salesman Problem (TSP), but it can be tedious and error-prone to parse—especially when writing instance readers in different programming languages.

**Lazy TSP Instances** simplifies this format to the bare essentials, making it easier to load and use TSP instances in any environment. The script supports parallel processing and allows filtering by instance dimension.

---

## Lazy Instance Format

The simplified format contains only the instance name, dimension, and full weight matrix:

```
<instance name>
<dimension>
<weight matrix (dimension x dimension)>
```

---

## Example

### Original TSPLIB format:

```
NAME: toy5  
TYPE: TSP  
COMMENT: 5-city toy instance  
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

### Lazy format:

```
toy5
5
0   3   1   2   4
3   0   3   4   6
1   3   0   2   5
2   4   2   0   1
4   6   5   1   0
```

---

## Usage

### Dependencies

Install the required packages using:

```bash
pip install -r requirements.txt
```

### Command-line syntax

```bash
python3 main.py SOURCE_DIR TARGET_DIR [options]
```

### Positional arguments

* `SOURCE_DIR`: Path to the directory containing the original TSPLIB instances.
* `TARGET_DIR`: Path to the directory where simplified instances will be saved.

### Optional arguments

| Flag           | Description                                             | Default |
| -------------- | ------------------------------------------------------- | ------- |
| `-j`, `--jobs` | Number of processes to use for parallel processing      | 4       |
| `--override`   | Overwrite existing files in the target directory        | False   |
| `--min-dim`    | Minimum instance dimension (number of nodes) to include | None    |
| `--max-dim`    | Maximum instance dimension (number of nodes) to include | None    |



### Example

```bash
python3 main.py ./tsplib95-instances ./simplified-instances --min-dim 50 --max-dim 500 --override -j 8
```

This command processes all instances in `./tsplib95-instances` with dimensions between 50 and 500 (inclusive), using 8 parallel processes, and writes the simplified instances to `./simplified-instances`, overwriting existing files if necessary.


