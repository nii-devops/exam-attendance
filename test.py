from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash



load_dotenv()


surname = os.getenv('ADMIN_SURNAME')
first_name = os.getenv('ADMIN_FIRSTNAME')
email = os.getenv('ADMIN_EMAIL')
phone = os.getenv('ADMIN_PHONE')
department = os.getenv('ADMIN_DEPARTMENT')
password = generate_password_hash(os.getenv('ADMIN_PASSWORD'), method='scrypt', salt_length=8)

print(f"Name: {first_name} {surname} \nEmail: {email} \nContact: {phone} \nDepartment: {department} \nEncrypted Password: {password}")

new_password = generate_password_hash("Helvetica@Swift86", method='scrypt', salt_length=8)
print(new_password)