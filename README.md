# Setup
## Clone the repository
git clone https://github.com/ummerooman/Learning.git

## Create a virtual environment and activate it
python -m venv venv  
venv\Scripts\activate

## Install the requirements
pip install -r requirements.txt

## Run the app
python app.py

# Use the api via postman
## Create an environment
variable = base_url  
initial value = http://127.0.0.1:5000

## Add tasks
Method : POST  
URL: {{base_url}}/tasks  
Headers: key = Content-Type, value = application/json  
Body: raw, JSON
### Examples:
{  
  name : "Take medicines",  
  is_completed: True  
}  
{  
  name : "Buy groceries"  
}

## View tasks
Method: GET
### View all tasks
URL: {{base_url}}/tasks
### View all is_completed = true tasks
URL : {{base_url}}/tasks?is_completed=true
### View all is_completed = false tasks
URL : {{base_url}}/tasks?is_completed=false
### View a certain task
URL : {{base_url}}/tasks?name=Take%20medicines

## Edit a task
Method: PATCH  
URL: {{base_url}}/tasks/<task_id>  
Headers : key = Content-Type, value = application/json  
Body: raw, JSON
### Examples
{  
  is_completed = True  
}  
{  
  name = "Visit the doctor"  
}







