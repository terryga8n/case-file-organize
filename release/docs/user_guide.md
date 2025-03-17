# Case File Organizer - User Guide

## Introduction
Case File Organizer is a powerful tool designed to help you organize files based on customizable patterns. It's particularly useful for managing case files, legal documents, and other structured data files.

## Features
- Pattern-based file organization
- Custom pattern management
- Year-based sorting and organization
- Automatic space fixing in filenames
- Backup before file operations
- Progress tracking
- Detailed logging

## Getting Started

### Installation
1. Download the latest release from the releases page
2. Extract the ZIP file to your desired location
3. Run `Case File Organizer.exe`

### Basic Usage
1. Launch the application
2. Select the directory containing files to organize
3. Choose a pattern from the dropdown list
4. Configure options as needed:
   - Create year folders
   - Sort by year
   - Backup before move
   - Fix spaces in filenames
5. Click "Organize Files" to start the process

### Managing Patterns

#### Adding a New Pattern
1. Click the "Add" button next to the pattern dropdown
2. Fill in the pattern details:
   - Name: A descriptive name for the pattern
   - Description: What this pattern is used for
   - Regex Pattern: The pattern to match filenames
   - Folder Format: How to name the target folder
3. Click "Save" to add the pattern

#### Editing a Pattern
1. Select the pattern from the dropdown
2. Click the "Edit" button
3. Modify the pattern details
4. Click "Save" to update the pattern

#### Deleting a Pattern
1. Select the pattern from the dropdown
2. Click the "Delete" button
3. Confirm the deletion

## Pattern Examples

### ACC Pattern
```
Regex: ACC(\d{4})-(\d{4})-(\d{4})
Folder Format: ACC {0}-{1}-{2}
```
This pattern matches files like "ACC1234-5678-9012.pdf" and organizes them into folders like "ACC 1234-5678-9012".

### HREPN Pattern
```
Regex: HREPN(\d{4})-(\d{4})-(\d{4})
Folder Format: HREPN {0}-{1}-{2}
```
This pattern matches files like "HREPN1234-5678-9012.pdf" and organizes them into folders like "HREPN 1234-5678-9012".

### HRER Pattern
```
Regex: HRER(\d{4})-(\d{4})-(\d{4})
Folder Format: HRER {0}-{1}-{2}
```
This pattern matches files like "HRER1234-5678-9012.pdf" and organizes them into folders like "HRER 1234-5678-9012".

## Options Explained

### Create Year Folders
When enabled, files will be organized into year-based subfolders within the pattern folder. This is useful for maintaining chronological organization.

### Sort by Year
When enabled, files will be sorted by year before being organized. The year is extracted from either the filename or the file's modification date.

### Backup Before Move
When enabled, a backup copy of each file will be created before moving it. This provides a safety net in case of errors during the organization process.

### Fix Spaces in Filenames
When enabled, extra spaces in filenames will be replaced with single spaces, making the filenames more consistent and easier to work with.

## Logging
The application maintains detailed logs of all operations. Logs are stored in the `logs` directory with timestamps in the filename. You can view the log in real-time in the application window.

## Troubleshooting

### Common Issues
1. **Pattern not matching files**
   - Check the regex pattern syntax
   - Verify the filename format matches the pattern
   - Use the log to see which files are being processed

2. **Files not being moved**
   - Check file permissions
   - Ensure the target directory is not read-only
   - Verify there's enough disk space

3. **Application not starting**
   - Check if all required files are present
   - Verify Python is installed correctly
   - Check the logs for error messages

### Getting Help
If you encounter issues:
1. Check the logs in the `logs` directory
2. Review the pattern configuration
3. Contact support with the log file and pattern details

## Best Practices
1. Always test patterns with a small set of files first
2. Enable "Backup before move" for safety
3. Review the logs after each operation
4. Keep patterns simple and well-documented
5. Regular backups of your configuration

## Support
For support, please:
1. Check the documentation
2. Review the logs
3. Contact support with:
   - Log file
   - Pattern configuration
   - Steps to reproduce the issue 