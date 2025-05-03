from streamlit.testing.v1 import AppTest

at = AppTest.from_file("../main.py")
at.run(timeout=15)
assert not at.exception