#!/bin/bash

# Function to display help information
display_help() {
    echo "Usage: manage.sh [command] [options]"
    echo
    echo "Commands:"
    echo "  app [name]    Create a new Django app with the specified name"
    echo "  run           Run the Django development server"
    echo "  migrate       Apply database migrations"
    echo "  su            Create a Django superuser"
    echo
    echo "Options:"
    echo "  -h, --help    Show this help message and exit"

    exit 0
}

# Function to create a new Django app
create_app() {
    if ! ./dmanage.py startapp --template app_template "$1"; then
        echo "Error creating app $1"
        exit   1
    fi
}

# Function to run the Django development server
run_server() {
    if ! ./dmanage.py runserver   0.0.0.0:8000; then
        echo "Error running server"
        exit   1
    fi
}

# Function to handle migrations
migrate() {
    if ! ./dmanage.py makemigrations; then
        echo "Error creating migrations"
        exit   1
    fi
    if ! ./dmanage.py migrate; then
        echo "Error applying migrations"
        exit   1
    fi
}

# Function to create a Django superuser
create_superuser() {
    if ! ./dmanage.py createsuperuser; then
        echo "Error creating superuser"
        exit   1
    fi
}

# Handling command-line arguments
case "$1" in
    app)
        create_app "$2"
        ;;
    run)
        run_server
        ;;
    migrate)
        migrate
        ;;
    su)
        create_superuser
        ;;
    --help|-H)
        display_help
        ;;
    *)
        ./dmanage.py "$@"
        ;;
esac
