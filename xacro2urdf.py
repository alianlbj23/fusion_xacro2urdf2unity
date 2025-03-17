import os
import re
import shutil
import urllib.request
import subprocess
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Convert xacro file to URDF and prepare files for Unity."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=os.getcwd(),
        help="Path to the folder containing the 'urdf' folder (default: current directory)."
    )
    args = parser.parse_args()

    # 切換到指定的工作目錄
    os.chdir(args.path)

    # Check if the urdf folder exists
    if not os.path.exists("urdf"):
        sys.stderr.write("Error, the 'urdf' folder doesn't exist. Please place this script into the same folder as the 'urdf' folder.\n")
        sys.exit(1)

    # Get the parent directory name (xxx_description)
    robot_mesh = os.path.basename(os.getcwd())

    # Set robot_name by removing '_description' from robot_mesh
    robot_name = robot_mesh.replace("_description", "")

    # Check if the urdf/<robot_name>.xacro file exists
    xacro_file = os.path.join("urdf", f"{robot_name}.xacro")
    if not os.path.exists(xacro_file):
        sys.stderr.write(f"Error, the '{xacro_file}' file doesn't exist.\n")
        sys.exit(1)

    # Download xacro.py only if it doesn't exist
    xacro_script = "xacro.py"
    if not os.path.exists(xacro_script):
        url = "https://raw.githubusercontent.com/doctorsrn/xacro2urdf/master/xacro.py"
        urllib.request.urlretrieve(url, xacro_script)

    # Create directories and copy meshes
    urdf_mesh_dir = os.path.join("urdf", robot_mesh, "meshes")
    os.makedirs(urdf_mesh_dir, exist_ok=True)
    if os.path.exists("meshes"):
        shutil.copytree("meshes", urdf_mesh_dir, dirs_exist_ok=True)

    # Create a temporary xacro file omitting any .gazebo includes.
    temp_xacro_file = xacro_file + ".temp"
    with open(xacro_file, "r", encoding="utf-8") as f:
        content = f.read()
    # Replace any xacro include line that references a .gazebo file with a comment.
    content = re.sub(r'<xacro:include\b[^>]*\.gazebo[^>]*>', '<!-- omitted .gazebo include -->', content)
    with open(temp_xacro_file, "w", encoding="utf-8") as f:
        f.write(content)

    # Run xacro.py to generate the URDF file using the temporary file
    urdf_output = f"{robot_name}.urdf"
    subprocess.run(["python", xacro_script, "-o", urdf_output, temp_xacro_file])

    # Optionally, remove the temporary file after processing.
    os.remove(temp_xacro_file)

    # --- Update URDF mesh file references ---
    # Convert any file:// absolute paths to use package://<robot_mesh>/meshes/...
    with open(urdf_output, "r", encoding="utf-8") as f:
        urdf_data = f.read()
    # This regex will replace the substring starting with 'file://' up to '/meshes'
    urdf_data = re.sub(r'file://.*?[/\\]meshes', f'package://{robot_mesh}/meshes', urdf_data)
    with open(urdf_output, "w", encoding="utf-8") as f:
        f.write(urdf_data)
    # --- End Update ---

    # Overwrite output directory if it exists
    output_dir = f"{robot_name}_to_unity"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    shutil.move(urdf_output, output_dir)
    shutil.move(os.path.join("urdf", robot_mesh), output_dir)

    print(f"Success. Your files are ready in the folder '{output_dir}'.")

if __name__ == "__main__":
    main()