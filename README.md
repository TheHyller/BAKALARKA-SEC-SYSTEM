# Security System Application

This project is a security system application built using Python and Kivy. It allows users to monitor and control a security system with features such as motion detection, image reception from cameras, and PIN-based system toggling.

## Project Structure

The project is organized into the following directories and files:

- **src/**: Contains the source code for the application.
  - **app.py**: Main application class that initializes the Kivy app and manages the UI.
  - **config.py**: Handles loading and saving configuration settings.
  - **network/**: Contains modules for network communication.
    - **discovery_listener.py**: Listens for discovery broadcasts.
    - **tcp_listener.py**: Handles incoming TCP connections for image data.
    - **udp_listener.py**: Listens for UDP broadcasts and status updates.
  - **ui/**: Contains modules for the user interface components.
    - **main_layout.py**: Defines the main layout and UI elements.
    - **popups.py**: Functions for displaying popups and messages.
  - **utils/**: Contains utility functions.
    - **helpers.py**: Includes helper functions for network operations.

- **config.json**: Configuration file for application settings.
- **requirements.txt**: Lists the dependencies required for the project.
- **README.md**: Documentation for the project.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd security-system-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/app.py
```

## Features

- Real-time monitoring of motion detection.
- Image reception from multiple cameras.
- User authentication via PIN code.
- Configurable system settings.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.