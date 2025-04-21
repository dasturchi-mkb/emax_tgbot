import asyncpg
from asyncpg.pool import Pool
from asyncpg.exceptions import UniqueViolationError
from typing import Union
from config.config import db_host, db_name, db_pass, db_user


class DataBase:
    def __init__(self):
        self.pool: Union[Pool, None] = None
    
    async def create_pool(self):
        self.pool = await asyncpg.create_pool(user=db_user, host=db_host, database=db_name,
                                              password=db_pass, max_inactive_connection_lifetime=0)

    async def create_tables(self):
        sql = """
        CREATE TABLE if not exists category_group(id SERIAL PRIMARY KEY, name VARCHAR unique);

        CREATE TABLE if not exists category(id SERIAL PRIMARY KEY, name VARCHAR unique,
            category_group_id INTEGER, FOREIGN KEY (category_group_id) REFERENCES category_group(id)
        );
    
        CREATE TABLE if not exists "user"(
            id SERIAL PRIMARY KEY, chat_id BIGINT UNIQUE, username VARCHAR(255) NULL, full_name VARCHAR(255)
        );
        
        CREATE TABLE if not exists product(
            id SERIAL PRIMARY KEY, name VARCHAR(500), description TEXT,
            category_id INTEGER, user_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES category(id)
        );
        
        CREATE TABLE if not exists images(
            id SERIAL PRIMARY KEY, image_path text, product_id INTEGER,
            FOREIGN KEY (product_id) REFERENCES product(id)
        );
        """
        await self.pool.execute(sql)

    async def add_user(self, chat_id, username, full_name):
        await self.pool.execute(
            """INSERT INTO "user" (
                chat_id, username, full_name) VALUES (
                $1, $2, $3) ON CONFLICT (chat_id) 
                DO UPDATE SET username = EXCLUDED.username, full_name = EXCLUDED.full_name""",
            chat_id, username, full_name
        )

