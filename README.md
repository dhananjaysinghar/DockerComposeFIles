## Trivy Scan
docker pull aquasec/trivy
docker build -t <imageName> -f Dockerfile .
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL --vuln-type library --ignore-unfixed "<imageName>:latest"
