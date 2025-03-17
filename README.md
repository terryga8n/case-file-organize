# Case File Organizer

A powerful and flexible file organization tool that helps you manage files based on customizable patterns. Perfect for organizing case files, legal documents, and other structured data files.

## Features

- **Pattern-based Organization**: Create and use custom patterns to organize files
- **Year-based Sorting**: Organize files by year automatically
- **Space Fixing**: Automatically fix spaces in filenames
- **Backup Support**: Create backups before moving files
- **Progress Tracking**: Monitor file organization progress
- **Detailed Logging**: Comprehensive logging of all operations
- **User-friendly Interface**: Simple and intuitive GUI

## Installation

### For End Users
1. Download the latest release from the releases page
2. Extract the ZIP file to your desired location
3. Run `Case File Organizer.exe`

### For Developers
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/case-file-organizer.git
   cd case-file-organizer
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python src/case_file_organizer.py
   ```

## Usage

1. Launch the application
2. Select the directory containing files to organize
3. Choose a pattern from the dropdown list
4. Configure options as needed
5. Click "Organize Files" to start the process

For detailed usage instructions, see the [User Guide](docs/user_guide.md).

## Project Structure

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
├── docs/
│   └── user_guide.md
├── tests/
│   ├── unit/
│   └── integration/
├── README.md
├── LICENSE
├── requirements.txt
├── case_file_organizer.spec
└── build.bat
```

## Building from Source

1. Ensure you have Python 3.8 or later installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the build script:
   ```bash
   build.bat
   ```

The executable will be created in the `dist` directory, and a release package will be created in the root directory.

## Logging

Logs are stored in the `logs` directory with timestamps in the filename. The application maintains detailed logs of:
- File operations
- Pattern matching
- Error messages
- Processing statistics

## Error Handling

The application includes robust error handling for:
- File permission issues
- Disk space problems
- Pattern matching errors
- Invalid configurations

## Support

For support:
1. Check the [User Guide](docs/user_guide.md)
2. Review the logs in the `logs` directory
3. Contact support with:
   - Log file
   - Pattern configuration
   - Steps to reproduce the issue

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Version History

### v1.0.0
- Initial release
- Basic pattern-based file organization
- Year-based sorting and organization
- Space fixing in filenames
- Backup support
- Progress tracking
- Detailed logging 