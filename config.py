# Configuration settings for the project

# %% Database configuration
DATABASE = {
    'host': 'localhost',
    'port': 5432,
    'name': 'local_db',
    'user': 'postgres',
    'password': '12345',
}

DATABASE_URL = f"postgresql://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['name']}"

print(DATABASE_URL)
# %%
