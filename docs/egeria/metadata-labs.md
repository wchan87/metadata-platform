# Metadata Labs

The [Open Metadata Labs](https://egeria-project.org/education/open-metadata-labs/overview/) is the entrypoint to learning Egeria.

## Lab Setup

[Lab - Coco Pharmaceuticals (odpi-egeria-lab)](https://egeria-project.org/guides/operations/kubernetes/charts/lab/) leverages Helm to set up Kubernetes pods to stand up a proper environment. The underlying Helm chart that's used is [egeria-charts/charts/odpi-egeria-lab/](https://github.com/odpi/egeria-charts/blob/main/charts/odpi-egeria-lab/values.yaml) which has been archived but still usable.
```bash
helm repo add egeria https://odpi.github.io/egeria-charts
helm repo update
helm install lab egeria/odpi-egeria-lab
```
To confirm the setup via Helm, you can use commands like below to check if a deployment failed.
```bash
kubectl get all
kubectl describe pod
kubectl logs strimzi-cluster-operator-69d6cbc465-hvhjn
```
One known issue is related to [strimzi-kafka-operator](https://github.com/strimzi/strimzi-kafka-operator/issues/11386) which is resolved as follows (by setting the Kubernetes version):
```bash
kubectl set env deployment.apps/strimzi-cluster-operator STRIMZI_KUBERNETES_VERSION="major=1,minor=34"
```

Once the pods are ready, you can enable access to relevant services in separate terminals (as these commands won't return)
* Jupyter Notebook: https://localhost:8888 (token can be found in the container logs or running `jupyter server list` within the container)
    ```bash
    kubectl port-forward service/lab-jupyter 8888:8888
    ```
* React UI: https://localhost:8091/coco with credentials as `garygeeke` / `admin`
    ```bash
    kubectl port-forward service/lab-presentation 8091:8091
    ```
* Egeria UI: https://localhost:8443
    ```bash
    kubectl port-forward service/lab-uistatic 8443
    ```

The steps to setup the lab environment properly is as follows:

1. Start with the Jupyter notebook, [read-me-first.ipynb](https://localhost:8888/lab/tree/read-me-first.ipynb)
2. Run the Jupyter notebook, [egeria-server-config.ipynb](https://localhost:8888/lab/tree/egeria-server-config.ipynb) to configure the services needed
3. TBD

## Lab Teardown

```bash
helm delete lab
```
