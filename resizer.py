import tkinter as tk
from tkinter import messagebox
from PIL import Image
import os

# Function to resize the image
def scale_image(input_image_path, output_image_path, target_dimension, adjust_dimension, target_ppi=300):
    try:
        # Open the image file
        image = Image.open(input_image_path)

        # Get current width and height of the image
        current_width, current_height = image.size

        if adjust_dimension == 'Width':
            target_width_inches = target_dimension
            target_width_pixels = int(target_width_inches * target_ppi)
            scale_factor = target_width_pixels / current_width
            target_height_pixels = int(current_height * scale_factor)
            target_height_inches = target_height_pixels / target_ppi
        elif adjust_dimension == 'Height':
            target_height_inches = target_dimension
            target_height_pixels = int(target_height_inches * target_ppi)
            scale_factor = target_height_pixels / current_height
            target_width_pixels = int(current_width * scale_factor)
            target_width_inches = target_width_pixels / target_ppi

        # Resize the image using LANCZOS filter for best quality
        resized_image = image.resize((target_width_pixels, target_height_pixels), Image.LANCZOS)

        # Save the resized image with the correct DPI
        dpi = (target_ppi, target_ppi)
        resized_image.save(output_image_path, dpi=dpi)

        return f"Resized {os.path.basename(input_image_path)} successfully to {target_width_inches}x{target_height_inches} inches at {target_ppi} PPI."
    except Exception as e:
        return f"Error resizing {os.path.basename(input_image_path)}: {str(e)}"

# Function to handle button click for resizing images
def resize_images():
    try:
        target_dimension = float(entry_target_dimension.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid dimension.")
        return

    # Determine which dimension to adjust
    if var_adjust_dimension.get() == 1:
        adjust_dimension = 'Width'
    elif var_adjust_dimension.get() == 2:
        adjust_dimension = 'Height'
    else:
        messagebox.showerror("Error", "Please select a dimension to adjust.")
        return

    target_ppi = 300  # Desired PPI

    # Fixed paths for input and output folders
    input_folder = r"C:\Users\admin\Desktop\IN"
    output_folder = r"C:\Users\admin\Desktop\OUT"

    success_messages = []

    # Get a list of all PNG files in the input folder
    png_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]

    # Process each PNG file
    for png_file in png_files:
        input_path = os.path.join(input_folder, png_file)
        output_path = os.path.join(output_folder, png_file)

        # Resize the image
        success_message = scale_image(input_path, output_path, target_dimension, adjust_dimension, target_ppi)
        success_messages.append(success_message)

    # Show summary message box
    messagebox.showinfo("Operation Complete", "\n".join(success_messages))

    # Close the main window
    root.destroy()

# Create main application window
root = tk.Tk()
root.title("Image Resizer")

# Label for target dimension
label_target_dimension = tk.Label(root, text="Desired Output Dimension (inches):")
label_target_dimension.grid(row=0, column=0, padx=10, pady=5)

# Entry field for target dimension
entry_target_dimension = tk.Entry(root, width=20)
entry_target_dimension.grid(row=0, column=1, padx=10, pady=5)

# Radio buttons to choose dimension to adjust
var_adjust_dimension = tk.IntVar()

radio_width = tk.Radiobutton(root, text="Adjust Width", variable=var_adjust_dimension, value=1)
radio_width.grid(row=1, column=0, padx=10, pady=5, sticky='w')

radio_height = tk.Radiobutton(root, text="Adjust Height", variable=var_adjust_dimension, value=2)
radio_height.grid(row=2, column=0, padx=10, pady=5, sticky='w')

# Button to resize images
button_resize = tk.Button(root, text="Resize Images", command=resize_images)
button_resize.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

# Start the main tkinter event loop
root.mainloop()
