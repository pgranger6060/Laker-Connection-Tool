from playwright.sync_api import sync_playwright, expect
import csv
import time
import pyautogui

def load_residents(file_path):
    with open(file_path, newline="") as f:
        return list(csv.DictReader(f))


def click_appointment_button(page, timeout=10000):
    try:
        button = page.locator("button.x-btn-text").filter(has_text="Appointment")
        button.wait_for(state="visible", timeout=timeout)
        expect(button).to_be_enabled(timeout=timeout)
        button.click()
        print("✓ Successfully clicked Appointment button")
        return True
    except Exception as e:
        print(f"✗ Failed to click Appointment button: {e}")
        return False


def type_in_student_combobox(page, student_name, timeout=10000):
    try:
        combobox = page.locator('input.x-form-field.sf-person-combobox[role="combobox"]')
        combobox.wait_for(state="visible", timeout=timeout)
        expect(combobox).to_be_enabled(timeout=timeout)
        combobox.click()
        combobox.fill("")
        combobox.type(student_name)
        time.sleep(1)  # allow AJAX search results
        expect(combobox).to_have_attribute("aria-expanded", "true", timeout=5000)
        print(f"✓ Typed student: {student_name}")
        return True
    except Exception as e:
        print(f"✗ Failed to type student: {e}")
        return False


def select_first_dropdown_result(page, timeout=5000):
    try:
        combobox = page.locator('input.x-form-field.sf-person-combobox[role="combobox"]')
        combobox.focus()
        time.sleep(1)
        combobox.press("ArrowDown")
        page.wait_for_timeout(300)
        combobox.press("Enter")
        expect(combobox).to_have_attribute("aria-expanded", "false", timeout=timeout)
        print("✓ Student selected")
        return True
    except Exception as e:
        print(f"✗ Failed to select student: {e}")
        return False


def fill_appointment_date(page, date_str, timeout=15000):
    try:
        date_field = page.locator('input.x-form-text.x-form-field[aria-label*="select a date"]').first
        date_field.wait_for(state="visible", timeout=timeout)
        expect(date_field).to_be_enabled(timeout=timeout)

        date_field.click()
        date_field.press("Control+a")
        date_field.press("Backspace")
        date_field.type(date_str, delay=50)
        date_field.press("Tab")
        expect(date_field).to_have_value(date_str, timeout=5000)
        print(f"✓ Date typed into textbox: {date_str}")
        return True

    except Exception as e:
        print(f"✗ Failed to fill date textbox: {e}")
        return False


def fill_start_time(page, start_time_str, timeout=15000):
    try:
        start_field = page.locator('input.x-form-text.x-form-field[aria-label="Start Time"]').first
        start_field.wait_for(state="visible", timeout=timeout)
        expect(start_field).to_be_enabled(timeout=timeout)

        start_field.click()
        start_field.press("Control+a")
        start_field.press("Backspace")
        start_field.type(start_time_str, delay=50)
        start_field.press("Tab")
        expect(start_field).to_have_value(start_time_str, timeout=5000)
        print(f"✓ Start time typed: {start_time_str}")
        return True

    except Exception as e:
        print(f"✗ Failed to fill start time: {e}")
        return False


def fill_end_time(page, end_time_str, timeout=15000):
    try:
        end_field = page.locator('input.x-form-text.x-form-field[aria-label="End Time"]').first
        end_field.wait_for(state="visible", timeout=timeout)
        expect(end_field).to_be_enabled(timeout=timeout)

        end_field.click()
        end_field.press("Control+a")
        end_field.press("Backspace")
        end_field.type(end_time_str, delay=50)
        end_field.press("Tab")
        page.wait_for_timeout(500)
        print(f"✓ End time typed: {end_time_str}")
        return True

    except Exception as e:
        print(f"✗ Failed to fill end time: {e}")
        return False
    
def select_location_online(page, timeout=10000):
    """
    Clicks at your physical mouse cursor position.
    """
    try:
        
        time.sleep(0.25)
        pyautogui.click()
        time.sleep(0.25)
        pyautogui.press('enter')
        
        return True
        
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
def select_reason(page, reason_code, timeout=10000):
    """
    Selects reason from dropdown using keyboard navigation.
    Reason codes: F1, S1, F2, S2, F3, S3
    """
    try:
        # Tab to the Reason field
        page.keyboard.press("Tab")
        page.wait_for_timeout(300)
        print("✓ Tabbed to Reason field")
        
        # Press Enter to open dropdown
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)
        print("✓ Opened Reason dropdown")
        
        # Determine number of down arrows based on reason code
        reason_map = {
            "F1": {"down": 1, "up": 1},  # Down then Up
            "S1": {"down": 1, "up": 0},  # Down only
            "F2": {"down": 2, "up": 0},
            "S2": {"down": 3, "up": 0},
            "F3": {"down": 4, "up": 0},
            "S3": {"down": 5, "up": 0}
        }
        
        if reason_code not in reason_map:
            print(f"✗ Invalid reason code: {reason_code}")
            return False
        
        actions = reason_map[reason_code]
        
        # Press Down arrow(s)
        for i in range(actions["down"]):
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(200)
        print(f"✓ Pressed ArrowDown {actions['down']} time(s)")
        
        # Press Up arrow(s) if needed (for F1)
        if actions["up"] > 0:
            for i in range(actions["up"]):
                page.keyboard.press("ArrowUp")
                page.wait_for_timeout(200)
            print(f"✓ Pressed ArrowUp {actions['up']} time(s)")
        
        # Press Enter to select
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)
        print(f"✓ Selected reason: {reason_code}")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to select reason: {e}")
        return False
    
