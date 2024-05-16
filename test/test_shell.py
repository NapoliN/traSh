from src.shell import ShellEmulator



def test_ShellEmulator():
    shell = ShellEmulator()
    assert shell.prompt == '>>> '
    assert shell.conjqueue == []
    assert shell.accept == True
    assert shell.stream == None
    assert shell.fstream == None
    