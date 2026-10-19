Microservice for managing restaurants and their menus: restaurant profiles, menu items, prices, and availability.

## CI/CD

A push to `main` deploys to staging, and an approved manual run deploys to prod
(`.github/workflows/ci-cd.yml`). The required GitHub secrets, how to retrieve
them with the Azure CLI, and how to manage the cluster with `kubectl` live on the
organization profile:
https://github.com/Cloud-Computing-FRI/.github

Two things are specific to this repository. The workflow logs in to Azure with
OIDC under the subject
`repo:Cloud-Computing-FRI/delivery-app-restaurants:environment:<staging|prod>`,
and in prod it reads `DATABASE_URL` from the pre-created `db-restaurants` Secret.
