# 🛡️ Certificate Converter (.der ➡️ .0)

A simple **PyQt5-based GUI tool** to convert `.der` certificate files into `.0` files (used in OpenSSL trust stores).  
The tool loads a DER-encoded certificate, converts it to PEM, generates the `subject_hash_old`, and renames the certificate file to `<hash>.0` automatically.

---

## ✨ Features

- 🗂️ Browse and select `.der` certificate files via a GUI.
- 🔄 Convert `.der` to `.pem` format.
- 🧮 Generate **subject_hash_old** (OpenSSL-compatible hash).
- 📝 Automatically rename and save the certificate as `<hash>.0`.
- 🖥️ User-friendly PyQt5 interface with logging output.
- ℹ️ Includes **About** and **Exit** options in the menu bar.

---

## 📦 Requirements

Install dependencies:

```bash
pip install PyQt5 pyopenssl
```

---

## ▶️ Usage

Run the program:

```bash
python cert_converter.py
```

1. Click **Browse .der File** to select your certificate.
2. The tool will:
   - Convert `.der` → `.pem`
   - Generate the hash
   - Rename the file to `<hash>.0`
   - Show logs in the output window
3. A popup will confirm successful conversion.

---

## 📂 Project Structure

```
.
├── cert_converter.py   # Main application script
├── images.ico          # Application icon
└── README.md           # Project documentation
```

---

## 🖼️ Screenshot

![Certificate Converter](https://github.com/hadesninja/Certificate-Converter/blob/master/screenshots/certificate_converter.png)

---

## ℹ️ About

- **Version:** 1.0
- **Developer:** Vaibhav Patil

---

## ⚠️ Notes

- Only `.der` files are supported as input.
- The tool renames the output to `<subject_hash_old>.0` automatically.
- Make sure you have read/write permission in the folder where the `.der` file is located.

---

## 📜 License

This project is licensed under the MIT License.
