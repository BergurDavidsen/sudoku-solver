from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from sudoku_solver import SudokuSolver
from sudoku_solver_csp import SudokuSolverCSP

def main():
    url = "https://www.websudoku.com?level=4"

    service = Service()  # Optional: add path to chromedriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Optional
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)

        # Wait for the frame to be present
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "frame"))
        )

        # Now inside the frame — wait for puzzle inputs
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[starts-with(@id, 'f')]"))
        )

        # Get page source of the inner frame
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract Sudoku board
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                cell_id = f"f{row}{col}"
                input_element = soup.find("input", id=cell_id)
                value = input_element.get("value", "")
                current_row.append(int(value) if value.isdigit() else 0)
            board.append(current_row)

        # Print the board
        for row in board:
            print(row)
            
        solver = SudokuSolver(board)
        
        solved = solver.solve()
        
        if solved:
            print()
            print("solved board:")
            for row in board:
                print(row)
            for row in range(9):
                for col in range(9):
                    cell_id = f"f{row}{col}"
                    if board[row][col] != 0:
                        input_element = driver.find_element(By.ID, cell_id)
                        # Only fill if it was originally empty
                        original_value = input_element.get_attribute("value")
                        if not original_value.strip():
                            input_element.clear()
                            input_element.send_keys(str(board[row][col]))
            driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td[2]/table/tbody/tr[2]/td/form/p[3]/input[1]').click()
        else:
            print("No solution")

    finally:
        input("Press Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    main()
