# pyhartig

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org/downloads)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A Python implementation of the formal algebra for Knowledge Graph Construction, based on the work of Olaf
> Hartig. [An Algebraic Foundation for Knowledge Graph Construction](https://arxiv.org/abs/2503.10385)

---

## 1. Project Context

This library is a research project developed for the **"Engineering For Research I"** module.

It is part of the **M1 Computer Science, SMART Computing Master's Program** at **Nantes Université**.

The project is hosted by the **LS2N (Laboratoire des Sciences du Numérique de Nantes)**, within the **GDD (Graphes,
Données, Décision) team**.

## 2. Overview

`pyhartig` provides a set of composable Python objects representing the core algebraic operators for querying
heterogeneous data sources.

This library is a core component of the **MCP-SPARQLLM** research project, which aims to provide the logical layer for
translating heterogeneous data (e.g., JSON from an API, CSV, LLM outputs) into a homogeneous, queryable format.

## 3. Theoretical Foundation

This implementation is formally grounded in the algebraic foundation defined by **Olaf Hartig**. We are implementing the
operators described in his work, which provide a formal semantics for defining data transformation and integration
operators (like `Source`, `Join`, `Project`, etc.) independent of the specific data source.

The foundational paper for this work is:

**Hartig, O. (2025). [*An Algebraic Foundation for Knowledge Graph Construction*](https://arxiv.org/abs/2503.10385).**

## 4. Installation

For development, it is highly recommended to install the library in "editable" mode in a virtual environment.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Armotik/pyhartig](https://github.com/Armotik/pyhartig)
   cd pyhartig
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install in editable mode (with test dependencies):**
   ```bash
   pip install -e '.[test]'
   ```
   The `-e` flag links your installation to your `src/` directory, so any code changes are immediately available.

## 5. Authors

This project is developed by:

* **Anthony MUDET**
* **Léo FERMÉ**
* **Mohamed Lamine MERAH**

### 5.1. Supervision

This project is supervised by:

* **Full Professor Pascal MOLLI**
* **Full Professor Hala SKAF-MOLLI**
* **Associate Professor Gabriela MONTOYA**

## 6. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 7. Acknowledgements

We would like to thank the LS2N and GDD team for their support and resources provided during this project.
We also acknowledge the foundational work of Olaf Hartig, which inspired this implementation.

## 8. Contact

For any questions or contributions, please open an issue or contact the authors directly.

