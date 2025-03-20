import time
import zipfile
import os
import glob
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotInteractableException,
    TimeoutException,
    NoSuchElementException
)
from webdriver_manager.chrome import ChromeDriverManager
import gemmi

def automate_prediction(email, password, file_path):
    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    
    # Set the default download directory dynamically
    downloads_path = os.path.expanduser("~/Downloads")
    prefs = {"download.default_directory": downloads_path}
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize the Chrome driver
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("AlphaFold server login page...")
        driver.get("https://alphafoldserver.com")

        google_login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Continue with Google')]"))
        )
        google_login_button.click()

        print("Logging in...")
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
        )
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)

        for _ in range(5):
            try:
                password_input = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
                )
                password_input.send_keys(password)
                password_input.send_keys(Keys.RETURN)
                break
            except ElementNotInteractableException:
                time.sleep(1)
        else:
            raise Exception("Unable to log in after multiple attempts.")

        WebDriverWait(driver, 20).until(EC.url_contains("alphafoldserver.com"))

        print("Loading the Excel file...")
        df = pd.read_excel(file_path)

        if 'variant' not in df.columns or 'fasta_sequence' not in df.columns:
            raise KeyError("Excel file is missing required columns. Available columns: " + ", ".join(df.columns))

        variant_list = df['variant'].tolist()
        fasta_sequence_list = df['fasta_sequence'].tolist()

        # Create dynamic output path
        extraction_path = os.path.join(os.getcwd(), "Output")
        os.makedirs(extraction_path, exist_ok=True)
        print(f"Output will be saved in: {extraction_path}")

        for i, (variant, fasta_sequence) in enumerate(zip(variant_list, fasta_sequence_list)):
            if i >= 20:
                print("Reached the limit of 20 jobs. Exiting loop.")
                break

            try:
                print(f"Processing variant {i+1}: {variant}")
                clear_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Clear')]"))
                )
                clear_button.click()

                fasta_sequence_textarea = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Input']"))
                )
                fasta_sequence_textarea.clear()
                fasta_sequence_textarea.send_keys(fasta_sequence)

                continue_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Continue and preview job')]"))
                )
                continue_button.click()

                submit_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Confirm and submit job')]"))
                )
                submit_button.click()

                print("Job submitted. Waiting for processing...")
                time.sleep(100)

                while True:
                    try:
                        menu_button = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "//tr[@role='row']//button"))
                        )
                        driver.execute_script("arguments[0].scrollIntoView(true);", menu_button)
                        time.sleep(1)
                        menu_button.click()

                        download_link = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Download')]"))
                        )
                        download_link.click()
                        print("Download initiated successfully.")
                        break
                    except (TimeoutException, NoSuchElementException):
                        print("Download link not available yet. Waiting for 3 minutes.")
                        time.sleep(180)

                print("Waiting for download to complete...")
                time.sleep(30)

                print("Extracting downloaded file...")
                list_of_files = glob.glob(os.path.join(downloads_path, '*.zip'))
                if not list_of_files:
                    raise FileNotFoundError("No .zip files found in the downloads directory.")

                latest_file = max(list_of_files, key=os.path.getctime)
                json_extracted, cif_extracted = False, False

                with zipfile.ZipFile(latest_file, 'r') as zip_ref:
                    for file in zip_ref.namelist():
                        if '_summary_confidences_0.json' in file:
                            zip_ref.extract(file, extraction_path)
                            json_extracted = True
                        if '_model_0.cif' in file:
                            zip_ref.extract(file, extraction_path)
                            cif_extracted = True
                        if json_extracted and cif_extracted:
                            break

                if json_extracted and cif_extracted:
                    for file in os.listdir(extraction_path):
                        if '_summary_confidences_0.json' in file:
                            os.rename(os.path.join(extraction_path, file), os.path.join(extraction_path, f"{variant}_summary0.json"))
                        if '_model_0.cif' in file:
                            os.rename(os.path.join(extraction_path, file), os.path.join(extraction_path, f"{variant}_model0.cif"))

                    cif_file = os.path.join(extraction_path, f"{variant}_model0.cif")
                    pdb_file = os.path.join(extraction_path, f"{variant}_model0.pdb")
                    if os.path.exists(cif_file):
                        structure = gemmi.read_structure(cif_file)
                        structure.write_pdb(pdb_file)
                else:
                    print("Required files were not found in ZIP archive.")
            except Exception as e:
                print(f"Error processing variant {variant}: {e}")
    finally:
        driver.quit()
