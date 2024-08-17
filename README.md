# Shortlinks

Shortlinks is a self-hostable URL shortener built using Python. It's a self-contained package that can be easily installed via PyPI and run on your local machine or deployed on a server. This lightweight and efficient tool allows you to create and manage shortened URLs with custom expiration times.

## Features

- Create shortened URLs quickly and easily
- Set custom expiration times for links (30 seconds, 60 seconds, 3 minutes, or never expire)
- Self-hosted solution for better privacy and control
- Simple and intuitive web interface
- Fast and efficient redirection

## Requirements

- Python 3.7+
- pip (Python package manager)

## Installation

Shortlinks is available on PyPI and can be installed with pip:

```
pip install shortlinks
```

This command will install Shortlinks and all its dependencies.

## Usage

To run the Shortlinks server, simply use the following command:

```
shortlinks run
```

By default, the server will run on `http://localhost:8000`.

Open your web browser and go to `http://localhost:8000` to access the Shortlinks interface.

## Configuration (Optional)

You can customize the host and port by passing arguments when running the server:

```
shortlinks run
```

This will run the server on all available network interfaces on port 5000.

## Using Shortlinks

1. Enter the long URL you want to shorten in the input field.
2. Select an expiration time from the dropdown menu.
3. Click the "Generate" button to create a shortened URL.
4. Copy the shortened URL and share it as needed.

## Deployment

To deploy Shortlinks on a server:

1. Install Shortlinks on your server using pip.
2. Run the Shortlinks server using the `shortlinks run` command.
3. Set up a reverse proxy (e.g., Nginx or Apache) to forward requests to the Shortlinks application.
4. Configure your firewall to allow traffic on the desired port.
5. (Optional) Set up SSL/TLS for secure connections.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For more information or support, please open an issue on the GitHub repository.
