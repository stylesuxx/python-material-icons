import os
import shutil
import tempfile
import subprocess

REPO_URL = "https://github.com/google/material-design-icons.git"
ICON_DIR = os.path.join(os.path.dirname(__file__), "..", "material_icons", "icons")


def main():
    os.makedirs(ICON_DIR, exist_ok=True)

    tmpdir = tempfile.mkdtemp()
    print("Cloning Material Icons (src only)...")
    subprocess.run(["git", "clone", "--depth=1", "--filter=blob:none", "--sparse", REPO_URL, tmpdir], check=True)

    # Configure sparse checkout to only include src directory
    subprocess.run(["git", "-C", tmpdir, "sparse-checkout", "set", "src"], check=True)
    subprocess.run(["git", "-C", tmpdir, "sparse-checkout", "reapply"], check=True)

    root = os.path.join(tmpdir, "src")

    # Mapping from directory names to clean style names
    style_mapping = {
        'materialiconsoutlined': 'outlined',
        'materialiconsround': 'round',
        'materialiconssharp': 'sharp'
    }

    # copy all SVGs into consolidated structure
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn == "24px.svg":  # Only process 24px.svg files
                full_path = os.path.join(dirpath, fn)

                # Parse the path: /src/$CATEGORY/$NAME/$STYLE/24px.svg
                path_parts = os.path.relpath(dirpath, root).split(os.sep)

                if len(path_parts) >= 3:
                    name = path_parts[1]
                    style_dir_name = path_parts[2].lower()

                    # Only process the styles we want
                    if style_dir_name in style_mapping:
                        clean_style = style_mapping[style_dir_name]

                        # Create target structure: /icons/$STYLE/$NAME.svg
                        target_style_dir = os.path.join(ICON_DIR, clean_style)
                        os.makedirs(target_style_dir, exist_ok=True)

                        target_path = os.path.join(target_style_dir, f"{name}.svg")
                        shutil.copy2(full_path, target_path)

    shutil.rmtree(tmpdir)
    print("Icons downloaded into:", ICON_DIR)


if __name__ == "__main__":
    main()
