from streamlit.testing.v1 import AppTest

at = AppTest.from_file("../main.py")
at.run(timeout=5)
assert not at.exception