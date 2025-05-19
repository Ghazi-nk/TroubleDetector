# TroubleDetector
welcome to the TroubleDetector project! This project is designed to help developers identify and fix issues in their code by leveraging the power of Semgrep, OpenAI, and Telegram.
## Goal
The goal of this project is to create a Telegram bot that can analyze GitHub repositories for potential issues using Semgrep and provide suggestions for fixes using OpenAI's GPT-4o model. The bot will also send notifications to the user via Telegram.

## Features
- Telegram bot that can receive GitHub repository names and analyze them for potential issues.
- Integration with Semgrep to scan the code for potential issues.
- Integration with OpenAI's GPT-4o model to provide suggestions for fixes.
- Notifications sent to the user via Telegram.
- GitHub Actions workflow to build and push the Docker image to GitHub Container Registry.

## 🚀 Project Flow
### main Workflow


1. **github workflow**
    - GitHub workflow is triggered by a push to the main branch.
    - it will build the docker image and push it to the ghcr.io registry.
    - it will also run a semgrep scan on the code and create a report.
2. **runing main.py**
    - the main.py file will be run in a docker container.
    - it will use the semgrep report to create a summary of the code quality and send it to the admin user via telegram.
   
3. **User Interaction**
   - Any user can send a GitHub repository name to the Telegram Bot.
   - The bot will trigger the folowing flow:
     1. clone repo into project folder
     2. run semgrep scan on the project folder
     3. create a report in the reports folder
     4. create a summary of the report (to exception caused by big request)
     5. get OpenAi response using the report summary and the fixed service prompt
     6. send the response to the user via telegram

#### notes:
- min. 1 pod in argocd muss zu sehen sein (greift auf local kubernetes cluster)
- wechsel auf github workflows
- telegram muss humorvolle message erhalten
- renovate integration! (github) 
- funktionsfähige pipeline (gitlab ci) und pods (argocd)

#### Präsentation:
- Produkt pitch (5 min)
- Code Review (5 min)
  - Argocd
  - kubernetes
  - gitlab ci
##### url to renovate:
https://developer.mend.io/github/Ghazi-nk/TroubleDetector 

---
### Notes:
#### get Argocd and cluster running:
Setup:
1. create arcod namespace:
```bash
kubectl create namespace argocd
```
2. install arocd in cluster:
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
3. then you can apply argocd:
```bash
kubectl apply -n argocd -f k8s/argocd-app.yaml
```
4. then redirect the argocd server to localhost:
```bash
kubectl port-forward svc/argocd-server -n argocd 8088:443
```
5. get the password (user name is "admin"):
```bash
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}")))
```
6. Add secret Key to cluster:
```powershell
$GHCRUsername = "ghazi-nk"
$GHCRToken = "your_personal_access_token" 
kubectl create secret docker-registry ghcr-secret `
  --docker-server=ghcr.io `
  --docker-username=$GHCRUsername `
  --docker-password=$GHCRToken `
  --namespace=default
```
7. consider adding the troubledetector-secret.yaml to the cluster:
```bash
kubectl apply -f k8s/troubledetector-secret.yaml
```
---
#### Run semgrep-scan on docker
pull, check the image and login to semgrep
```powershell
docker pull semgrep/semgrep
docker run --rm semgrep/semgrep semgrep --version
docker run -it semgrep/semgrep semgrep login
```
run image to scan project under app/project and create report under app/reports
```powershell
docker run --rm `
  -v "$(pwd)\app\project:/src" `
  -v "$(pwd)\app\reports:/reports" `
  semgrep/semgrep semgrep scan --config auto --json --output /reports/report.json
