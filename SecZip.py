import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cryptography.fernet import Fernet
import zipfile
import threading
import os

class SecureCompressorApp:
    def __init__(self, master):
        self.master = master
        master.title("Secure File Compressor")
        master.geometry("400x300")
        master.resizable(False, False)
        
        # Key management
        self.key_file = 'encryption_key.key'
        self.key = self.load_or_generate_key()
        self.cipher_suite = Fernet(self.key)
        
        # UI Components
        self.create_widgets()
        
    def create_widgets(self):
        # Compress Section
        compress_frame = ttk.LabelFrame(self.master, text='Compress & Encrypt')
        compress_frame.pack(padx=10, pady=10, fill='x')
        
        self.compress_button = ttk.Button(compress_frame, text='Select File to Compress',command=self.compress_encrypt_file)
        self.compress_button.pack(pady=5, padx=10, fill='x')
        
        # Decompress Section
        decompress_frame = ttk.LabelFrame(self.master, text='Decrypt & Decompress')
        decompress_frame.pack(padx=10, pady=10, fill='x')
        
        self.decompress_button = ttk.Button(decompress_frame, text='Select File to Decrypt',command=self.decrypt_decompress_file)
        self.decompress_button.pack(pady=5, padx=10, fill='x')
        
        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.master, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.pack(pady=10)
        
        # Status Label
        self.status_label = ttk.Label(self.master, text='Ready', anchor='center')
        self.status_label.pack(pady=5)
        
    def load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
        
    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.master.update_idletasks()
        
    def update_status(self, message):
        self.status_label.config(text=message)
        self.master.update_idletasks()
        
        
    def compress_encrypt_file(self):
        # Disable buttons during operation
        self.compress_button.config(state='disabled')
        self.decompress_button.config(state='disabled')
        
        # Reset progress
        self.update_progress(0)
        self.update_status('Selecting file...')
        
        input_file = filedialog.askopenfilename()
        if not input_file:
            return
        
        output_file = filedialog.asksaveasfilename(defaultextension=".seczip")
        if not output_file:
            self.reset_ui()
            return
        
        # Use threading to prevent UI freeze
        threading.Thread(target=self.compress_encrypt_thread, args=(input_file, output_file), daemon=True).start()
        
    def compress_encrypt_thread(self, input_file, output_file):
        try:
            # Get file size for progress bar
            file_size = os.path.getsize(input_file)
            
            # Compress
            self.update_status('Compressing file...')
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(input_file, arcname=os.path.basename(input_file))
                
            self.update_progress(50)
            self.update_status('Encrypting file...')
                
            # Encrypt
            with open(output_file, 'rb') as f:
                data = f.read()
            encrypted_data = self.cipher_suite.encrypt(data)
            
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)
                
            self.update_progress(100)
            self.update_status('File compressed and encrypted successfully!')
            
            # Show success message in the main thread
            self.master.after(0, self.show_success, "File compressed and encrypted successfully!")
        except Exception as e:
            # Show error message in the main thread
            self.master.after(0, self.show_error, f"An error occurred: {e}")
        finally:
            # Reset UI in the main thread
            self.master.after(0, self.reset_ui)
            
    def decrypt_decompress_file(self):
        # Disable buttons during operation
        self.compress_button.config(state='disabled')
        self.decompress_button.config(state='disabled')
        
        # Reset progress
        self.update_progress(0)
        self.update_status('Selecting file...')
        
        input_file = filedialog.askopenfilename(filetypes=[('Secure Zip Files', '*.seczip')])
        if not input_file:
            self.reset_ui()
            return
        
        output_dir = filedialog.askdirectory()
        if not output_dir:
            self.reset_ui()
            return
        
        # Use threading to prevent UI freeze
        threading.Thread(target=self.decrypt_decompress_thread, args=(input_file, output_dir), daemon=True).start()
        
    def decrypt_decompress_thread(self, input_file, output_dir):
        try:
            # Decrypt
            self.update_status('Decrypting file...')
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            
            self.update_progress(50)
            self.update_status('Decompressing file...')
            
            # Decompress
            temp_zip = os.path.join(output_dir, 'temp_decrypted.zip')
            with open(temp_zip, 'wb') as f:
                f.write(decrypted_data)
                
            with zipfile.ZipFile(temp_zip, 'r') as zipf:
                zipf.extractall(output_dir)
                
            os.remove(temp_zip)
            
            self.update_progress(100)
            self.update_status('File decrypted and decompressed successfully!')
            
            # Show success message in the main thread
            self.master.after(0, self.show_success, "File decrypted and decompressed successfully!")
        except Exception as e:
            # Show error message in the main thread
            self.master.after(0, self.show_error, f"An error occurred: {e}")
        finally:
            # Reset UI in the main thread
            self.master.after(0, self.reset_ui)
            
    def show_success(self, message):
        messagebox.showinfo('Success', message)
        
    def show_error(self, message):
        messagebox.showerror('Error', message)
        
    def reset_ui(self):
        self.compress_button.config(state='normal')
        self.decompress_button.config(state='normal')
        self.update_progress(0)
        self.update_status('Ready')  
            
def main():
    root = tk.Tk()
    SecureCompressorApp(root)
    root.mainloop()
        
if __name__ == '__main__':
    main()