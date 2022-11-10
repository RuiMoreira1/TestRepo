echo "Deploying changes..."

# Shut down the existing containers
echo $1 | sudo -S docker compose down 

# Removes all images
echo $1 | sudo -S docker system prune -a -f

echo $1 | sudo -S docker network rm shift_planner_project_default

# Rebuild and start the new containers 
echo $1 | sudo -S docker compose -f docker-compose.yml -f docker-compose.production.yml up --build -d 
echo "Deployed!"  
