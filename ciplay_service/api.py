from fastapi import APIRouter
import asyncpg

# from .settings import USER, PASSWORD, DATABASE, HOST


router = APIRouter(
    prefix='/devices'
)
