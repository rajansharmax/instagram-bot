import json
import os

def create_video_file_json():
    # Ask for user input for video name and path
    video_name = input("\033[33mEnter the video name: ")
    video_path = input("\033[33mEnter the video path: ")

    # Define the new video entry
    new_video = {
        "name": video_name,
        "path": video_path
    }

    # Specify the file path where the JSON will be saved
    json_file_path = "video_file.json"

    try:
        # Check if the JSON file already exists
        if os.path.exists(json_file_path):
            # If the file exists, open it and load the existing data
            with open(json_file_path, "r") as json_file:
                video_data = json.load(json_file)
        else:
            # If the file doesn't exist, start with an empty structure
            video_data = {"video_files": []}

        # Append the new video entry to the list of video files
        video_data["video_files"].append(new_video)

        # Write the updated data back to the JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(video_data, json_file, indent=4)

        print(f"\033[32mFile '{json_file_path}' updated successfully with new video data!")
    
    except Exception as e:
        print(f"\033[31mError occurred: {str(e)}")

# Example Usage
if __name__ == "__main__":
    create_video_file_json()
