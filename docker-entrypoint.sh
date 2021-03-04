#!/bin/bash

echo "Migrate the Database at startup of project"

# Wait for few minute and run db migraiton
while ! python manage.py migrate  2>&1; do
   echo "Migration is in progress status"
   sleep 2
done

echo "Django docker is fully configured successfully."

exec "$@"
