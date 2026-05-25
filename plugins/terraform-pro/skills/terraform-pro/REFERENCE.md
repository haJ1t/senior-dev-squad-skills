# Terraform Pro — Reference

Full code samples, configuration blocks, command lists, and worked examples. Linked from [SKILL.md](SKILL.md).

---

## 1. Project Structure

```
infrastructure/
  environments/
    dev/
      main.tf
      variables.tf
      terraform.tfvars
      backend.tf
    staging/
    prod/
  modules/
    networking/
      main.tf
      variables.tf
      outputs.tf
    database/
    compute/
    monitoring/
  policies/              ← Sentinel / OPA
  scripts/
    plan.sh
    apply.sh
  .terraform-docs.yml
```

---

## 2. Module Design

```hcl
# modules/database/main.tf
variable "name" {
  description = "Database identifier"
  type        = string
}

variable "instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.medium"
}

variable "engine_version" {
  description = "PostgreSQL engine version"
  type        = string
  default     = "16.3"
}

variable "backup_retention_days" {
  description = "Days to retain backups"
  type        = number
  default     = 30
}

resource "aws_db_instance" "main" {
  identifier        = var.name
  engine            = "postgres"
  engine_version    = var.engine_version
  instance_class    = var.instance_class

  allocated_storage     = 100
  max_allocated_storage = 500
  storage_encrypted     = true
  storage_type          = "gp3"

  db_name  = var.name
  username = random_password.username.result
  password = random_password.password.result

  backup_retention_period = var.backup_retention_days
  backup_window           = "03:00-04:00"
  maintenance_window      = "sun:04:00-sun:05:00"

  deletion_protection = true
  skip_final_snapshot = false

  vpc_security_group_ids = [var.security_group_id]
  db_subnet_group_name   = var.subnet_group

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = {
    Name        = var.name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
```

---

## 3. Remote State

```hcl
# environments/prod/backend.tf
terraform {
  backend "s3" {
    bucket         = "org-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }

  required_version = ">= 1.7"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

---

## 4. Workspace Strategy

```bash
# Per-environment workspaces
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Conditional logic based on workspace
locals {
  environment = terraform.workspace
  instance_count = {
    dev     = 1
    staging = 2
    prod    = 5
  }[local.environment]
}
```

---

## 5. CI/CD for Terraform

```yaml
# .github/workflows/terraform.yml
name: Terraform
on:
  push:
    paths: ['infrastructure/**']
    branches: [main]
  pull_request:
    paths: ['infrastructure/**']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3

      - name: Terraform fmt
        run: terraform fmt -check -recursive

      - name: Terraform init
        run: terraform init
        working-directory: infrastructure/environments/dev

      - name: Terraform validate
        run: terraform validate
        working-directory: infrastructure/environments/dev

      - name: Security scan
        uses: tenable/terrascan-action@main
        with:
          iac_type: terraform
          iac_dir: infrastructure

  plan:
    needs: validate
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3

      - name: Terraform plan
        run: |
          terraform init
          terraform plan -out=tfplan
        working-directory: infrastructure/environments/staging
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Post plan to PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs')
            const plan = fs.readFileSync('tfplan.txt', 'utf8')
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Terraform Plan\n\`\`\`\n${plan}\n\`\`\``
            })

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: |
          terraform init
          terraform apply -auto-approve
        working-directory: infrastructure/environments/prod
```

---

## 6. Policy as Code (Sentinel)

```hcl
# policies/enforce_encryption.sentinel
import "tfplan/v2" as tfplan

main = rule {
  all tfplan.resource_changes as _, rc {
    rc.change.after.encrypted else true
  }
}
```

---

## 7. Security Scanning

```bash
# Terrascan — IaC security
terrascan scan -i terraform -d infrastructure/

# tfsec — Terraform-specific
tfsec infrastructure/

# Checkov — cloud security
checkov -d infrastructure/

# Infracost — cost estimation
infracost breakdown --path infrastructure/environments/prod
```
