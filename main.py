# main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sudoku_solver import SudokuSolver
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class SudokuRequest(BaseModel):
    board: list[list[int]]

@app.post("/solve")
async def solve_sudoku(req: SudokuRequest):
    board = req.board
    solver = SudokuSolver(board)
    solved, solve_time = solver.solve()
    if solved:
        return {"solved": True, "solution": solver.board, "solve_time": solve_time}
    else:
        return {"solved": False, "message": "No solution found"}

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as f:
        return f.read()
