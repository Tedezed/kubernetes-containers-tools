FROM alpine/terragrunt:1.3.7

RUN set -e \
    && apk add curl python3 \
    && curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x kubectl \
    && mv ./kubectl /bin/kubectl \
    && curl -sSL https://sdk.cloud.google.com | sh

RUN ln -s /root/google-cloud-sdk/.install/.backup/bin/gcloud /bin/gcloud
