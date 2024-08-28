import os
import json

def export_video_paths(directory_path, output_file):
    videos_path = []

    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory.")
        return

    # Iterate over files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Check if the file is a video (you can add more video extensions if needed)
        if os.path.isfile(file_path) and filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            videos_path.append(file_path)

    # Prepare dictionary to export as JSON
    data = {"videos_path": videos_path}

    # Write the data to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)
    
    print(f"Exported video paths to '{output_file}' successfully.")

# Specify the directory path containing video files
videos_directory = "/home/rajansharmax/Documents/Reels/2d_animation/2d_animation"

# Specify the output JSON file path
output_json_file = "videos_path2.json"

# Call the function to export video paths to JSON
export_video_paths(videos_directory, output_json_file)
