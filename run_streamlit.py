import streamlit.web.cli as stcli
import sys

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "streamlit_app.py", "--server.port=8501"]
    sys.exit(stcli.main())