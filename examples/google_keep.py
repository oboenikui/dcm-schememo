import sys
import time
import gkeepapi
import gpsoauth
from pathlib import Path
from dcm_schememo import parse_vcs_file
import webview

ics_path = str(Path(__file__).parent / "test_event.vcs")

# Google Keepにログイン
keep = gkeepapi.Keep()

# Create a webview window with the specified storage path
window = webview.create_window(
    'Google Login',
    'https://accounts.google.com/EmbeddedSetup',
)

oauth_token = None
email = None

def check_oauth_token():
    while True:
        cookies = window.get_cookies()
        for cookie in cookies:
            if 'oauth_token' in cookie:
                global oauth_token
                oauth_token = cookie['oauth_token'].value
                print("oauth_token cookie found:", oauth_token)
                window.destroy()
                return
        time.sleep(1)

# Start the webview and check for the oauth-token cookie
webview.start(check_oauth_token)

if oauth_token is None:
    print("oauth_tokenを取得できませんでした。")
    sys.exit(1)

# 標準入力でGoogleアカウントのメールアドレスを取得
email = input("ブラウザでログインしたGoogleアカウントのメールアドレスを入力してください: ")
android_id = "0123456789abcdef"  # Android IDは適当な値を指定

master_response = gpsoauth.exchange_token(email, oauth_token, android_id)
master_token = master_response['Token']  

# ブラウザでログインするためのトークンを取得
state = {}
keep.authenticate(email, master_token)
keep.sync()

notes = parse_vcs_file(ics_path)
Path("output").mkdir(exist_ok=True)

# memo_textsの内容をGoogle Keepに保存
for note in notes:
    try:
        keep.createNote(title=note.summary, text=note.description)
        keep.sync()
        if note.photo is not None:
            # 添付画像を保存
            image_path = Path("output") / f"{note.last_modified.strftime('%Y%m%d_%H%M%S')}.bin"
            with open(image_path, "wb") as image_file:
                image_file.write(note.photo)  # Updated to use note.photo instead of note[3]
            print(f"画像を保存しました: {image_path}")
            print("Google Keepの最新メッセージに画像を添付してください")
            print("続ける場合はEnterを押してください。")
            input()
    except Exception as e:
        print(f"メモの保存中にエラーが発生しました: {e}")

# Google Keepの変更を同期
try:
    keep.sync()
    print("Google Keepの変更を同期しました。")
except Exception as e:
    print(f"同期中にエラーが発生しました: {e}")