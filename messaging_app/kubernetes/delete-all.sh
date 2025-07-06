#!/bin/bash

# Exit on error
set -e

# Set namespace
NAMESPACE=messaging-app

# Delete all resources in the namespace
kubectl delete all --all -n $NAMESPACE
kubectl delete configmap --all -n $NAMESPACE
kubectl delete secret --all -n $NAMESPACE
kubectl delete pvc --all -n $NAMESPACE
kubectl delete networkpolicy --all -n $NAMESPACE
kubectl delete hpa --all -n $NAMESPACE
kubectl delete pdb --all -n $NAMESPACE
kubectl delete resourcequota --all -n $NAMESPACE
kubectl delete rolebinding --all -n $NAMESPACE
kubectl delete role --all -n $NAMESPACE
kubectl delete serviceaccount --all -n $NAMESPACE

# Delete the namespace (this will also delete all resources in the namespace)
kubectl delete namespace $NAMESPACE

echo "All resources in namespace $NAMESPACE have been deleted."
