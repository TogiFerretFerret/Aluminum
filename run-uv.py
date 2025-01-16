import os
import platform
import subprocess
import urllib.request
import tarfile
import zipfile

NODE_VERSION = "20.18.1"
NODE_DIST_URL = "https://nodejs.org/dist/v{}/".format(NODE_VERSION)
NODE_EXECUTABLE = "node"
def download_node():
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if system == "windows":
        node_filename = "node-v{}-win-{}.zip".format(NODE_VERSION, "x64" if arch.endswith("64") else "x86")
    elif system == "darwin":
        node_filename = "node-v{}-darwin-{}.tar.gz".format(NODE_VERSION, "x64" if arch.endswith("64") else "x86")
    else:
        node_filename = "node-v{}-linux-{}.tar.xz".format(NODE_VERSION, "x64" if arch.endswith("64") else "x86")

    node_url = NODE_DIST_URL + node_filename
    node_path = os.path.join(os.getcwd(), node_filename)

    print("Downloading Node.js from:", node_url)
    urllib.request.urlretrieve(node_url, node_path)
    print("Downloaded to:", node_path)

    return node_path
def extract_node(node_path):
    extract_path = os.path.join(os.getcwd(), "node")
    if node_path.endswith(".zip"):
        with zipfile.ZipFile(node_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    else:
        with tarfile.open(node_path, 'r:*') as tar_ref:
            tar_ref.extractall(extract_path)
    # Remove the downloaded file
    os.remove(node_path)
    print("Extracted to:", extract_path)
    return extract_path
def run_script(node_executable):
    script_path = os.path.join(os.getcwd(), "src", "index.js")
    subprocess.run([node_executable, script_path])

def main():
    global node_executable
    node_path = download_node()
    extract_path = extract_node(node_path)
    system = platform.system().lower()
    arch = platform.machine().lower()
    if system == "windows":
        node_filename = "node-v{}-win-{}".format(NODE_VERSION, "x64" if arch.endswith("64") else "x86")
    elif system == "darwin":
        node_filename = "node-v{}-darwin-{}".format(NODE_VERSION, "x64" if arch.endswith("64") else "arm64")
    else:
        node_filename = "node-v{}-linux-{}".format(NODE_VERSION, "x64" if arch.endswith("64") else "x86")
    if platform.system().lower() == "windows":
        node_executable = os.path.join(extract_path, node_filename, "node.exe")
        os.system(os.path.join(extract_path, node_filename, "npm")+" install")
        os.chdir("Ultraviolet-Static")
        os.system(os.path.join("..",extract_path, node_filename, "npm")+" install")
        os.chdir("..")
        # Instll the depencencies in ultraviolet-static
    else:
        node_executable = os.path.join(extract_path, node_filename,"bin", "node")
        subprocess.run([os.path.join(extract_path, node_filename, "bin", "npm"), "install"])
        os.chdir("Ultraviolet-Static")
        subprocess.run([os.path.join("..",extract_path, node_filename, "bin", "npm"), "install"])
        os.chdir("..")
    # Install the dependencies
    
    run_script(node_executable)

if __name__ == "__main__":
    main()
