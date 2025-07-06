#!/bin/bash

# Exit on error
set -e

# Set namespace
NAMESPACE=messaging-app

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Apply RBAC
kubectl apply -f rbac.yaml -n $NAMESPACE

# Apply ConfigMap and Secret
kubectl apply -f configmap.yaml -n $NAMESPACE
kubectl apply -f secret.yaml -n $NAMESPACE

# Apply MySQL
kubectl apply -f mysql-deployment.yaml -n $NAMESPACE

# Apply Redis
kubectl apply -f redis-deployment.yaml -n $NAMESPACE

# Wait for MySQL and Redis to be ready
kubectl wait --for=condition=ready pod -l app=mysql --timeout=300s -n $NAMESPACE
kubectl wait --for=condition=ready pod -l app=redis --timeout=300s -n $NAMESPACE

# Apply Django application
kubectl apply -f django-deployment.yaml -n $NAMESPACE

# Apply NetworkPolicy
kubectl apply -f network-policy.yaml -n $NAMESPACE

# Apply HPA
kubectl apply -f hpa.yaml -n $NAMESPACE

# Apply PDB
kubectl apply -f pdb.yaml -n $NAMESPACE

# Apply ResourceQuota
kubectl apply -f resource-quota.yaml -n $NAMESPACE

# Wait for Django to be ready
kubectl wait --for=condition=ready pod -l app=messaging-app --timeout=300s -n $NAMESPACE

# Run database migrations
kubectl apply -f db-migration-job.yaml -n $NAMESPACE

# Wait for migration job to complete
kubectl wait --for=condition=complete job/db-migration --timeout=300s -n $NAMESPACE

# Apply Ingress
kubectl apply -f ingress.yaml -n $NAMESPACE

echo "Deployment completed successfully!"
echo "You can access the application at: http://your-domain.com"
