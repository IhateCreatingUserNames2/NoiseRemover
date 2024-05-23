import tkinter as tk
from tkinter import filedialog
from scipy.io import wavfile
import torch
import torchaudio
from denoiser import pretrained


def select_file():
    filepath = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if filepath:
        entry.delete(0, tk.END)
        entry.insert(0, filepath)


def reduce_noise():
    filepath = entry.get()
    if filepath:
        rate, data = wavfile.read(filepath)

        # Convert numpy array to torch tensor
        data_tensor = torch.from_numpy(data).float()

        # Normalize the data to -1 to 1 range
        data_tensor = data_tensor / 32768.0

        # Load the pretrained denoiser model
        model = pretrained.dns64()

        # Apply noise reduction
        with torch.no_grad():
            denoised = model(data_tensor.unsqueeze(0)).squeeze(0).cpu()

        # Convert back to numpy array and denormalize
        denoised_data = (denoised.numpy() * 32768.0).astype('int16')

        output_filepath = "mywav_reduced_noise.wav"
        wavfile.write(output_filepath, rate, denoised_data)
        status_label.config(text=f"Noise reduction completed. Output saved as {output_filepath}")
    else:
        status_label.config(text="Please select a WAV file first.")


# Create main window
root = tk.Tk()
root.title("Noise Reduction")

# Create UI elements
label = tk.Label(root, text="Select WAV file:")
label.grid(row=0, column=0, padx=5, pady=5)

entry = tk.Entry(root, width=50)
entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

browse_button = tk.Button(root, text="Browse", command=select_file)
browse_button.grid(row=0, column=3, padx=5, pady=5)

reduce_button = tk.Button(root, text="Reduce Noise", command=reduce_noise)
reduce_button.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

status_label = tk.Label(root, text="")
status_label.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()
