#Bricklink wanted list merge

## About
Just a simple python script that allows you to easily merge bricklink wanted lists together. It has a few options that allow you to modify the data in bulk before uploading it back to bricklink.

## Options
- `--add_extra <int>` - Add extra quantity to each item in bulk
- `--min_qty <int>` - Set the minimum number in bulk for each item
- `--path <str>` - Path where the xml files exist, default is current directory
- `--condition <str>` - Condition to set on each item in bulk, valid options are `N` for new and `U` for used
- `-h / --help` - Show help
