# 🔤 KirilToLatin — Azerbaijani Cyrillic → Latin Converter

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Platform-Windows-informational?style=for-the-badge&logo=windows" />
  <img src="https://img.shields.io/badge/UI-CustomTkinter-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<p align="center">
  A modern, dark-themed desktop application that converts Azerbaijani Cyrillic text inside <strong>DOCX documents</strong> to Latin script — instantly and without any internet connection.
</p>

---

## ✨ Features

- 📄 **DOCX Support** — Converts `.docx` files while preserving all formatting (bold, italic, fonts, colors, tables, headers, footers)
- 🔤 **Full Azerbaijani Cyrillic Alphabet** — Accurate 1-to-1 character mapping based on the standard Azerbaijani Cyrillic alphabet
- 💬 **Quote Replacement** — Optional toggle to replace `«` and `»` with standard `"` double quotes
- 🎯 **Custom Save Location** — Choose exactly where to save the converted file before processing starts
- 🖤 **Modern Dark UI** — Sleek, premium dark theme built with CustomTkinter
- ❌ **One-Click Clear** — Clear selected file with the circular button on the top-right of the drop zone
- 📦 **Standalone .exe** — Can be packaged into a single portable Windows executable (no Python needed)

---

## 🖼️ Character Mapping Table

| Cyrillic | Latin | Cyrillic | Latin |
|----------|-------|----------|-------|
| А а | A a | Н н | N n |
| Б б | B b | О о | O o |
| В в | V v | Ө ө | Ö ö |
| Г г | Q q | П п | P p |
| Ғ ғ | Ğ ğ | Р р | R r |
| Д д | D d | С с | S s |
| Е е | E e | Т т | T t |
| Ә ә | Ə ə | У у | U u |
| Ж ж | J j | Ү ү | Ü ü |
| З з | Z z | Ф ф | F f |
| И и | İ i | Х х | X x |
| Ы ы | I ı | Һ һ | H h |
| Ј ј | Y y | Ч ч | Ç ç |
| К к | K k | Ш ш | Ş ş |
| Ҝ ҝ | G g | Ҹ ҹ | C c |
| Л л | L l | | |
| М м | M m | | |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8 or higher** (3.8 recommended for maximum Windows compatibility including Windows 7)
- `pip` package manager

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/KirilToLatin.git
cd KirilToLatin/python_app
```

**2. (Optional but recommended) Create a virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the application:**
```bash
python main.py
```

---

## 📦 Building a Standalone `.exe`

To distribute the app without requiring Python on the target machine:

```bash
pyinstaller --clean --onefile --windowed --name KirilToLatin ^
  --icon=icon.ico ^
  --version-file=version_info.txt ^
  --add-data "path\to\customtkinter;customtkinter" ^
  --hidden-import="jaraco" ^
  --hidden-import="platformdirs" ^
  --hidden-import="packaging" ^
  main.py
```

> 💡 Replace `path\to\customtkinter` with the actual path from:
> ```bash
> python -c "import customtkinter; print(customtkinter.__file__)"
> ```

The resulting `.exe` will be inside the `dist/` folder.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Python 3.8+](https://www.python.org/) | Core programming language |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Modern dark-themed GUI framework |
| [python-docx](https://python-docx.readthedocs.io/) | Reading and writing `.docx` files |
| [PyInstaller](https://pyinstaller.org/) | Packaging into standalone `.exe` |

---

## 📋 Requirements

```
customtkinter==5.2.2
python-docx==1.1.0
pyinstaller==6.4.0
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
python_app/
│
├── main.py            # Main app entry point & UI
├── converter.py       # Cyrillic → Latin character mapping engine
├── docx_handler.py    # DOCX file processing logic
├── requirements.txt   # Python dependencies
├── version_info.txt   # Windows EXE version metadata
├── icon.ico           # Application icon (optional)
└── build.bat          # Windows build helper script
```

---

## 📝 How It Works

1. **User selects a `.docx` file** via the file browser or drag-and-drop
2. **User chooses a save location** for the converted output file
3. The app reads every paragraph, run, table cell, header, and footer inside the document
4. **Each Cyrillic character is mapped 1-to-1** to its Latin equivalent
5. All original formatting (bold, italic, font size, color) is preserved
6. The converted document is saved to the chosen location

---

## ⚙️ Compatibility

| OS | Status |
|---|---|
| Windows 10 / 11 | ✅ Fully supported |
| Windows 7 / 8 | ✅ Supported (build with Python 3.8) |
| macOS / Linux | ⚠️ UI works, `.exe` packaging is Windows-only |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ for Azerbaijani document workflows</p>
