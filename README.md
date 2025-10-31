# Install dependencies
Download MySQL [here](https://dev.mysql.com/downloads/mysql/)
- Search online how to setup. 
- Set password to `password`
- Mac can follow this instruction but no need install workbench (https://www.youtube.com/watch?v=ODA3rWfmzg8) 

Create database from `refinedModel.sql`
Use the command below but use your file location of the refinedModel.sql (Inside the project root folder)
- `mysql -u root -p <filelocation>`
- then type in your password (Should be `password`)
For  example my one is
```bash
mysql -u root -p < '/Users/xinnie/Library/Project/67/refinedModel.sql'
```


Install Flask and mysql-connector modules
```bash
python3 -m pip install Flask mysql-connector-python
```

# Running applicaiton
```bash
flask --app app --debug run
```

App link: http://127.0.0.1:5000

# Additional info
These are the current users populated in the database
| **username**| **password**  | **role** 
| SystemAdmin | 1             | Admin
| ganbf       | 1             | Admin
| CSR         | 11            | Platform_Manager
| mgr         | 2             | Platform_Manager
| pin01       | pin123        | PIN_Support

