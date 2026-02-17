import json

def set_default():
    with open('game_settings.json', 'r+') as file:
        settings = json.load(file)

        for key, value in settings.items():
            if key == '3':
                settings[key]['checked'] = True
            else:
                settings[key]['checked'] = False

        file.seek(0)
        file.truncate()
        json.dump(settings, file, indent=4)

if __name__ == '__main__':
    set_default()

