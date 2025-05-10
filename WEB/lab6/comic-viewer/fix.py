import json
import os

# Root directory of your manga content
root_dir = 'manga_store\\contents'

# Walk through all manga directories
for manga_dir in os.listdir(root_dir):
    manga_path = os.path.join(root_dir, manga_dir)

    # Only process directories
    if os.path.isdir(manga_path):
        info_json_path = os.path.join(manga_path, 'info.json')

        # Check if info.json exists in the directory
        if os.path.isfile(info_json_path):
            try:
                # Load the info.json
                with open(info_json_path, 'r', encoding='utf-8') as info_file:
                    info_data = json.load(info_file)

                # Update the img_path key with the new path
                # img_path = os.path.join(manga_path, 'img.webp')
                # info_data['img_path'] = img_path

                # Save the modified info.json back
                with open(info_json_path, 'w', encoding='utf-8') as info_file:
                    json.dump(info_data, info_file, ensure_ascii=False, indent=4)

                print(f"✅ Updated img_path for {manga_dir}")

            except json.JSONDecodeError:
                print(f"⚠️ Error reading JSON in: {info_json_path}")
        else:
            print(f"⚠️ info.json not found in: {manga_path}")

print("✅ All manga directories processed!")
