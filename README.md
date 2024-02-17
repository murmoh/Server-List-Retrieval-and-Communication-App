# Server-List Retrieval and Communication App

This Python script, built with the Kivy framework, creates an application that not only retrieves a server list from a server but also enables users to join servers and communicate with others. The loading screen features engaging animations, a progress bar, and a label. As the application transitions to the main screen, users can interact with the server list, join servers, and engage in communication.

## Key Features:
- **Server Communication:** Establishes a connection to a server for real-time retrieval of the server list.
- **Interactive Server List:** The main screen displays the retrieved server list, allowing users to join servers and communicate with others.
- **Loading Screen Animation:** Engaging loading screen with a rotating image, custom label, and progress bar to enhance the user experience.

## Usage:
1. Ensure the server is running and accessible.
2. Run the script to start the application.
3. Loading screen animations and progress bar indicate ongoing server communication.
4. After a predefined duration, the application seamlessly transitions to the main screen, where users can join servers and communicate.

## Server Interaction:
- Customize the server IP and port in the script (`sys.argv`) to connect to your server.
- Users can join servers, communicate with others, and participate in real-time chat.

## Dependencies:
- **Kivy:** A Python framework for developing multi-touch applications.
- **Tkinter:** Used for creating the graphical user interface.
- **Socket:** Enables communication between the client and server.
- **Threading:** Implemented for handling concurrent tasks.

Feel free to customize the script to meet specific server communication requirements or enhance the user interface for a personalized touch.
