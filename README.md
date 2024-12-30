# HeadNav

**HeadNav** is an advanced head-tracking system that enables users to control their mouse cursor with head movements, providing a hands-free interaction method. The project leverages Mediapipe for facial landmark detection and PyAutoGUI for mouse control.

## Features

- **Head Tracking**: Tracks head movements using a webcam.
- **Mouse Control**: Moves the mouse cursor based on head position.
- **Precision & Smoothing**: Includes smoothing algorithms to eliminate jitter and ensure smooth operation.
- **Dead Zone**: Prevents unintended movements when the head is in its initial position.
- **Customizable Sensitivity**: Adjustable sensitivity for fine or broad movements.
- **Real-Time Debugging**: Displays movement deltas for debugging purposes.

---

## Installation

### Prerequisites

1. Python 3.7 or above installed on your system.
2. A webcam (configured for index `1` in the code).
3. A system with GPU support for optimal performance.

### Steps to Install and Run Locally

1. **Clone the Repository**
   Open a terminal and run:
   ```bash
   git clone https://github.com/Subho4531/HeadNav.git
   cd HeadNav
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv headnav-env
   source headnav-env/bin/activate  # On Windows: headnav-env\Scripts\activate
   ```

3. **Install Dependencies**
   Use the following command to install required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Program**
   Execute the program with:
   ```bash
   python headnav.py
   ```

5. **Using the Application**
   - Ensure your webcam is functional.
   - Sit with your head in the center position for calibration.
   - Move your head left, right, up, or down to control the cursor.
   - The system will adjust cursor movement based on the sensitivity settings in the code.

---

## How It Works

- The **nose tip** landmark is used as the reference for tracking head position.
- Movements are scaled and mapped to screen dimensions for precise control.
- Adjust the `sensitivity`, `dead_zone`, and `smoothing_factor` variables in the script to suit your needs.

---

## Troubleshooting

- **Jittery Movements**: Adjust the `smoothing_factor` to a higher value.
- **No Mouse Movement**: Ensure the webcam is active and the index (`1`) matches your camera device.
- **Unexpected Movements**: Re-calibrate by restarting the program with your head centered.

---

## Contributions

Contributions are welcome! Feel free to fork the repository, create a branch, and submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Enjoy hands-free mouse control with **HeadNav**! Let us know if you encounter any issues or have suggestions for improvements.

