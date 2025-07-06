# Kubernetes Deployment Guide

This directory contains Kubernetes configuration files for deploying the Messaging App.

## Prerequisites

1. Kubernetes cluster (Minikube, EKS, GKE, AKS, etc.)
2. `kubectl` configured to communicate with your cluster
3. Docker registry (e.g., Docker Hub, ECR, GCR) with push access

## Directory Structure

- `django-deployment.yaml`: Deployment and service for the Django application
- `mysql-deployment.yaml`: MySQL database deployment
- `redis-deployment.yaml`: Redis deployment for caching and Celery
- `ingress.yaml`: Ingress configuration for external access
- `configmap.yaml`: Non-sensitive configuration
- `secret.yaml`: Sensitive configuration (passwords, API keys, etc.)
- `db-migration-job.yaml`: Job to run database migrations
- `db-backup-cronjob.yaml`: CronJob for database backups
- `hpa.yaml`: Horizontal Pod Autoscaler configuration
- `pdb.yaml`: Pod Disruption Budget
- `network-policy.yaml`: Network policies for pod communication
- `resource-quota.yaml`: Resource quotas for the namespace
- `namespace.yaml`: Kubernetes namespace configuration
- `rbac.yaml`: Role-based access control configuration
- `deploy.sh`: Script to deploy all resources
- `delete-all.sh`: Script to delete all resources

## Deployment Steps

1. **Build and push the Docker image**:
   ```bash
   docker build -t your-dockerhub-username/messaging-app:latest .
   docker push your-dockerhub-username/messaging-app:latest
   ```

2. **Update the image name** in `django-deployment.yaml` and `db-migration-job.yaml` if needed.

3. **Update the domain** in `ingress.yaml`.

4. **Update the secrets** in `secret.yaml` with base64-encoded values:
   ```bash
   echo -n 'your-secret-key' | base64
   echo -n 'your-db-password' | base64
   ```

5. **Deploy all resources**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

6. **Verify the deployment**:
   ```bash
   kubectl get all -n messaging-app
   kubectl get ingress -n messaging-app
   ```

## Accessing the Application

- **Web Interface**: http://your-domain.com
- **Admin Interface**: http://your-domain.com/admin
- **Health Check**: http://your-domain.com/health/

## Scaling the Application

To scale the number of replicas:

```bash
kubectl scale deployment messaging-app --replicas=5 -n messaging-app
```

Or let the Horizontal Pod Autoscaler handle it based on CPU/memory usage.

## Database Backups

Database backups run daily at midnight and are stored in the `backup-pv-claim` PersistentVolume.

## Monitoring

To monitor the application:

```bash
# View logs
kubectl logs -l app=messaging-app -n messaging-app

# View pod status
kubectl get pods -n messaging-app

# View service status
kubectl get svc -n messaging-app

# View ingress status
kubectl get ingress -n messaging-app
```

## Cleanup

To delete all resources:

```bash
chmod +x delete-all.sh
./delete-all.sh
```

## Troubleshooting

- **Pods not starting**: Check logs with `kubectl logs <pod-name> -n messaging-app`
- **Database connection issues**: Verify the MySQL service is running and the credentials are correct
- **Ingress not working**: Check if the Ingress controller is installed and the host is correctly configured
- **PersistentVolume issues**: Ensure your cluster has a default StorageClass or create appropriate PersistentVolumes
