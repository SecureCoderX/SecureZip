# SecureZip: Multi-File Encrypted Compression Tool

## Overview
SecureZip is an advanced Python desktop application designed for secure, multi-file compression and encryption. Create robust, encrypted archives with multiple files using a custom .seczip extension.

## 🌟 Key Features
- 📂 Multi-file selection and compression
- 🔒 Custom .seczip encryption
- 🖥️ Intuitive graphical user interface
- 🔑 Secure key management
- 📊 Progress tracking
- 💻 Cross-platform compatibility

## Technical Specifications
- **Language**: Python 3.8+
- **Encryption**: Fernet (AES-256)
- **GUI**: Tkinter
- **Libraries**: 
  - cryptography
  - zipfile

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/chadparker/securezip.git

# Navigate to project directory
cd securezip

# Install dependencies
pip install cryptography
```

## 🛠 Usage

### Compression Workflow
1. Launch the application
2. Click "Select Files to Compress"
3. Choose multiple files
4. Review selected files in list
5. Remove files if needed
6. Click "Compress Selected Files"
7. Choose save location
8. Encrypted .seczip created!

### Decryption Workflow
1. Click "Select File to Decrypt"
2. Choose .seczip file
3. Select destination folder
4. Decrypt and extract files

## 🔒 Security Notes
- Encryption key is automatically generated
- Store encryption key securely
- Key loss means unrecoverable files

## 🛡️ Security Features
- AES-256 bit encryption
- Automatic key management
- Single encrypted archive for multiple files
- Secure file handling

## Potential Improvements
- [ ] Cloud key backup
- [ ] Enhanced logging
- [ ] Password-based key generation
- [ ] File integrity verification

## ⚠️ Warnings
- Keep encryption key private
- Do not share .seczip files without key
- Verify file integrity after transfer

## Contributing
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## License
MIT License

## 👤 Author
Chad Parker