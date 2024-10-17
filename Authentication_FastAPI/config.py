# Configuration settings for the project

# %% Database configuration
DATABASE = {
    'host': 'localhost',
    'port': 5432,
    'name': 'auth_db',
    'user': 'superAdmin',
    'password': 'HelloWorld',
}

DATABASE_URL = f"postgresql+psycopg2://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['name']}"

print(DATABASE_URL)
# %%
