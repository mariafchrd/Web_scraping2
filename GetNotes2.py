from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import time
import re

# Setup Chrome driver
options = Options()
options.add_argument("user-agent=Mozilla/5.0")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

def get_youtube_url(driver):
    """Extract YouTube URL from current page"""
    try:
        # First try to find direct links
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            href = link.get_attribute("href")
            if href and ("youtube.com/watch" in href or "youtu.be" in href):
                return href
        
        # Then check page content
        page_content = driver.page_source
        youtube_matches = re.findall(
            r'(https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{11})[^\s"]*', 
            page_content
        )
        if youtube_matches:
            return youtube_matches[0][0]
        
        # Check for iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            src = iframe.get_attribute("src")
            if src and ("youtube.com" in src or "youtu.be" in src):
                return src
                
    except Exception as e:
        print(f"Error while searching for YouTube URL: {str(e)}")
    
    return None

def clean_youtube_url(url):
    """Standardize YouTube URL format"""
    if not url:
        return None
    
    # Extract video ID
    video_id_match = re.search(
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|embed\/)([\w-]{11})', 
        url
    )
    if video_id_match:
        return f"https://www.youtube.com/watch?v={video_id_match.group(1)}"
    return url

def save_to_excel(data, filename="MyNotes2.xlsx"):
    """Save data to Excel file"""
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"✅ Successfully saved {len(data)} YouTube links to '{filename}'")
        return True
    except Exception as e:
        print(f"❌ Error saving to Excel: {str(e)}")
        return False

def main():
    data = []
    try:
        # Login
        print("Logging in...")
        driver.get("https://----") #the site URL
        wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys('Your Username') #input your username
        driver.find_element(By.ID, 'password').send_keys('Your Password') #input your Password
        driver.find_element(By.ID, 'loginbtn').click()

        # Wait for login to complete
        wait.until(EC.url_contains("the body of the URL")) #INPUT
        print("Login successful")

        # Go to course page
        course_url = "https://----" # the page containing the notes URL
        print(f"Navigating to course: {course_url}")
        driver.get(course_url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.courseindex-section")))
        print("Course page loaded")

        # Collect all activity links first
        activities = []
        sections = driver.find_elements(By.CSS_SELECTOR, "div.courseindex-section")
        
        for section in sections:
            try:
                title_element = section.find_element(By.CSS_SELECTOR, ".courseindex-section-title .courseindex-link")
                class_title = title_element.text.strip()

                section_activities = section.find_elements(By.CSS_SELECTOR, "li.courseindex-item")
                
                for activity in section_activities:
                    try:
                        link = activity.find_element(By.CSS_SELECTOR, "a.courseindex-link")
                        activity_name = link.text.strip()
                        activity_url = link.get_attribute("href")

                        if activity_name.lower() != "announcements":
                            activities.append({
                                "class_title": class_title,
                                "activity_name": activity_name,
                                "url": activity_url
                            })
                    except Exception as e:
                        print(f"Error collecting activity link: {str(e)}")
            except Exception as e:
                print(f"Error processing section: {str(e)}")

        print(f"\nFound {len(activities)} activities to process")
        
        # Process each activity
        for i, activity in enumerate(activities, 1):
            print(f"\nProcessing activity {i}/{len(activities)}: {activity['activity_name']}")
            
            try:
                # Open activity in new tab
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(activity['url'])
                
                # Wait for page to load
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main']")))
                    
                    # Get YouTube URL
                    youtube_url = get_youtube_url(driver)
                    clean_url = clean_youtube_url(youtube_url) if youtube_url else None
                    
                    if clean_url:
                        data.append({
                            "Class Title": activity['class_title'],
                            "Activity Name": activity['activity_name'],
                            "YouTube URL": clean_url                        
                        })
                        print(f"✅ Found YouTube video: {clean_url}")
                    else:
                        print(f"⚠️ No YouTube link found")
                    
                except Exception as e:
                    print(f"Error loading activity page: {str(e)}")
                
                # Close tab and switch back
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)  # Brief pause
                
            except Exception as e:
                print(f"Error processing activity: {str(e)}")
                # Ensure we're back to main window
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"❌ Major error occurred: {str(e)}")
    finally:
        driver.quit()
        # Save data even if script fails
        if data:
            save_to_excel(data)
        else:
            print("\n⚠️ No YouTube links were collected")

        print("\nScript completed")

if __name__ == "__main__":
    main()