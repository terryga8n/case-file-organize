# Case File Organizer

A powerful file organization tool designed to help manage and organize case files efficiently.

## Features

- Organize files based on customizable patterns
- Create year-based folder structures
- Automatic file backup before moving
- Progress tracking with cancel option
- Detailed logging of all operations
- User-friendly graphical interface
- Pattern management system
- Space fixing in filenames

## Installation

### Prerequisites

- Python 3.8 or later
- pip (Python package installer)

### Quick Installation

1. Download or clone this repository
2. Run the `install.bat` script
3. Follow the on-screen instructions

### Manual Installation

If you prefer to install manually:

1. Ensure Python 3.8 or later is installed
2. Open a terminal in the project directory
3. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. If using a virtual environment, activate it:
   ```bash
   venv\Scripts\activate
   ```
2. Run the application:
   ```bash
   python src/case_file_organizer.py
   ```

### Building the Executable

1. If using a virtual environment, activate it:
   ```bash
   venv\Scripts\activate
   ```
2. Run the build script:
   ```bash
   build.bat
   ```
3. The executable will be created in the `dist` folder

## Configuration

The application uses a JSON configuration file (`file_patterns.json`) to store:
- File patterns
- Folder naming rules
- Default settings

### Default Patterns

- ACC: Accident case files
- HREPN: Human rights enforcement case files
- HRER: Human rights enforcement report files

## Development

### Project Structure

```
Case File Organizer/
├── src/
│   ├── core/
│   │   ├── config_manager.py
│   │   └── pattern_manager.py
│   ├── gui/
│   │   └── progress_window.py
│   ├── utils/
│   │   ├── logger.py
│   │   └── file_utils.py
│   └── case_file_organizer.py
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── build.bat
├── install.bat
└── requirements.txt
```

### Running Tests

Run the test suite using:
```bash
run_tests.bat
```

## Troubleshooting

Common issues and solutions:

1. **Python not found**
   - Ensure Python is installed and added to PATH
   - Check Python version with `python --version`

2. **Installation fails**
   - Check internet connection
   - Ensure pip is up to date
   - Try running as administrator

3. **Application won't start**
   - Verify all dependencies are installed
   - Check the logs in the `logs` directory

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For support, please:
1. Check the documentation in the `docs` directory
2. Review the troubleshooting section
3. Submit an issue on the repository 