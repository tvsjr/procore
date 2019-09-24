This application was created at the request of Procore as a demonstration of
my programming capabilities.

main.py instantiates a web server, which responds to the following:
 - GET / - returns a usage summary
 - POST /password (password=ABC) - returns a base64-encoded SHA512 hash of the
   value in password
 - GET or POST /stats - returns a JSON object containing the number of hashes
   computed during the application run and the average time to complete
 - GET or POST /shutdown - conducts an orderly shutdown of the server, allowing
   pending requests to complete
   
Dependencies:
Ensure git, python3, curl, and virtualenv are installed

Usage:

Clone the GitHub repo (git clone https://www.github.com/tvsjr/procore)
In the project directory, build the virtual environment (virtualenv -p python3 venv)
Activate the virtual environment (source venv/bin/activate)
Run the server (python3 main.py)
