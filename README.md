# grbr
A link grabber and text summarizer app.

## Installation and Usage (Python)
- Clone the repository
  - `git clone git@github.com:jameshtwose/grbr.git`
  - `cd grbr`
- Install the requirements
  - `pip install -r requirements.txt`
- Run the app
  - `streamlit run app.py`

## Installation and Usage (Docker)
- Clone the repository
  - `git clone git@github.com:jameshtwose/grbr.git`
  - `cd grbr`
- Download and install Docker
  - https://docs.docker.com/get-docker/
- Build and run the app
  - `docker build -t grbr .`
  - `docker run -p 8501:8501 grbr`
  - Open http://localhost:8501 in your browser
  - To stop the app, press `Ctrl+C` in the terminal
  - To check the RAM/ storage used by Docker, run `docker stats`