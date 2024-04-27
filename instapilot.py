# import

import datetime
import importlib.util
import json
import os
import subprocess
import sys
import threading
import time

import schedule
import tqdm

# req


class fg:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[39m"


def typewriter(message):
    for char in message:
        print(char, end="", flush=True)
        time.sleep(0.01)
    print()


package_names = ["instagrapi", "requests"]

InsPi = """
\033[32m
 .___                 __        __________.__.__          __
 |   | ____   _______/  |______ \______   \__|  |   _____/  |_
 |   |/    \ /  ___/\   __\__  \ |     ___/  |  |  /  _ \   __\
 |   |   |  \/___ \  |  |  / __ \|    |   |  |  |_(  <_> )  |
 |___|___|  /____  > |__| (____  /____|   |__|____/\____/|__|
          \/     \/            \/
 <------------------------------------------------------------>
 | GitHub : rajansharmax            |       MIT License    		|
 | Instagram Automated Python Tool  |        Instagrapi       |
 +------------------------------------------------------------+
"""

# installations & logo

time.sleep(1)
os.system("clear")
time.sleep(1)

typewriter(InsPi)

time.sleep(1)
print("\n\033[35m[+] Checking Requirements \n")
time.sleep(2)

for package_name in package_names:
    if importlib.util.find_spec(package_name):
        print(f"\n\033[32m[+] {package_name} Is Installed ;)\n")
    else:
        print(f"\n\033[31m[×] {package_name} Is Not Installed :/")
        try:
            print(f"\033[35m[+] Installing {package_name}")
            subprocess.run(
                ["pip3", "install", package_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            print(f"\033[32m[+] {package_name} Installed Successfully !\n")
            import instagrapi
            from instagrapi import Client
        except subprocess.CalledProcessError:
            print("\033[31m Please Install Packages Manually")
            sys.exit(1)

import instagrapi
from instagrapi import Client

cl = Client()

time.sleep(1)
os.system("clear")
print(InsPi)
time.sleep(1)


def load_last_user_details():
    try:
        with open("last_user.json", "r") as f:
            data = json.load(f)
            return data.get("accounts", [])
    except FileNotFoundError:
        return []


# Function to save last used login details
def save_last_user_details(username, password):
    try:
        with open("last_user.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"accounts": []}

    # Check if the account already exists in the list
    updated_accounts = [
        {"username": user["username"], "password": user["password"]}
        for user in data["accounts"]
    ]

    if {"username": username, "password": password} not in updated_accounts:
        updated_accounts.append({"username": username, "password": password})

    with open("last_user.json", "w") as f:
        json.dump({"accounts": updated_accounts}, f, indent=4)


def load_captions_details():
    try:
        with open("captions.json", "r") as f:
            data = json.load(f)
            return data["captions"]
    except FileNotFoundError:
        return None, None


def load_videos_paths():
    try:
        with open("videos_path.json", "r") as f:
            data = json.load(f)
            return data["videos_path"]
    except FileNotFoundError:
        return None, None


def load_usernames():
    try:
        with open("usernames.json", "r") as f:
            data = json.load(f)
            return data["usernames"]
    except FileNotFoundError:
        return None, None


def startSleepLoader(seconds):
    for _ in range(seconds):
        print(".", end="", flush=True)
        time.sleep(1)


# process

# Main script logic
print("\n[+] Login")

# Prompt to load last user details
use_last_details = input("\nLoad last user details (y/n): ").strip().lower()

if use_last_details == "y":
    # Load and display list of accounts
    accounts = load_last_user_details()

    if accounts:
        print("\n[+] Accounts with last login details:")
        for idx, account in enumerate(accounts):
            print(f"{idx + 1}. {account['username']}")

        # Prompt user to select an account
        account_choice = input("\nSelect account by number: ").strip()

        try:
            selected_index = int(account_choice) - 1
            if 0 <= selected_index < len(accounts):
                usr = accounts[selected_index]["username"]
                pas = accounts[selected_index]["password"]
                print(f"\n[+] Using last login details for {usr}")
            else:
                usr = input("\nusername: ")
                pas = input("password: ")
        except ValueError:
            usr = input("\nusername: ")
            pas = input("password: ")
    else:
        usr = input("\nusername: ")
        pas = input("password: ")
else:
    usr = input("\nusername: ")
    pas = input("password: ")

try:
    cl.login(usr, pas)
    print("\n\033[32m [+] Login Successful !")
    save_last_user_details(usr, pas)  # Save login details if successful
except instagrapi.exceptions.BadPassword:
    print("\n\033[31m [+] Please Check Your Password !")
    sys.exit()
except instagrapi.exceptions.RateLimitError:
    print("\n\033[31m [+] Too Many Login Attempts, Please Try Later !")
    sys.exit()
except instagrapi.exceptions.PleaseWaitFewMinutes:
    print("\n\033[31m [+] Please Try After Few Minutes !")
    sys.exit()
except instagrapi.exceptions.ClientConnectionError:
    print("\n\033[31m [+] Please Check You Internet Connection !")
    sys.exit()
except instagrapi.exceptions.ChallengeUnknownStep:
    print("\n\033[31m [+] Instagram Needs Phone Number Verification !")
    sys.exit()
except instagrapi.exceptions.ProxyAddressIsBlocked:
    print("\n\033[31m [+] Instagram Has Blocked Your IP Address, Use Proxy To Bypass !")
except KeyboardInterrupt:
    print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
    sys.exit()


def conexit():
    con = input("\n\033[34m Do You Want To Continue (Y/n) : ")

    if con == "Y" or con == "y":
        time.sleep(1)
        os.system("clear")
        Main()
    else:
        cne = "\n\033[32m [+] Thank You For Using !!"
        typewriter(cne)


def follow(username):
    try:
        x = username
        try:
            y = cl.user_id_from_username(x)
            cl.user_follow(y)
            print("\n\033[36m User Followed !")
        except Exception as e:
            print("\n\033[31m Error" + e)
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()


def follow_user_list(usernames):
    try:
        user_id = [cl.user_id_from_username(user) for user in usernames]
        print(f"\n\033[36m Total Users : {len(user_id)}")
        print("\n\033[36m Trying To Follow Users...")

        for usertof in user_id:
            try:
                print(f"\n\033[36m Trying To Follow User : {usertof}")
                cl.user_follow(usertof)
                print(" User Followed !")
                startSleepLoader(30)
            except instagrapi.exceptions.UserNotFound:
                print("\n\033[31m User Not Found !")
            except instagrapi.exceptions.ClientNotFoundError:
                print("\n\033[31m Client Not Found !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()


def follow_user_listv2(usernames):
    try:
        print(f"\n\033[36m Total Users : {len(usernames)}")
        print(f"\n\033[36m Trying To Follow Users...")

        for username in usernames:
            try:
                user_id = cl.user_id_from_username(username)
                cl.user_follow(user_id)
                print(f"\n\033[32m User Followed : {username}")
                startSleepLoader(60)
            except Exception as e:
                print(f"\n\033[31m Error : {e}")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()


def unfollow_user_list(usernames):
    try:
        user_id = [cl.user_id_from_username(user) for user in usernames]
        print(f"\n\033[36m Total Users : {len(user_id)}")
        print("\n\033[36m Trying To Follow Users...")

        for usertof in user_id:
            try:
                print(f"\n\033[36m Trying To UnFollow User : {usertof}")
                cl.user_unfollow(usertof)
                print(" User UnFollowed !")
                startSleepLoader(30)
            except instagrapi.exceptions.UserNotFound:
                print("\n\033[31m User Not Found !")
            except instagrapi.exceptions.ClientNotFoundError:
                print("\n\033[31m Client Not Found !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()


def unfollow_user_listv2(usernames):
    try:
        print(f"\n\033[36m Total Users : {len(usernames)}")
        print(f"\n\033[36m Trying To UnFollow Users...")

        for username in usernames:
            try:
                user_id = cl.user_id_from_username(username)
                cl.user_unfollow(user_id)
                print(f"\n\033[32m User unFollowed : {username}")
                startSleepLoader(60)
            except Exception as e:
                print(f"\n\033[31m Error : {e}")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()


def unfollow_user(target):
    try:
        unfollow_user_id = cl.user_id_from_username(target)
        try:
            print(f"\n\033[36m Trying To Unfollow User : {unfollow_user_id}")
            cl.user_unfollow(unfollow_user_id)
            print(" User Unfollowed !")
        except instagrapi.exceptions.UserNotFound:
            print("\n\033[31m User Not Found !")
        except instagrapi.exceptions.ClientNotFoundError:
            print("\n\033[31m Client Not Found !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()


def remove_follower(target):
    try:
        user_id = cl.user_id_from_username(target)
        try:
            print(f"\n\033[36m Trying To Remove Follower : {user_id}")
            cl.user_remove_follower(user_id)
            print(" Follower Removed !")
        except instagrapi.exceptions.UserNotFound:
            print("\033[31m User Not Found !")
        except instagrapi.exceptions.ClientNotFoundError:
            print("\n\033[31m Client Not Found !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()


def remove_all_followers():
    try:
        user_id = cl.user_id_from_username(usr)
        print("\n\033[36m Fetching Info... ('This May Take Time') ! \n")
        followers = cl.user_followers(user_id)
        followers_ids = list(followers.keys())

        for f_to_removed in followers_ids:
            try:
                print(f"\n\033[36m Trying To Remove Followers : {f_to_removed}")
                cl.user_remove_follower(f_to_removed)
                print(" Follower Removed !")
            except instagrapi.exceptions.UserNotFound:
                print("\033[31m User Not Found !")
            except instagrapi.exceptions.ClientNotFoundError:
                print("\n\033[31m Client Not Found !")
            except instagrapi.exceptions.PleaseWaitFewMinutes:
                print("\n\033[31m Please Try Again After Few Minutes !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()


def unfollow_all_user():
    try:
        user_id = cl.user_id_from_username(usr)
        print("\n\033[36m Fetching Info... ('This May Take Time') ! \n")
        followings = cl.user_following(user_id)
        followings_ids = list(followings.keys())

        for u_to_unfollow in followings_ids:
            try:
                print(f"\n\033[36m Trying To Unfollow User : {u_to_unfollow}")
                cl.user_unfollow(u_to_unfollow)
                print(" User Unfollowed !")
                startSleepLoader(60)
            except instagrapi.exceptions.UserNotFound:
                print("\033[31m User Not Found !")
            except instagrapi.exceptions.ClientNotFoundError:
                print("\n\033[31m Client Not Found !")
            except instagrapi.exceptions.PleaseWaitFewMinutes:
                print("\n\033[31m Please Try Again After Few Minutes !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()


def follow_user_following(target):
    try:
        user_id = cl.user_id_from_username(target)
        followings = cl.user_following(user_id)
        followings_ids = list(followings.keys())

        for u_to_follow in followings_ids:
            try:
                print(f"\n\033[36m Trying To Follow User : {u_to_follow}")
                cl.user_follow(u_to_follow)
                print(" User Followed !")
            except instagrapi.exceptions.UserNotFound:
                print("\033[31m User Not Found !")
            except instagrapi.exceptions.PleaseWaitFewMinutes:
                print("\n\033[31m Please Try Again After Few Minutes !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()
    except instagrapi.exceptions.UserNotFound:
        print("\n\033[31m User Not Found !")


def follow_user_followers(target):
    try:
        user_id = cl.user_id_from_username(target)
        followers = cl.user_followers(user_id)
        followers_ids = list(followers.keys())

        for u_to_follow in followers_ids:
            try:
                print(f"\n\033[36m Trying To Follow User : {u_to_follow}")
                cl.user_follow(u_to_follow)
                print("User Followed !")
            except instagrapi.exceptions.UserNotFound:
                print("\033[31m User Not Found !")
            except instagrapi.exceptions.PleaseWaitFewMinutes:
                print("\n\033[31m Please Try Again After Few Minutes !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()
    except instagrapi.exceptions.UserNotFound:
        print("\n\033[31m User Not Found !")


def get_user_id_from_username(target):
    try:
        user_id = cl.user_id_from_username(target)
        print(f"\n\033[36m User_Id : {user_id}")
    except instagrapi.exceptions.UserNotFound:
        print("\033[31m User Not Found !")
    except instagrapi.exceptions.PleaseWaitFewMinutes:
        print("\n\033[31m Please Try Again After Few Minutes !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()
    except instagrapi.exceptions.UserNotFound:
        print("\n\033[31m User Not Found !")


def get_username_from_user_id(target):
    try:
        username = cl.username_from_user_id(target)
        print(f"\n\033[36m Username : {username}")
    except instagrapi.exceptions.UserNotFound:
        print("\033[31m User Not Found !")
    except instagrapi.exceptions.PleaseWaitFewMinutes:
        print("\n\033[31m Please Try Again After Few Minutes !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()
    except instagrapi.exceptions.UserNotFound:
        print("\n\033[31m User Not Found !")


def user_following_into_list(target):
    try:
        print("\n\033[36m Fetching Info... ('This May Take Time') !")
        user_id = cl.user_id_from_username(target)
        followings = cl.user_following(user_id)
        followings_ids = list(followings.keys())
        followings_username = []

        for usernames in followings_ids:
            try:
                username = cl.username_from_user_id(usernames)
                followings_username.append(username)
            except instagrapi.exceptions.UserNotFound:
                print("\033[31m User Not Found !")

        filename = f"{user_id}_following.txt"

        with open(filename, "w") as file:
            for user_names in followings_username:
                file.write(username + "\n")

        print(f"\n\033[36m File Saved As : {filename}")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def user_followers_into_list(target):
    try:
        print("\n\033[36m Fetching Info... ('This May Take Time') !")
        user_id = cl.user_id_from_username(target)
        followers = cl.user_followers(user_id)
        followers_ids = list(followers.keys())
        followers_username = []

        for usernames in followers_ids:
            try:
                username = cl.username_from_user_id(usernames)
                followers_username.append(username)
            except instagrapi.exceptions.UserNotFound:
                print("\033[31m User Not Found !")

        filename = f"{user_id}_followers.txt"

        with open(filename, "w") as file:
            for user_names in followers_username:
                file.write(user_names + "\n")

        print(f"\n\033[36m File Saved As : {filename}")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def like_media(url):
    try:
        media_id = cl.media_pk_from_url(url)
        cl.media_like(media_id)
        print(f"\n\033[36m Media Liked !")
    except instagrapi.exceptions.MediaError:
        print("\n\033[31m Media Error Received From Instagram")
    except instagrapi.exceptions.MediaNotFound:
        print("\n\033[31m Media Not Found !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()


def like_all_media(target):
    try:
        user_id = cl.user_id_from_username(target)
        media_list = cl.user_medias(user_id)
        media_pk = []

        for media in media_list:
            media_pk.append(media.pk)

        for media_x in media_pk:
            try:
                print(f"\n\033[36m Media : {media_x}")
                cl.media_like(media_x)
                print(" Status : Liked !")
            except instagrapi.exceptions.MediaError:
                print("\033[31m Status : Not Liked !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def unlike_media(url):
    try:
        media_id = cl.media_pk_from_url(url)
        cl.media_unlike(media_id)
        print(f"\n\033[36m Media Unliked !")
    except instagrapi.exceptions.MediaError:
        print("\n\033[31m Media Error Received From Instagram")
    except instagrapi.exceptions.MediaNotFound:
        print("\n\033[31m Media Not Found !")
    except KeyboardInterrupt:
        print("\n\033[31m [+] Keyboard Interrupt : Script Ended !")
        sys.exit()


def unlike_all_media(target):
    try:
        user_id = cl.user_id_from_username(target)
        media_list = cl.user_medias(user_id)
        media_pk = []

        for media in media_list:
            media_pk.append(media.pk)

        for media_x in media_pk:
            try:
                print(f"\n\033[36m Media : {media_x}")
                cl.media_unlike(media_x)
                print(" Status : Unliked !")
            except instagrapi.exceptions.MediaError:
                print("\033[31m Status : Not Unliked !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def download_post(url):
    try:
        media_id = cl.media_pk_from_url(url)
        path = "saved_media/"
        try:
            print(f"\n\033[36m Downloading Media : {media_id}")
            post = cl.photo_download(media_id, path)
            print(" Status : Media Downloaded !")
        except instagrapi.exceptions.MediaError:
            print("\033[31m Status : Media Not Downloaded !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def download_reel(url):
    try:
        media_id = cl.media_pk_from_url(url)
        path = "saved_media/"
        try:
            print(f"\n\033[36m Downloading Media : {media_id}")
            post = cl.clip_download(media_id, path)
            print(" Status : Media Downloaded !")
        except instagrapi.exceptions.MediaError:
            print("\033[31m Status : Media Not Downloaded !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def download_video(url):
    try:
        media_id = cl.media_pk_from_url(url)
        path = "saved_media/"
        try:
            print(f"\n\033[36m Downloading Media : {media_id}")
            post = cl.video_download(media_id, path)
            print(" Status : Media Downloaded !")
        except instagrapi.exceptions.MediaError:
            print("\033[31m Status : Media Not Downloaded !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def upload_post(Path, Caption):
    try:
        try:
            print(f"\n\033[36m Uploading Media...")
            cl.photo_upload(path=Path, caption=Caption)
            print(f" Status : Uploaded !")
        except instagrapi.exceptions.MediaError:
            print(f"\n\033[31m Status : Media Not Uploaded !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def upload_reel(Path, Caption):
    try:
        try:
            print(f"\n\033[36m Uploading Media...")
            cl.clip_upload(path=Path, caption=Caption)
            print(f" Status : Uploaded !")
        except instagrapi.exceptions.MediaError:
            print("\n\033[31m Status : Media Not Uploaded !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def upload_reel_multi(paths, caption):
    try:
        paths_list = paths.split(",")
        for path in paths_list:
            try:
                print(f"\n\033[36m Uploading Media...")
                cl.clip_upload(path=path.strip(), caption=caption)
                print(f" Status : Uploaded !")
            except instagrapi.exceptions.MediaError:
                print("\n\033[31m Status : Media Not Uploaded !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def upload_video(Path, Caption):
    try:
        try:
            print(f"\n\033[36m Uploading Media...")
            cl.video_upload(path=Path, caption=Caption)
            print(f" Status : Uploaded !")
        except instagrapi.exceptions.MediaError:
            print("\n\033[31m Status : Media Not Uploaded !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def upload_reel_job(path, caption):
    try:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\r\033[36mCurrent Time: {current_time}", end="")
        print(f" Uploading Media from path: {path}")
        # Assuming 'cl' is your instagrapi client
        cl.clip_upload(path=path, caption=caption, thumbnail=path + ".jpg")
        print(f" Status: Uploaded !")
    except instagrapi.exceptions.MediaError:
        print("\n\033[31mStatus: Media Not Uploaded !")


def schedule_video_uploads(paths, captions, upload_interval_minutes):
    index = 0

    while True:
        # Get the current video path and caption
        path = paths[index]
        caption = captions[index]

        # Start a new thread to upload the current video
        thread = threading.Thread(target=upload_reel_job, args=(path, caption))
        thread.start()

        # Move to the next video (circular list)
        index = (index + 1) % len(paths)

        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\r\033[36mCurrent Time: {current_time}", end="")
        # Sleep for the upload interval (1 minute) before scheduling the next video
        time.sleep(upload_interval_minutes * 60)


def upload_reel_multi_time(paths_input, caption_input, upload_interval_minutes_str):
    try:
        paths = []
        captions = []
        upload_interval_minutes = int(upload_interval_minutes_str)

        # Process paths_input (either from file or manual input)
        if paths_input.lower() == "file":
            # Load video paths from a JSON file
            with open("./videos_path.json", "r") as file:
                data = json.load(file)
                if "videos_path" in data:
                    paths = data["videos_path"]
        else:
            # Manual input of comma-separated video URLs
            paths = paths_input.split(",")

        # Process caption_input (either from file or manual input)
        if caption_input.lower() == "file":
            # Load captions from a file (assuming it's a JSON file with a "captions" list)
            with open("./captions.json", "r") as file:
                captions_data = json.load(file)
                if "captions" in captions_data:
                    captions = [item["text"] for item in captions_data["captions"]]
        else:
            # Manual input of a single caption to be used for all videos
            caption = caption_input
            captions = [caption] * len(paths)  # Use the same caption for all videos

        # Validate paths and captions
        if not paths:
            print("\n\033[31mError: No video paths found.")
            return
        if not captions:
            print("\n\033[31mError: No captions found.")
            return

        # Start scheduling video uploads
        schedule_video_uploads(paths, captions, upload_interval_minutes)

    except Exception as e:
        print(f"\n\033[31mError: {str(e)}")


def repostViralReels(viralReelKey, timeToPostInterval):
    try:
        cl.repost_viral_reels(
            viral_reel_id=viralReelKey, time_to_post_interval=timeToPostInterval
        )
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def delete_media(url):
    try:
        media_id = cl.media_pk_from_url(url)
        try:
            print(f"\n\033[36m Deleting Media : {media_id}")
            cl.media_delete(media_id)
            print(" Status : Deleted !")
        except instagrapi.exceptions.MediaError:
            print("\n\033[31m Status : Media Not Uploaded !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def mass_delete_media():
    try:
        user_id = cl.user_id_from_username()
        media_list = cl.user_medias(user_id)
        media_pk = []

        for media in media_pk:
            media_pk.append(media.pk)

        for media_d in media_pk:
            try:
                print(f"\n\033[36m Deleting Media : {media_d}")
                cl.media_delete(media_d)
                print(" Status : Deleted !")
            except instagrapi.exceptions.MediaError:
                print("\n\033[31m Status : Media Not Uploaded !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def media_info(url):
    try:
        media_id = cl.media_pk_from_url(url)
        media_info = cl.media_info(media_id)
        info = f"""\033[36m
 Username : {media_info.user.username}
 Name : {media_info.user.full_name}
 Comments : {media_info.comment_count}
 Likes : {media_info.like_count}
 Caption : {media_info.caption_text}
 Views : {media_info.view_count}
 Duration : {media_info.video_duration}"""
        print(info)
    except Exception as e:
        print(f"\n\033[31m Error : {str(e)}")


def comment(url, comment):
    try:
        media_id = cl.media_pk_from_url(url)
        print(f"\n\033[36m Comment : {comment}")
        cl.media_comment(media_id, comment)
        print(" Status : Done !")
    except Exception as e:
        print(f"\n\033[31m Error : {str(str)}")


def help():
    url = "https://bit.ly/TnYtCoder"
    command = ["am", "start", "-a", "android.intent.action.VIEW", "-d", url]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


time.sleep(1)
os.system("clear")


def Main():
    print(InsPi)
    time.sleep(0.1)
    options = """\033[33m
 ·————————————————————————————————————·————————————————————————————————————·
 │ [1] Follow User                    │ [21] Upload Reel                   │
 │ [2] Follow/Unfollow User From List │ [22] Upload Video                  │
 │ [3] Unfollow User                  │ [23] Delete Media                  │
 │ [4] Remove Follower                │ [24] Mass Media Delete             │
 │ [5] Remove All Followers           │ [25] Media Information             │
 │ [6] Unfollow All User              │ [26] Comment                       │
 │ [7] Follow User Following          │ [27] Upload Multiple Rell          │
 │ [8] Follow User Followers          │ [28] Upload Multiple reel on Time  │
 │ [9] Get User Id From Username      │ [29] Follow/Unfollow User V2       │
 │ [10] Get Username From User Id     │ [30] Find Viral Video Repost       │
 │ [11] User Following Into List      │                                    │
 │ [12] User Followers Into List      │                                    │
 │ [13] Like Media                    │                                    │
 │ [14] Like All Media                │                                    │
 │ [15] Unlike Media                  │                                    │
 │ [16] Unlike All Media              │                                    │
 │ [17] Download Post                 │                                    │
 │ [18] Download Reel                 │                                    │
 │ [19] Download Video                │                                    │
 │ [20] Upload Post                   │                                    │
 ·————————————————————————————————————·—————————————————————————————————————
 │            \033[31m[00] Exit               \033[33m│              [99] Help             │
 ·——————————————————————————————————————————————————————————————————————————
	"""
    print(options)
    opt = int(input("\033[35m Your Option : "))
    if opt == 1:
        followuser = input("\n\033[33m username : ")
        flu = follow(followuser)
        conexit()

    elif opt == 2:
        followuserlist = input("\nLoad last user details (y/n): ").strip().lower()

        if followuserlist == "y":
            followuserlist = load_usernames()

            followOrUnfollow = (
                input("\nFollow users or Unfollow users (f/u): ").strip().lower()
            )

            if followOrUnfollow == "f":
                ful = follow_user_list(followuserlist)
                conexit()
            else:
                ful = unfollow_user_list(followuserlist)
                conexit()

        else:
            followuserlist = input("\n\033[33m enter usernames in comman separated : ")
            ful = follow_user_list(followuserlist)
            conexit()

    elif opt == 3:
        unfollowuser = input("\n\033[33m username : ")
        uu = unfollow_user(unfollowuser)
        conexit()

    elif opt == 4:
        rmfollowersuser = input("\n\033[33m username : ")
        rfu = remove_follower(rmfollowersuser)
        conexit()

    elif opt == 5:
        remove_all_followers()
        conexit()

    elif opt == 6:
        unfollow_all_user()
        conexit()

    elif opt == 7:
        target = input("\n\033[33m username : ")
        fuf = follow_user_following(target)
        conexit()

    elif opt == 8:
        target = input("\n\033[33m username : ")
        fufs = follow_user_followers(target)
        conexit()

    elif opt == 9:
        target = input("\n\033[33m username : ")
        guifu = get_user_id_from_username(target)
        conexit()

    elif opt == 10:
        target = input("\n\033[33m user id : ")
        gufui = get_username_from_user_id(target)
        conexit()

    elif opt == 11:
        target = input("\n\033[33m username : ")
        ufil = user_following_into_list(target)
        conexit()

    elif opt == 12:
        target = input("\n\033[33m username : ")
        ufil = user_followers_into_list(target)
        conexit()

    elif opt == 13:
        target = input("\n\033[33m url : ")
        lm = like_media(target)
        conexit()

    elif opt == 14:
        target = input("\n\033[33m username : ")
        lam = like_all_media(target)
        conexit()

    elif opt == 15:
        target = input("\n\033[33m url: ")
        um = unlike_media(target)
        conexit()

    elif opt == 16:
        target = input("\n\033[33m username : ")
        ual = unlike_all_media(target)
        conexit()

    elif opt == 17:
        target = input("\n\033[33m url : ")
        dp = download_post(target)
        conexit()

    elif opt == 18:
        target = input("\n\033[33m url : ")
        dr = download_reel(target)
        conexit()

    elif opt == 19:
        target = input("\n\033[33m url : ")
        dv = download_video(target)
        conexit()

    elif opt == 20:
        path = input("\n\033[33m path : ")
        caption = input(" caption : ")
        up = upload_post(path, caption)
        conexit()

    elif opt == 21:
        path = input("\n\033[33m path : ")
        caption = input(" caption : ")
        ur = upload_reel(path, caption)
        conexit()

    elif opt == 22:
        path = input("\n\033[33m path : ")
        caption = input(" caption : ")
        uv = upload_video(path, caption)
        conexit()

    elif opt == 23:
        url = input("\n\033[33m url : ")
        dm = delete_media(url)
        conexit()

    elif opt == 24:
        mass_delete_media()
        conexit()

    elif opt == 25:
        url = input("\n\033[33m url : ")
        mi = media_info(url)
        conexit()

    elif opt == 26:
        url = input("\n\033[33m url : ")
        comment = input(" comment : ")
        c = comment(url, comment)
        conexit()

    elif opt == 27:
        paths = input("\n\033[33m Enter comma-separated video URLs: ")
        caption = input("\n\033[33m Enter caption: ")
        urm = upload_reel_multi(paths, caption)
        conexit()

    # elif opt == 28:
    # 	paths = input("\n\033[33m Enter comma-separated video URLs: ")
    # 	caption = input("\n\033[33m Enter caption: ")
    # 	urmt = upload_reel_multi_time(paths, caption)
    # 	conexit()

    elif opt == 28:
        paths_input_option = input(
            "\n\033[33m Use video paths from file? (file/manual): "
        )
        caption_input_option = input(
            "\n\033[33m Use captions from file? (file/manual): "
        )
        upload_time = input("\n\033[33m Enter upload time in minutes: ")
        if caption_input_option.lower() == "manual":
            caption_text = input("\n\033[33m Enter caption to use for all videos: ")
            upload_reel_multi_time(paths_input_option, caption_text, upload_time)
        else:
            upload_reel_multi_time(
                paths_input_option, caption_input_option, upload_time
            )
        conexit()

    elif opt == 29:
        followuserlist = input("\nLoad last user details (y/n): ").strip().lower()

        if followuserlist == "y":
            followuserlist = load_usernames()

            followOrUnfollow = (
                input("\nFollow users or Unfollow users (f/u): ").strip().lower()
            )

            if followOrUnfollow == "f":
                ful = follow_user_listv2(followuserlist)
                conexit()
            else:
                ful = unfollow_user_listv2(followuserlist)
                conexit()

    elif opt == 30:
        # repost viral reels
        viralReelKey = input("\n\033[33m Enter your Viral Reel Key: ")
        timeToPostInterval = input(
            "\n\033[33m Enter time to post interval in minutes: "
        )
        repostViralReels(viralReelKey, timeToPostInterval)
        conexit()

    elif opt == 00:
        time.sleep(0.5)
        exit = "\n\033[32m [+] Thank You For Using !!"
        typewriter(exit)

    elif opt == 99:
        help()
        conexit()

    else:
        print("\n\033[31m Wrong Options")
        time.sleep(3)
        os.system("clear")
        Main()


Main()

cl.logout()
# ending
