# Student Management App

A basic **CRUD-based Student Management web application** built with **Node.js, Express, EJS, and CSS**, backed by a **MySQL** database. The app supports core student management operations along with login/authentication.

This application was developed as a simple base project for practicing cloud deployment, containerization, CI/CD, automated testing, and orchestration workflows.

---

## Tech Stack

- **Backend:** Node.js, Express
- **Frontend:** EJS templates, CSS
- **Database:** MySQL
- **Testing:** Selenium (Python)
- **DevOps tooling:** Docker, Jenkins, Kubernetes (minikube)

---

## DevOps Implementation

The application is intentionally simple so that the focus can remain on implementing practical DevOps workflows around it. The project covers key stages of the deployment lifecycle, including cloud deployment, containerization, CI automation, automated testing, and Kubernetes orchestration.

### 1. Cloud Deployment (IaaS & PaaS)
- Deployed the application on **AWS EC2** (IaaS) — provisioned an Ubuntu instance, configured security groups, set up SSH access, installed and configured the required servers/dependencies, and got the app running end-to-end.
- Deployed the same application using **AWS Elastic Beanstalk** (PaaS) along with **Amazon RDS** for the database, to compare the IaaS vs PaaS deployment experience.
- Practiced configuring compute, storage, and managed database services on a public cloud platform.

### 2. Containerization & CI Automation
- Wrote a **`Dockerfile`** to containerize the web application.
- Wrote **`docker-compose.yml`** to orchestrate the app and database containers together, with a persistent volume attached to the database container so data survives container restarts.
- Set up **Jenkins** (running on EC2) with a **`Jenkinsfile`** pipeline that pulls the latest code from GitHub and builds/runs the app in containers automatically — an early CI workflow triggered by GitHub pushes.
- Added a separate **`docker-compose-jenkins.yml`** variant for the Jenkins-driven build environment (different ports/container names to avoid clashing with the standalone setup).

### 3. Automated Testing + CI Test Stage
- Wrote **Selenium test cases** (Python, headless Chrome) covering core app flows — see `assignment3_tests/`.
- Extended the Jenkins pipeline to add a **test stage**: on every GitHub push, Jenkins fetches the code, spins up the app in a container, runs the Selenium test suite against it, reports the test results and sends an email notification when the pipeline completes.

### 4. Kubernetes Deployment
- Wrote Kubernetes manifests (see `k8s/`) for both the web server and the database:
  - **Deployment + Service** pairs for each component.
  - **PersistentVolumeClaim** attached to the database deployment for persistent storage.
  - Services exposed as **NodePort**.
  - A **HorizontalPodAutoscaler** on top of the web server deployment for auto-scaling based on load.
- Deployed and tested the full stack on a **minikube** cluster running on an EC2 instance, and exposed both the application and the minikube dashboard externally via secure tunnels (ngrok) for evaluation.
