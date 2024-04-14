import argparse

# サブコマンドと引数の定義
parser = argparse.ArgumentParser(description='Process some input')
parser.add_argument('command', type=str, help='Command')

parser_2 = parser.add_argument('--arg2',type=str)


# 入力を受け取る
input_string = input("Enter command and value: ")

# 入力をパース
args = parser.parse_args(input_string.split())

# -sの内容を表示
print(args.arg2)