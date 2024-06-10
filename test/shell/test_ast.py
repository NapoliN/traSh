from src.shell.ast_ import ASTBuilder, NodeCommand, NodeRedirect, NodePipe
from src.shell.tokenizer import tokenize


ast_builder = ASTBuilder()

def test_cmd_with_no_arg():
    tokens = tokenize("ls")
    ast = ast_builder.build_ast(tokens)
    assert type(ast) == NodeCommand
    assert ast.cmd == "ls"
    
def test_cmd_with_args():
    tokens = tokenize("ls -l")
    ast = ast_builder.build_ast(tokens)
    assert type(ast) == NodeCommand
    assert ast.cmd == "ls"
    assert ast.args == ["-l"]
    
def test_cmd_with_multiple_args():
    tokens = tokenize("ls -l -a")
    ast = ast_builder.build_ast(tokens)
    assert type(ast) == NodeCommand
    assert ast.cmd == "ls"
    assert ast.args == ["-l", "-a"]
    
def test_cmd_with_redirect():
    tokens = tokenize("ls -l > out.txt")
    ast = ast_builder.build_ast(tokens)
    assert type(ast) == NodeCommand
    assert ast.cmd == "ls"
    assert ast.args == ["-l"]
    assert ast.redirects is not None
    assert ast.redirects[0].type_ == NodeRedirect.Type.Out
    assert ast.redirects[0].fname == "out.txt"
    
def test_cmd_with_multiple_redirect():
    tokens = tokenize("ls -a -l < in.txt > out.txt")
    ast = ast_builder.build_ast(tokens)
    assert type(ast) == NodeCommand
    assert ast.cmd == "ls"
    assert ast.args == ["-a", "-l"]
    assert ast.redirects is not None
    assert ast.redirects[0].type_ == NodeRedirect.Type.In
    assert ast.redirects[0].fname == "in.txt"
    assert ast.redirects[1].type_ == NodeRedirect.Type.Out
    assert ast.redirects[1].fname == "out.txt"
    
def test_cmd_with_pipe():
    tokens = tokenize("ls -l | grep test")
    ast = ast_builder.build_ast(tokens)
    assert type(ast) == NodePipe
    left,right = ast.left, ast.right
    assert type(left) == NodeCommand
    assert type(right) == NodeCommand
    assert left.cmd == "ls"
    assert left.args == ["-l"]
    assert right.cmd == "grep"
    assert right.args == ["test"]
    
def test_cmd_with_pipe_and_redirect():
    tokens = tokenize("ls -l | grep test > out.txt")
    ast = ast_builder.build_ast(tokens)
    assert type(ast) == NodePipe
    left,right = ast.left, ast.right
    assert type(left) == NodeCommand
    assert type(right) == NodeCommand
    assert left.cmd == "ls"
    assert left.args == ["-l"]
    assert right.cmd == "grep"
    assert right.args == ["test"]
    assert right.redirects is not None
    assert right.redirects[0].type_ == NodeRedirect.Type.Out
    assert right.redirects[0].fname == "out.txt"
    
def test_cmd_with_redirect_and_pipe():
    tokens = tokenize("ls -l > out.txt | grep test")
    ast = ast_builder.build_ast(tokens)
    assert type(ast) == NodePipe
    left,right = ast.left, ast.right
    assert type(left) == NodeCommand
    assert type(right) == NodeCommand
    assert left.cmd == "ls"
    assert left.args == ["-l"]
    assert left.redirects is not None
    assert left.redirects[0].type_ == NodeRedirect.Type.Out
    assert left.redirects[0].fname == "out.txt"
    assert right.cmd == "grep"
    assert right.args == ["test"]

def test_cmd_with_multiple_redirect_and_pipe():
    tokens = tokenize("ls -l < in.txt > out.txt | grep test")
    ast = ast_builder.build_ast(tokens)
    assert type(ast) == NodePipe
    left,right = ast.left, ast.right
    assert type(left) == NodeCommand
    assert type(right) == NodeCommand
    assert left.cmd == "ls"
    assert left.args == ["-l"]
    assert left.redirects is not None
    assert left.redirects[0].type_ == NodeRedirect.Type.In
    assert left.redirects[0].fname == "in.txt"
    assert left.redirects[1].type_ == NodeRedirect.Type.Out
    assert left.redirects[1].fname == "out.txt"
    assert right.cmd == "grep"
    assert right.args == ["test"]
    
def test_cmd_with_multiple_pipe():
    tokens = tokenize("ls -l | grep test | wc -l")
    ast = ast_builder.build_ast(tokens)
    assert type(ast) == NodePipe
    left,right = ast.left, ast.right
    assert type(left) == NodeCommand
    assert type(right) == NodePipe
    rleft, rright = right.left, right.right
    assert type(rleft) == NodeCommand
    assert type(rright) == NodeCommand
    assert left.cmd == "ls"
    assert left.args == ["-l"]
    assert rleft.cmd == "grep"
    assert rleft.args == ["test"]
    assert rright.cmd == "wc"
    assert rright.args == ["-l"]
    