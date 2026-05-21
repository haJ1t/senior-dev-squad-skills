---
name: terraform-pro
description: "Terraform modules, remote state, workspaces, CI/CD for IaC, security scanning. Use when writing or reviewing Terraform infrastructure code."
---

# Terraform Pro

## Purpose

Manage infrastructure as code at production scale. Covers module design, remote state, workspaces, CI/CD pipelines, policy as code, and security scanning.

## When to Use

**Use this when:**
- Designing or refactoring Terraform module structure for a multi-environment setup
- Setting up remote state with locking or migrating from local to remote backends
- Adding a Terraform CI/CD pipeline with plan-on-PR and apply-on-merge gates

**Use this ESPECIALLY when:**
- Multiple engineers are applying Terraform manually without state locking — state corruption is imminent
- A module has no documented inputs/outputs and callers are copy-pasting variable blocks
- Security scanning (tfsec, checkov) is absent from CI and the team is shipping IaC without policy checks

**Don't skip when:**
- Provisioning any production database or stateful resource — deletion protection and prevent_destroy must be set
- Adding a new environment — workspace isolation and backend key separation are required before first apply
- Handling secrets in Terraform — sensitive outputs, SSM/Secrets Manager references, and never-in-state patterns apply

## Core Patterns

### 1. Project Structure

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

### 2. Module Design

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

### 3. Remote State

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

### 4. Workspace Strategy

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

### 5. CI/CD for Terraform

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

### 6. Policy as Code (Sentinel)

```hcl
# policies/enforce_encryption.sentinel
import "tfplan/v2" as tfplan

main = rule {
  all tfplan.resource_changes as _, rc {
    rc.change.after.encrypted else true
  }
}
```

### 7. Security Scanning

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

### Checklist

- [ ] Remote state with locking (S3 + DynamoDB)
- [ ] State files never committed to git
- [ ] Modules follow semantic versioning
- [ ] Every module has documented inputs/outputs
- [ ] Sensitive outputs marked as `sensitive = true`
- [ ] Resource tags on every resource (Name, Environment, ManagedBy)
- [ ] prevent_destroy on critical resources (databases)
- [ ] CI/CD pipeline includes plan + apply stages
- [ ] Security scanning (tfsec/terrascan/checkov) in CI
- [ ] Cost estimation in CI (infracost)
- [ ] Workspace isolation (dev/staging/prod)
- [ ] Deletion protection on production databases

## Related Skills

- **devops-release-engineer** — Terraform provisions the infrastructure that release pipelines deploy to; coordinate when a new service requires both IaC changes and updated CI/CD configuration
- **cloud-security-auditor** — IAM policies, security group rules, and encryption settings provisioned by Terraform are the primary surface for cloud security review; use together when auditing or hardening infrastructure modules
- **docker-k8s-pro** — EKS, GKE, and AKS clusters are commonly provisioned with Terraform; coordinate when Terraform manages the Kubernetes control plane and node pools that docker-k8s-pro configures
- **security-reviewer** — sensitive variable handling, state file encryption, and least-privilege provider credentials are code-level security concerns; cross-reference when a module handles secrets or IAM
- **postgres-pro** — RDS and Cloud SQL instances provisioned in Terraform must align with the database configuration (instance class, parameter groups, backup windows) that postgres-pro recommends; coordinate on database module design
- **observability-pro** — CloudWatch, Grafana, and alerting infrastructure are often Terraform-managed; use together when building or extending the monitoring stack via IaC

## CRITICAL Findings
### C1: [Title] | [Framework]: [ID]
**Finding:** [What]
**Impact:** [Why matters]
**Fix:** [Concrete fix — code, not words]
## HIGH Findings
[Same format]
## MEDIUM / LOW
[Same format]
## Summary
- CRITICAL: N, HIGH: N, MEDIUM: N
- Verdict: PASS/FAIL
```
