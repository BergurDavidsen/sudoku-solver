import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from sudoku_solver import SudokuSolver
from sudoku_solver_csp import SudokuSolverCSP


def main():
    url = "https://www.sudokuonline.io/easy"

    service = Service()  # Optional: add path to chromedriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Optional
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        driver.add_cookie({"name":"sessionid", "value":"qp0vut0ku2h1p4v40wvxrwfycjqmvqbr", "path":"/"})
        while True:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "sudoku"))
            )

            # Try clicking cookie prompt if it's there
            try:
                driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[1]').click()
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[1]/div/div[2]/button[1]'))
                )
                driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[1]/div/div[2]/button[1]').click()
            except:
                pass  # Ignore if not shown again

            # Scrape the grid
            cells = driver.find_elements(By.CSS_SELECTOR, '#sudoku .cell')
            board = [[0] * 9 for _ in range(9)]

            for cell in cells:
                row = int(cell.get_attribute("data-row"))
                col = int(cell.get_attribute("data-column"))
                val = cell.get_attribute("data-value")
                board[row][col] = int(val) if val.isdigit() else 0

            solver = SudokuSolver(board)
            if solver.solve():
                random.shuffle(cells)
                has_waited = False
                for cell in cells:
                    classes = cell.get_attribute("class")
                    if "fixed" in classes:
                        #for evading bot detection
                        if not has_waited:
                            #time.sleep(70)
                            has_waited = True
                        continue
                    row = int(cell.get_attribute("data-row"))
                    col = int(cell.get_attribute("data-column"))
                    val = board[row][col]
                    cell.send_keys(str(val))
                    # time.sleep(random.uniform(0.2, 2.5))

            # Wait a bit to look human or simulate time to solve
            time.sleep(random.uniform(2.0, 4.0))

            # Refresh to get new puzzle
            driver.get(url)

    finally:
        input("Press Enter to close browser...")
        driver.quit()


if __name__ == "__main__":
    main()
