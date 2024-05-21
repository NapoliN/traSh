'''
tokenizer.pyをテストするモジュール
'''
from src.shell.tokenizer import tokenize, TokenType


def test_tokenize():
    input_ = "ls -l"
    tokens = tokenize(input_)
    assert len(tokens) == 2
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "ls"
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "-l"
    
def test_tokenize_with_redirectfile():
    input_ = "ls -l > out.txt"
    tokens = tokenize(input_)
    assert len(tokens) == 4
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "ls"
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "-l"
    assert tokens[2].type == TokenType.REDIRECT_FILE_OUT
    assert tokens[2].value == ">"
    assert tokens[3].type == TokenType.STRING
    assert tokens[3].value == "out.txt"
    
def test_tokenize_with_redirectchannel():
    input_ = "ls -l >> out.txt"
    tokens = tokenize(input_)
    assert len(tokens) == 4
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "ls"
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "-l"
    assert tokens[2].type == TokenType.REDIRECT_CHANNEL_OUT
    assert tokens[2].value == ">>"
    assert tokens[3].type == TokenType.STRING
    assert tokens[3].value == "out.txt"