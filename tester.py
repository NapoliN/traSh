import sys
import selectors

def is_stdin_blocking():
    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ)
    
    events = sel.select(timeout=0)
    sel.unregister(sys.stdin)
    
    return not events  # eventsが空の場合はブロッキングしている

if is_stdin_blocking():
    print("sys.stdin.read() は現在ブロッキングしています")
else:
    print("sys.stdin.read() は現在ブロッキングしていません")

# 標準入力から読み取る（この操作はブロッキングする）
print("データを入力してください:")
data = sys.stdin.read()
print(f"読み取ったデータ: {data}")