# fusion_xacro2urdf2unity
This repository is cited from [xacro2urdf](https://github.com/doctorsrn/xacro2urdf). We write some scripts to help us quickly create URDF files for Unity from [fusion2urdf](https://github.com/syuntoku14/fusion2urdf).

# Usage
1. Prepare Your Folder:
The folder you specify must contain:
    - A `urdf` folder with the necessary URDF files and xacro file.
    - A `meshes` folder with the associated mesh files.
    - A `launch` folder if you have launch files to run.

2. Running the Script:
You have two choices to transform your files:

    - python version(Recommend)

    ```python
    python xacro2urdf.py /path/to/your/folder
    ```

    - sh script

    Put the script into the same folder of `urdf` folder. And then run the script.



