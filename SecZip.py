import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cryptography.fernet import Fernet
import zipfile
import threading

class SecureCompressorApp:
    def __init__(self, master):
        self.master = master
        master.title("Secure Multi-File Compressor")
        master.geometry("450x400")
        master.resizable(False, False)

        # Key management
        self.key_file = 'encryption_key.key'
        self.key = self.load_or_generate_key()
        self.cipher_suite = Fernet(self.key)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Multi-File Compress Section
        compress_frame = ttk.LabelFrame(self.master, text="Compress & Encrypt Multiple Files")
        compress_frame.pack(padx=10, pady=10, fill='x')

        # File Selection Button
        self.select_files_button = ttk.Button(compress_frame, text="Select Files to Compress", 
                                              command=self.select_multiple_files)
        self.select_files_button.pack(pady=5, padx=10, fill='x')

        # Selected Files Listbox
        self.files_listbox = tk.Listbox(compress_frame, height=5, width=50)
        self.files_listbox.pack(pady=5, padx=10, fill='x')

        # Remove Selected File Button
        self.remove_file_button = ttk.Button(compress_frame, text="Remove Selected File", 
                                              command=self.remove_selected_file)
        self.remove_file_button.pack(pady=5, padx=10, fill='x')

        # Compress Button
        self.compress_button = ttk.Button(compress_frame, text="Compress Selected Files", 
                                           command=self.compress_encrypt_files)
        self.compress_button.pack(pady=5, padx=10, fill='x')

        # Decompress Section
        decompress_frame = ttk.LabelFrame(self.master, text="Decrypt & Decompress")
        decompress_frame.pack(padx=10, pady=10, fill='x')

        self.decompress_button = ttk.Button(decompress_frame, text="Select File to Decrypt", 
                                            command=self.decrypt_decompress_file)
        self.decompress_button.pack(pady=5, padx=10, fill='x')

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.master, orient='horizontal', 
                                            length=350, mode='determinate')
        self.progress_bar.pack(pady=10)

        # Status Label
        self.status_label = ttk.Label(self.master, text="Ready", anchor='center')
        self.status_label.pack(pady=5)

        # List to store selected files
        self.selected_files = []

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

    def select_multiple_files(self):
        # Open file dialog for multiple file selection
        files = filedialog.askopenfilenames(title="Select files to compress")
        
        # Add new files to the list
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                self.files_listbox.insert(tk.END, os.path.basename(file))

    def remove_selected_file(self):
        # Get selected indices
        selected_indices = self.files_listbox.curselection()
        
        # Remove from end to beginning to avoid index shifting
        for index in reversed(selected_indices):
            del self.selected_files[index]
            self.files_listbox.delete(index)

    def compress_encrypt_files(self):
        # Check if files are selected
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select files to compress")
            return

        # Choose output file
        output_file = filedialog.asksaveasfilename(defaultextension=".seczip")
        if not output_file:
            return

        # Disable buttons during operation
        self.select_files_button.config(state='disabled')
        self.remove_file_button.config(state='disabled')
        self.compress_button.config(state='disabled')
        self.decompress_button.config(state='disabled')
        
        # Reset progress
        self.update_progress(0)
        self.update_status("Compressing files...")

        # Start compression in a separate thread
        threading.Thread(target=self.compress_encrypt_thread, 
                         args=(self.selected_files, output_file), 
                         daemon=True).start()

    def compress_encrypt_thread(self, files, output_file):
        try:
            # Create temporary zip file
            temp_zip = output_file + '_temp.zip'
            
            # Compress multiple files
            with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    zipf.write(file, arcname=os.path.basename(file))
            
            self.update_progress(50)
            self.update_status("Encrypting...")
            
            # Read zip file
            with open(temp_zip, 'rb') as f:
                data = f.read()
            
            # Encrypt
            encrypted_data = self.cipher_suite.encrypt(data)
            
            # Write encrypted data
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Remove temporary zip
            os.remove(temp_zip)
            
            self.update_progress(100)
            self.update_status("Compression and Encryption Complete!")
            
            # Show success message in main thread
            self.master.after(0, self.show_success, f"{len(files)} files compressed and encrypted!")
        except Exception as e:
            # Show error message in main thread
            self.master.after(0, self.show_error, str(e))
        finally:
            # Reset UI in main thread
            self.master.after(0, self.reset_ui)

    def decrypt_decompress_file(self):
        # Disable buttons during operation
        self.select_files_button.config(state='disabled')
        self.remove_file_button.config(state='disabled')
        self.compress_button.config(state='disabled')
        self.decompress_button.config(state='disabled')
        
        # Reset progress
        self.update_progress(0)
        self.update_status("Selecting file...")

        input_file = filedialog.askopenfilename(filetypes=[("Secure Zip", "*.seczip")])
        if not input_file:
            self.reset_ui()
            return

        output_dir = filedialog.askdirectory()
        if not output_dir:
            self.reset_ui()
            return

        # Use threading to prevent UI freezing
        threading.Thread(target=self.decrypt_decompress_thread, 
                         args=(input_file, output_dir), 
                         daemon=True).start()

    def decrypt_decompress_thread(self, input_file, output_dir):
        try:
            # Decrypt
            self.update_status("Decrypting...")
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)

            self.update_progress(50)
            self.update_status("Decompressing...")

            # Decompress
            temp_zip = os.path.join(output_dir, 'temp_decrypted.zip')
            with open(temp_zip, 'wb') as f:
                f.write(decrypted_data)

            with zipfile.ZipFile(temp_zip, 'r') as zipf:
                zipf.extractall(output_dir)

            os.remove(temp_zip)
            
            self.update_progress(100)
            self.update_status("Decryption and Decompression Complete!")
            
            # Show success message in main thread
            self.master.after(0, self.show_success, "File decrypted and decompressed!")
        except Exception as e:
            # Show error message in main thread
            self.master.after(0, self.show_error, str(e))
        finally:
            # Reset UI in main thread
            self.master.after(0, self.reset_ui)

    def show_success(self, message):
        messagebox.showinfo("Success", message)

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def reset_ui(self):
        self.select_files_button.config(state='normal')
        self.remove_file_button.config(state='normal')
        self.compress_button.config(state='normal')
        self.decompress_button.config(state='normal')
        self.update_progress(0)
        self.update_status("Ready")

def main():
    root = tk.Tk()
    app = SecureCompressorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()