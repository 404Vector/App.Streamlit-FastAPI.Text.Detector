if __name__ == "__main__":
    import os
    address = "localhost"
    port = 30001
    os.system(f"streamlit run frontend/main.py --server.address {address} --server.port {port}")