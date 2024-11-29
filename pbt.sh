#!/bin/bash


help() {
    echo "Welcome to Python Backend Templates!
Usage:
$ pdt [COMMAND] [OPTION]"

    echo "Commands:"
    echo " template        Use the repository as a template"
    echo " clear           Delete all installation files"
    echo " --help          Show this help message and exit"

    echo "Options:"
    echo " -h, --help      Show this help message and exit"
}

django_setup() {
    pr_name=$1


    sed -i "s/projectname/$pr_name/g" README.md
    mkdir docs
    touch "docs/{$pr_name}.dbml"
    touch "docs/{$pr_name}_TZ.md"

    # local containers
    cp pbt_configs/containers-django/Dockerfile.local server/Dockerfile.local
    cp pbt_configs/containers-django/docker-compose.local.yml docker-compose.yml

    # dev containers
    cp pbt_configs/containers-django/Dockerfile.dev server/Dockerfile.dev
    cp pbt_configs/containers-django/docker-compose.dev.yml docker-compose.dev.yml

    # prod containers
    cp pbt_configs/containers-django/Dockerfile.prod server/Dockerfile.prod
    cp pbt_configs/containers-django/docker-compose.prod.yml docker-compose.prod.yml

    # other utils
    cp pbt_configs/containers-django/entrypoint.local.sh server/entrypoint.local.sh
    cp pbt_configs/containers-django/entrypoint.dev.sh server/entrypoint.dev.sh
    cp pbt_configs/containers-django/entrypoint.prod.sh server/entrypoint.prod.sh
    cp pbt_configs/deploy.sh deploy.sh
    mv .dockerignore server/.dockerignore

    chmod 755 deploy.sh
}


template_drf() {
    mv django-template-drf server 
    rm -rf README.md

    cat pbt_configs/django_drf_readme.md > README.md
    read -p "Project name: " pr_name
    django_setup "$pr_name"
}

template_gql() {

    # delete files
    rm -rf README.md
    rm -rf LICENSE

    mv django-template-gql server 

    read -p "Project name: " pr_name

    cat pbt_configs/django_gql_readme.md > README.md
    sed -i "s/projectname/$pr_name/g" README.md
    touch "docs/{$pr_name}.dbml"
    touch "docs/{$pr_name}_TZ.md"

    # local containers
    cp pbt_configs/containers-django/Dockerfile.local server/Dockerfile.local
    cp pbt_configs/containers-django/docker-compose.local.yml docker-compose.yml

    # dev containers
    cp pbt_configs/containers-django/Dockerfile.dev server/Dockerfile.dev
    cp pbt_configs/containers-django/docker-compose.dev.yml docker-compose.dev.yml

    # prod containers
    cp pbt_configs/containers-django/Dockerfile.prod server/Dockerfile.prod
    cp pbt_configs/containers-django/docker-compose.prod.yml docker-compose.prod.yml

    # other utils
    cp pbt_configs/containers-django/entrypoint.local.sh server/entrypoint.local.sh
    cp pbt_configs/containers-django/entrypoint.dev.sh server/entrypoint.dev.sh
    cp pbt_configs/containers-django/entrypoint.prod.sh server/entrypoint.prod.sh
    cp pbt_configs/deploy.sh deploy.sh
    mv .dockerignore server/.dockerignore

    chmod 755 deploy.sh

}

template_fastapi() {
  echo "NOt ready"
}

clear() {
    rm -rf LICENSE
    rm -rf django-template-gql
    rm -rf django-template-drf
    rm -rf fast-api-template
    rm -rf pbt_configs
    rm -rf pbt.sh 
    read -p "Remove nginx? [y/n]" ans
    if [[ "$ans" == "y" || "$ans" == "Y" ]]; then
      rm -rf nginx
    fi 
}

as_template() {
    echo "Select template:"
    echo "[1] Django + DRF"
    echo "[2] Django + Graphene"
    echo "[2] Fast Api"
    read -p "> " template_choice

    case "$template_choice" in
        1)
            echo "Django + DRF"
            template_drf
            ;;
        2)
            echo "Django + Graphene"
            template_gql
            ;;
        3)
            echo "Fast Api"
            template_fastapi
            ;;
        *)
            echo "Aborted..."
            exit 1
            ;;
    esac
}

case "$1" in
    template)
        as_template
        ;;
    clear)
        clear
        ;;
    *)
        help
        ;;
esac
