# ⚡ SkyRank-Client

SkyRank-Client is a wrapper for the SkyRank library that allows you to easily execute Skyline ranking algorithms via the `Client/Engine.py` script.

---

## 🚀 Overview

This project provides:

✅ A simple interface to run Skyline ranking algorithms  
✅ Compatibility with multiple input formats (JSON, Dict, or SQLite)  
✅ Integration with PyPy for high-performance execution

---

## 🔗 Installation Guide

For detailed installation instructions, please refer to the [INSTALL.md](./INSTALL.md) file.

---

## 🐍 PyPy Installation (Recommended)

To run SkyRank-Client efficiently, we recommend using [PyPy 3.10](https://www.pypy.org/download.html) instead of the standard Python interpreter.

### ➡️ Windows Installation

1️⃣ Download the **Windows** installer from the [PyPy 3.10 download page](https://www.pypy.org/download.html).  
2️⃣ Extract the downloaded archive (for example: `D:\pypy3.10-v7.3.19-win64`).  
3️⃣ Add the extracted directory to your PATH variable (optional but recommended).

### ➡️ Linux/macOS Installation

1️⃣ Download the appropriate **PyPy 3.10** tarball from the [PyPy 3.10 download page](https://www.pypy.org/download.html).  
2️⃣ Extract the archive using:
```bash
tar -xvf pypy3.10-v7.3.19-linux64.tar.bz2
```
3️⃣ Add the extracted folder to your PATH:
```bash
export PATH=$PATH:/path/to/pypy3.10-v7.3.19-linux64/bin
```
Optionally, add this line to your `.bashrc` or `.zshrc` to persist the change.

---

## 📦 Installing Dependencies with PyPy

Once PyPy is installed and the project is cloned:

1️⃣ Open a terminal in the project root (where `requirements.txt` is located).  
2️⃣ Run the following commands to install dependencies using PyPy:
```bash
/path/to/pypy3.10-v7.3.19-linux64/bin/pypy3.10 -m ensurepip
/path/to/pypy3.10-v7.3.19-linux64/bin/pypy3.10 -m pip install --upgrade pip
/path/to/pypy3.10-v7.3.19-linux64/bin/pypy3.10 -m pip install -r requirements.txt
```
(Replace `/path/to/` with the actual path on your system.)

---

## ⚡ Usage

Once installed, you can run algorithms with the `Client/Engine.py` script.  
Here’s how to use it with **PyPy**:
```bash
/path/to/pypy3.10-v7.3.19-linux64/bin/pypy3.10 Client/Engine.py
```
On Windows:
```bash
D:\pypy3.10-v7.3.19-win64\pypy3.10.exe Client/Engine.py
```

---

### 📝 Example Configuration:

- **Input File**: JSON, Dict, or SQLite.
- **Algorithm**: Choose between `CoskySQL`, `CoskyAlgorithme`, `RankSky`, `DpIdpDh`, and `SkyIR`.
- **Preferences**: Required for some algorithms, e.g., `[Preference.MIN, Preference.MIN, Preference.MIN]`.

Modify `Client/Engine.py` to point to your input file and set the correct preferences.  
Run the script and you’ll see the results in the console.

---

## 🛠️ Development Notes

- Always ensure submodules are updated:
```bash
git submodule update --init --recursive
```
- If needed, re-run dependency installation with:
```bash
/path/to/pypy3.10-v7.3.19-linux64/bin/pypy3.10 -m pip install -r requirements.txt
```

Happy ranking! 🚀
