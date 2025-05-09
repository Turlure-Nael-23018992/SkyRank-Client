# ⚙️ SkyRank-Client — Installation Guide

This repository acts as a client wrapper for the SkyRank library, providing a simplified execution interface through the `Client/Engine.py` script. It includes two Git submodules:

- `SkyRank/` → [SkyRank](https://github.com/Turlure-Nael-23018992/SkyRank.git)
- `external/BBS/` → [BBS-Python-3.x-](https://github.com/Turlure-Nael-23018992/BBS-Python-3.x-.git), which itself includes:
- `RTree/` → [R-Tree-Python-3.x-](https://github.com/Turlure-Nael-23018992/R-Tree-Python-3.x-.git)

---

## 🚀 Clone the Project (with Submodules)

To properly install everything, you must clone the repository **with submodules recursively**:

```bash
git clone --recurse-submodules https://github.com/Turlure-Nael-23018992/SkyRank-Client.git
cd SkyRank-Client
cd SkyRank
git submodule update --init --recursive
```

## 📦 Install Requirements
```bash
pip install -r requirements.txt
```