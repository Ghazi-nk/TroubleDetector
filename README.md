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