import os
import platform
import subprocess
import urllib.request
import tarfile
import zipfile
NODE_VERSION = "20.18.1"
NODE_DIST_URL = "https://nodejs.org/dist/v{}/".format(NODE_VERSION)
NODE_EXECUTABLE = "node"
def add_to_path(bin_path):
    os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
add_to_path(__file__)
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
    global NODE_EXECUTABLE
    node_path = download_node()
    extract_path = extract_node(node_path)
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if system == "windows":
        node_dir = "node-v{}-win-{}".format(NODE_VERSION, "x64" if arch.endswith("64") else "x86")
        node_executable = os.path.join(extract_path, node_dir, "node.exe")
        npm_executable = os.path.join(extract_path, node_dir, "npm.cmd")
    elif system == "darwin":
        node_dir = "node-v{}-darwin-{}".format(NODE_VERSION, "x64" if arch.endswith("64") else "arm64")
        node_executable = os.path.join(extract_path, node_dir, "bin", "node")
        npm_executable = os.path.join(extract_path, node_dir, "bin", "npm")
    else:
        node_dir = "node-v{}-linux-{}".format(NODE_VERSION, "x64" if arch.endswith("64") else "x86")
        node_executable = os.path.join(extract_path, node_dir, "bin", "node")
        npm_executable = os.path.join(extract_path, node_dir, "bin", "npm")

    add_to_path(os.path.dirname(node_executable))
    
    # Install dependencies
    if system == "windows":
        os.system(f"{npm_executable} install")
        os.chdir("Ultraviolet-Static")
        os.system(f"{npm_executable} install")
        os.chdir("..")
        os.system("start cmd /k python\python.exe lms.py")
    else:
        subprocess.run([npm_executable, "install"])
        os.chdir("Ultraviolet-Static")
        subprocess.run([npm_executable, "install"])
        os.chdir("..")
    
    run_script(node_executable)

if __name__ == "__main__":
    main()
