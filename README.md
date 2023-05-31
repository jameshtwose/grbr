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
  - `docker run -p 8080:8080 grbr`
  - Open http://localhost:8501 in your browser
  - To stop the app, press `Ctrl+C` in the terminal
  - To check the RAM/ storage used by Docker, run `docker stats`

## Build and deploy instructions (terraform-gcp)
- Install [Terraform](https://www.terraform.io/downloads.html)
- Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- `cd terraform_gcp_deploy`
- get credentials .json file from GCP if you don't have it already
  - https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/getting_started#adding-credentials
  - https://cloud.google.com/docs/authentication/getting-started
- put credentials .json file in `terraform_gcp_deploy` folder
- `terraform init`
- `terraform plan`
- `terraform fmt`
- `terraform apply`
- `gcloud init` (if you haven't already)
- `gcloud app deploy`
- `terraform destroy` (when you're done)