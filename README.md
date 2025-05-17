### Next steps:
* (register gitlab runner in kubernetes https://docs.gitlab.com/runner/install/kubernetes/

### Setup and start gitlab runner
* add repo:
```bash
helm repo add gitlab https://charts.gitlab.io
```
* add values.yaml and update the values.yaml:
  - gitlabUrl: https://gitlab.rz.htw-berlin.de/
  - runnerRegistrationToken: <your-gitlab-runner-registration-token>
  - rbac: { create: true }
* start runner:
```bash 
helm install --generate-name -f values.yaml gitlab/gitlab-runner
```


## 🚀 Project Flow

1. **User Interaction**
   - User sends a GitHub repository URL to the Telegram Bot.

2. **Pipeline Trigger**
   - The Telegram Bot triggers a GitLab CI/CD pipeline, passing the repository URL.

3. **GitLab Pipeline Tasks**
   - Clones the specified repository.
   - Runs a **SonarQube** analysis using the **SonarScanner CLI**.
   - Sends the analysis results to a running **SonarQube server**.
   - Once the analysis is complete, the pipeline sends a request to an **AI Summary Service**.

4. **AI Summary Service Tasks**
   - Fetches the **SonarQube report**.
   - Uses the **OpenAI API** to generate a short summary of key findings and suggestions.

5. **User Notification**
   - The **Telegram Bot** receives the summary and sends it back to the user.

#### notes:
- min. 1 pod in argocd muss zu sehen sein (greift auf local kubernetes cluster)
- wechsel auf github workflows
- telegram muss humorvolle message erhalten
- renovate integration! (github) 
- funktionsfähige pipeline (gitlab ci) und pods (argocd)
#### Präsentation:
- Krankheit -> 
  - 2. Prüfungszeitraum
  - einfach machen!
- Produkt pitch (5 min)
- Code Review (5 min)
  - Argocd
  - kubernetes
  - gitlab ci


### Notes:
#### Argocd runnen:
Setup:
1. create arcod namespace:
```bash
kubectl create namespace argocd
```
2. install arocd in cluster:
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
then you can apply argocd:
```bash
kubctl apply -n argocd -f argocd-app.yaml
```
then redirect the argocd server to localhost:
```bash
kubectl port-forward svc/argocd-server -n argocd 8088:443
```
get the password (user name is "admin"):
```bash
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}")))
```
