# Installing
1. Download MP4Box --> https://gpac.io/downloads/
2. Install all packages --> conda env create -f matrox.yml

# Preparing GCP
1. Have a project with {PROJECT_ID} setup as well as a billing account
2. Have gcloud CLI installed
3. Enable Cloud Vision API and Vision AI API in GCP project
4. Set project ID: gcloud config set project {PROJECT_ID}
5. Authenticate yourself: gcloud auth application-default login