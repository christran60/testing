import os
from PIL import Image

def swap_colors_recursive(input_root, output_root, tolerance=15):
    """
    Recursively walks through input_root, converts white/black pixels,
    and mirrors the folder structure inside output_root.
    """
    # Target colors in RGB
    new_white = (252, 178, 1)   # #FCB201 (Persona Yellow/Gold)
    new_black = (148, 0, 11)    # #94000B (Persona Red)
    
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')

    # Walk through every folder and subfolder inside Assets
    for root, dirs, files in os.walk(input_root):
        for filename in files:
            if filename.lower().endswith(valid_extensions):
                # Full path to the original image
                img_path = os.path.join(root, filename)
                
                # Calculate the matching output folder path
                relative_path = os.path.relpath(root, input_root)
                target_folder = os.path.join(output_root, relative_path)
                
                # Create the matching subfolder structure if it doesn't exist yet
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                
                output_path = os.path.join(target_folder, filename)
                
                try:
                    with Image.open(img_path) as img:
                        orig_mode = img.mode
                        img = img.convert("RGBA")
                        data = img.getdata()
                        
                        new_data = []
                        for item in data:
                            r, g, b, a = item
                            
                            # Check for White
                            if (255 - r <= tolerance) and (255 - g <= tolerance) and (255 - b <= tolerance):
                                new_data.append((*new_white, a))
                                
                            # Check for Black
                            elif (r <= tolerance) and (g <= tolerance) and (b <= tolerance):
                                new_data.append((*new_black, a))
                                
                            else:
                                new_data.append(item)
                        
                        img.putdata(new_data)
                        
                        if orig_mode in ["RGB", "L"]:
                            img = img.convert("RGB")
                            
                        img.save(output_path)
                        print(f"Processed and saved to: {os.path.join(relative_path, filename)}")
                        
                except Exception as e:
                    print(f"Skipped {filename} due to error: {e}")

if __name__ == "__main__":
    # Based on your sidebar structure:
    # color_swap.py is in the root directory right next to the 'Assets' folder.
    INPUT_DIR = "Assets"
    OUTPUT_DIR = "Assets_Output"
    
    # 0 = exact match only. 15 helps catch anti-aliased edges in UI icons.
    TOLERANCE_LEVEL = 15 
    
    print("Starting color swap across all subfolders...")
    swap_colors_recursive(INPUT_DIR, OUTPUT_DIR, tolerance=TOLERANCE_LEVEL)
    print(f"\nDone! Check the new '{OUTPUT_DIR}' folder for your styled assets.")