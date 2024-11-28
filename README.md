# SecureZip: Encrypted File Compression Tool

## Overview
SecureZip is a Python desktop application for secure file compression and encryption, creating custom .seczip archives with robust security features.

## Features
- 🔒 Custom encryption with .seczip extension
- 📁 File compression and decryption
- 🖥️ User-friendly GUI with progress tracking
- 🔑 Secure key management system
- 💻 Cross-platform desktop application

## Security Architecture
- Implements Fernet symmetric encryption
- AES-256 bit encryption standard
- Automatic key generation and management
- Secure file handling workflow

## Technical Requirements
- Python 3.8+
- cryptography library
- tkinter
- Minimal system resources

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/securezip.git

# Install dependencies
pip install cryptography

# Run the application
python secure_compressor.py
