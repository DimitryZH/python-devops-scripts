# GCP DevOps Automation

This folder contains **DevOps / SRE-focused Python components** that support the deployment and operation of an Employee Directory application on **Google Cloud Platform (GCP)**.

These components are used by a GCP application hosted in a separate repository:

- **AWS to GCP Migration: Employee Directory Application** – https://github.com/DimitryZH/emp-app/tree/main/GCP

The focus here is on the **automation, configuration, and operational tooling** around that workload, not on duplicating the web application code.

---

## Purpose and Scope

This folder is part of the broader `python-devops-scripts` portfolio and focuses on:

- **Environment-based configuration** for applications deployed to GCP.
- **Separation of concerns** between web application logic (in `emp-app`) and DevOps/SRE tooling (here).
- A foundation for future GCP automation scripts (provisioning, backups, health checks, etc.).

---

## Files

### `config.py`

File: [`config.py`](config.py:1)

Central configuration module used by the GCP Employee Management Portal and supporting automation scripts.

**Key characteristics:**

- Reads configuration from **environment variables**, in line with 12‑factor and cloud-native best practices:
  - `PHOTOS_BUCKET` – name of the Google Cloud Storage bucket used for storing employee photos.
  - `GCP_PROJECT` – GCP project ID the app and its resources run in.
  - `FLASK_SECRET` – Flask secret key, read from the environment with a default fallback.
  - Optional database settings (`DATABASE_HOST`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_DB_NAME`) when a relational DB is used.

**Why this is DevOps/SRE-related:**

- Encodes how the application is **configured per environment** (dev / staging / prod) without code changes.
- Is the central piece that CI/CD pipelines and infrastructure automation interact with:
  - Cloud Build / GitHub Actions / other pipelines set the required env vars.
  - Terraform / manual infra provisioning defines the buckets, projects, and database endpoints that these values point to.

This module is intentionally lightweight and reusable so both the app and operational scripts can import it.

---


# Future additions 
- Scripts to provision / validate GCP resources (buckets, service accounts, IAM bindings) for the employee app.
- Datastore / Firestore export, backup, and schema migration tools.
- Health-check and post-deployment verification scripts that call the app’s public endpoints.

All of these would live alongside [`config.py`](config.py:1) and use the same environment-driven configuration model.

---

## Related Project

- **AWS to GCP Migration: Employee Directory Application**  
  Repository: https://github.com/DimitryZH/emp-app/tree/main/GCP  
  This is where the actual Flask application code, routes, and templates reside; the `GCP-DevOps-Automation` folder in `python-devops-scripts` focuses on the surrounding configuration and operational tooling.
