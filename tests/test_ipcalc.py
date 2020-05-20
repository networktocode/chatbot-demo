from chatbot.ipcalc import ipcalc



def test_ipcalc_output():
    result = ipcalc("1.1.1.1/23")
    assert type(result) == str

