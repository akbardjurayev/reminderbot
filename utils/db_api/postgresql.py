from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
            port=config.DB_PORT
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def create_users_table(self):
        sql = """CREATE TABLE IF NOT EXISTS public.users (         
        id bigserial primary key,
        telegram_id bigint not null constraint users_telegram_id_unique unique,
        name varchar(255),  
        last_page integer,  
        page_aim integer,  
        created_at  timestamp(0) default now() not null,
        updated_at  timestamp(0) default now() not null
        );"""
        await self.execute(sql, execute=True)

    async def create_pages_table(self):
        sql = """CREATE TABLE IF NOT EXISTS public.pages (         
        id bigserial primary key,
        last_page integer,  
        goal_page integer,  
        created_at  timestamp(0) default now() not null,
        updated_at  timestamp(0) default now() not null
        );"""
        await self.execute(sql, execute=True)

    async def create_user(self, **kwargs):
        sql = """INSERT INTO public.users (telegram_id, name,  last_page, page_aim) VALUES ($1,$2,$3,$4)"""
        return await self.execute(sql, *kwargs.values(), execute=True)

    async def create_page(self, **kwargs):
        sql = """INSERT INTO public.users (last_page, last_page) VALUES ($1,$2)"""
        return await self.execute(sql, *kwargs.values(), execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM public.users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM public.users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM public.users"
        return await self.execute(sql, fetchval=True)

    async def update_user_last_page(self, last_page, telegram_id):
        sql = "UPDATE public.users SET last_page=$1 WHERE telegram_id=$2"
        return await self.execute(sql, last_page, telegram_id, execute=True)

    async def update_user_page_aim(self, page_aim, telegram_id):
        sql = "UPDATE public.users SET page_aim=$1 WHERE telegram_id=$2"
        return await self.execute(sql, page_aim, telegram_id, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE public.users", execute=True)

    async def get_languages(self):
        sql = "SELECT * FROM public.languages"
        return await self.execute(sql, fetch=True)

    async def add_language(self, name, code, flag):
        sql = "INSERT INTO public.languages (name, code, flag) VALUES ($1,$2,$3)"
        return await self.execute(sql, name, code, flag, execute=True)

    async def get_word_types(self):
        sql = "SELECT * FROM public.types"
        return await self.execute(sql, fetch=True)

    async def add_word_type(self, name):
        sql = "INSERT INTO public.types (name) VALUES ($1)"
        return await self.execute(sql, name, execute=True)

    async def add_word(self, name, language_id):
        sql = "INSERT INTO public.words (name, language_id) VALUES ($1,$2) RETURNING id"
        return await self.execute(sql, name, language_id, fetchval=True)

    async def add_dictionary(self, word_id, translation_id):
        sql = "INSERT INTO public.dictionaries (word_id, translation_id) VALUES ($1,$2)"
        return await self.execute(sql, word_id, translation_id, execute=True)

    async def delete_word(self, word_id):
        sql = "DELETE FROM public.words WHERE id=$1"
        return await self.execute(sql, word_id, execute=True)

    async def get_random_test(self):
        sql = """select w.name as arabic_name, w2.name as uzbek_name, w.id as arabic_name_id, w2.id as uzbek_name_id from dictionaries
         left join words w on (w.id = dictionaries.translation_id) left join words w2 on (w2.id = dictionaries.word_id) 
         OFFSET floor(random() * (select count(*) from dictionaries)) LIMIT 100;"""
        return await self.execute(sql, fetch=True)

    async def get_random_options(self, word_id, limit, type_word):
        type_word = "translation_id" if type_word == "arabic" else "word_id"
        sql = f"""select w.name as name, w.id as id from dictionaries
                  left join words w on (w.id = dictionaries.{type_word}) 
                  where w.id != {word_id} OFFSET floor(random() * (select count(*) from dictionaries)) LIMIT {limit};"""
        return await self.execute(sql, fetch=True)
