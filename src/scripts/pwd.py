'''pwd:     現在のチャンネルを出力します'''

from src.shell.environment import Environment

def pwd():
    env = Environment()
    print(env.current_channel_name)
    
if __name__ == "__main__":
    pwd()