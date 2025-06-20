# Ransomware Analysis Report

## Technical Overview
This Python script implements ransomware functionality with hybrid encryption (RSA+AES) and includes a decoy Notepad application.

## Encryption Specifications

### Target File Types
The ransomware encrypts **all file types** except those with `.enc` extension. When triggered via Notepad, it specifically targets:

```python
target_extensions = [
    '.txt', '.doc', '.docx', '.xls', '.xlsx', 
    '.ppt', '.pptx', '.pdf', '.jpg', '.png',
    '.sql', '.mdb', '.csv', '.psd', '.ai'
]

## Encryption Process

1. **AES-256-CBC encryption** for files
   - Uses 256-bit key size
   - Cipher Block Chaining (CBC) mode
   - PKCS#7 padding

2. **RSA-2048-OAEP** for key encryption
   - 2048-bit RSA keys
   - Optimal Asymmetric Encryption Padding (OAEP)
   - Encrypts the AES session keys

- **IV (16 bytes)**: Initialization Vector for AES-CBC
- **Encrypted AES key (256 bytes)**: RSA-encrypted AES session key
- **Encrypted file data**: Actual encrypted content

## Execution Flow

### Initial Infection

1. **File Encryption**:
- Recursively encrypts all files on Desktop
- Skips files with `.enc` extension
- Original files are deleted after encryption

2. **Ransom Note**:
- Creates `Decryption_password.txt` on Desktop
- Contains fake recovery instructions ("utssob uui z")

3. **User Notification**:
- Displays full-screen alert with red text
- Black background for high visibility
- Auto-dismisses after 3 seconds

4. **Decoy Application**:
- Launches a functional Notepad clone
- Provides basic text editing capabilities
- Serves as distraction from encryption process