def navigate_to_outcomes(page, text, timeout=10000):
    """
    Clicks the Outcomes tab and types the outcome text into the rich text editor.
    """
    try:
        # Click the Outcomes tab
        tab = page.locator('a.sf-main-tab-txt >> text=Outcomes')
        tab.wait_for(state="visible", timeout=timeout)
        tab.click()
        print("✓ Outcomes tab clicked")
        return True

    except Exception as e:
        print(f"✗ Failed to fill outcome text: {e}")
        return False
    
def fill_outcome_text(page, text, timeout=10000):
    """
    Types the outcome text into the Outcomes rich text editor iframe.
    Assumes you have already navigated to the Outcomes tab.
    """
    try:
        # Switch to the iframe by its title
        iframe = page.frame_locator('iframe[title="Comments, text editor"]')

        # Locate the body inside the iframe
        body = iframe.locator('body.html-editor')
        body.wait_for(state="visible", timeout=timeout)

        # Click to focus
        body.click()

        # Clear any existing text
        body.fill("")

        # Type the text (use small delay so ExtJS onChange triggers)
        body.type(text, delay=10)

        print("✓ Outcome text typed")
        return True

    except Exception as e:
        print(f"✗ Failed to fill outcome text: {e}")
        return False
    
def navigate_to_speednotes_tab(page, timeout=10000):
    """
    Clicks the SpeedNotes tab and waits for the tab content to be visible.
    """
    try:
        # Locate the SpeedNotes tab by its visible text
        tab = page.locator('a.sf-main-tab-txt >> text=SpeedNotes')
        tab.wait_for(state="visible", timeout=timeout)

        # Force click in case ExtJS decorations block normal click
        tab.click(force=True)
        print("✓ SpeedNotes tab clicked")

        # Wait briefly for tab content to render
        page.wait_for_timeout(500)

        return True

    except Exception as e:
        print(f"✗ Failed to navigate to SpeedNotes tab: {e}")
        return False
    
def check_wellbeing_checkbox(page, timeout=5000):
    """
    Checks the Well-being checkbox if it is not already checked.
    """
    try:
        # Locate the checkbox
        checkbox = page.locator('input[type="checkbox"][name="activity_3025"]')
        checkbox.wait_for(state="visible", timeout=timeout)
        expect(checkbox).to_be_enabled(timeout=timeout)

        # Check if already checked
        is_checked = checkbox.is_checked()
        if not is_checked:
            checkbox.click()
            print("✓ Well-being checkbox checked")
        else:
            print("✓ Well-being checkbox was already checked")

        return True

    except Exception as e:
        print(f"✗ Failed to check Well-being checkbox: {e}")
        return False
    
def press_submit_button(page, timeout=15000):
    """
    Clicks the Submit button in an ExtJS modal and waits for submission.
    """
    try:
        # Locate the clickable span with text "Submit"
        submit = page.locator('span.bold', has_text="Submit").first
        submit.wait_for(state="visible", timeout=timeout)

        # Scroll into view in case it's off-screen
        submit.scroll_into_view_if_needed()

        # Force click because ExtJS often blocks normal clicks
        submit.click(force=True)
        print("✓ Submit button clicked")

        # Optional: wait for modal to close or success indicator
        page.wait_for_timeout(2000)

        return True

    except Exception as e:
        print(f"✗ Failed to press Submit button: {e}")
        return False

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://oswego.starfishsolutions.com/starfish-ops/instructor/index.html")
    page.wait_for_selector("input.headerStudentSearch[role='combobox']", timeout=120_000)
    print("Dashboard search input found!")

    residents = load_residents("residents.csv")

    for idx, r in enumerate(residents, 1):
        print(f"\n--- Processing {idx}/{len(residents)}: {r['name']} ---")

        if not click_appointment_button(page):
            continue

        time.sleep(2)

        if not type_in_student_combobox(page, r["name"]):
            continue

        if not select_first_dropdown_result(page):
            continue

        page.wait_for_timeout(1000)

        if not fill_appointment_date(page, r["date"]):
            continue

        if not fill_start_time(page, r["start_time"]):
            continue

        if not fill_end_time(page, r["end_time"]):
            continue

        if not select_location_online(page):
            continue

        if not select_reason(page, r["reason"]):
            continue

        if not navigate_to_outcomes(page, r["outcome_text"]):
            continue

        if not fill_outcome_text(page, r["outcome_text"]):
            continue

        if not navigate_to_speednotes_tab(page):
            continue

        if not check_wellbeing_checkbox(page):
            continue

        if not press_submit_button(page):
            continue

        time.sleep(2)

    browser.close()
    