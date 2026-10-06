
# Object Shuffler

<img width="382" height="635" alt="Screenshot_25" src="https://github.com/user-attachments/assets/759fd674-d96c-48f4-b0a1-52f2bc93fe8a" />

Blender add-on for quickly selecting, replacing, and randomizing scene objects.

## Requirements

- Blender 5.1+

## Features

- Select Similar by cleaned object name
- Replace selected objects with a chosen object
- Replace selected objects with random objects from a collection
- Random Keep by percentage
- Random Rotation on X, Y, and Z axes
- Random Scale with uniform or per-axis controls

## Installation

1. Download the latest release ZIP.
2. In Blender, open **Edit → Preferences → Add-ons → Install...**
3. Select the ZIP file.
4. Enable **Object Shuffler**.
5. Open the 3D View sidebar with **N** and use the **Shuffler** tab.

## Usage

### Object Selection
Select an object and press **Select Similar**. Objects are matched by their cleaned base name, so names such as `Cube.001`, `Cube.002` and `Cube` are treated as the same base name.

### Universal Replace
Choose either an object or a collection as the replacement source, then press **Replace Objects**.

### Random Keep
Set **Keep %** and press **Random Keep**. The add-on keeps a randomly selected subset of the currently selected objects.

### Random Rotation
Enable the axes you want to randomize and press **Apply Rotation**.

### Random Scale
Set the minimum and maximum scale. Use **Uniform XYZ** for proportional scaling, or disable it to control X/Y/Z independently.

## License

GPL-3.0. See [LICENSE](LICENSE).

## Version

1.3.0
