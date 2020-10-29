FROM nginx:stable

ARG SUPPORT_EMAIL="devops@guadaltech.es"
ARG TEAM_NAME="DevOps Team"

ADD custom/conf.d/ /etc/nginx/conf.d/
ADD custom/html/ /usr/share/nginx/html/

RUN for file_error in $(ls /usr/share/nginx/html/); do \
        echo "Update file: $file_error"; \
        sed -i "s/SUPPORT_EMAIL/$SUPPORT_EMAIL/g" /usr/share/nginx/html/$file_error; \
        sed -i "s/TEAM_NAME/$TEAM_NAME/g" /usr/share/nginx/html/$file_error; \
    done