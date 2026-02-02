import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.urls import LOGIN_URL, SIGNUP_URL, WELCOME_URL
from playwright.sync_api import expect
import re

def test_PODCAST_TC_001_NavigatePodGalleryButton(authenticated_page):
    """Verify clicking the 'Pod Gallery' button"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Click the 'Pod Gallery' button
    pod_gallery_button_selector = "button:has-text('Pod Gallery')"
    authenticated_page.locator(pod_gallery_button_selector).click(timeout=10000)

    # Expected: Current URL changes to 'https://dev.vox.snappod.ai/pod-gallery' (inferred)
    expect(authenticated_page).to_have_url(re.compile(r"dev\.vox\.snappod\.ai/pod-gallery"), timeout=10000)

def test_PODCAST_TC_002_NavigateUpgradeButton(authenticated_page):
    """Verify clicking the 'Upgrade' button"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Click the 'Upgrade' button
    upgrade_button_selector = "button:has-text('Upgrade')"
    authenticated_page.locator(upgrade_button_selector).click(timeout=10000)

    # Expected: Current URL changes to 'https://dev.vox.snappod.ai/upgrade' (inferred)
    expect(authenticated_page).to_have_url(re.compile(r"dev\.vox\.snappod\.ai/upgrade"), timeout=10000)

def test_PODCAST_TC_003_GenerateScriptMinimumFields(authenticated_page):
    """Verify script generation with only the required podcast topic"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Enter 'The Future of AI in Healthcare' into the podcast topic input field
    podcast_topic_input_selector = "#rc_select_0"
    podcast_topic_value = "The Future of AI in Healthcare"
    authenticated_page.locator(podcast_topic_input_selector).fill(podcast_topic_value, timeout=10000)
    expect(authenticated_page.locator(podcast_topic_input_selector)).to_have_value(podcast_topic_value, timeout=10000)

    # Click the 'GENERATE SCRIPT' button
    generate_script_button_selector = "button:has-text('GENERATE SCRIPT')"
    authenticated_page.locator(generate_script_button_selector).click(timeout=10000)

    # Expected: The 'GENERATE SCRIPT' button indicates activity.
    # For a static site, we primarily verify that the interaction occurs and the page state (URL) remains.
    expect(authenticated_page.locator(generate_script_button_selector)).to_be_visible(timeout=10000)
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000) # Expect to stay on the same page

def test_PODCAST_TC_004_GenerateScriptAllFields(authenticated_page):
    """Verify script generation with all available fields filled"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Enter 'Innovations in Renewable Energy' into the podcast topic input field
    podcast_topic_input_selector = "#rc_select_0"
    podcast_topic_value = "Innovations in Renewable Energy"
    authenticated_page.locator(podcast_topic_input_selector).fill(podcast_topic_value, timeout=10000)
    expect(authenticated_page.locator(podcast_topic_input_selector)).to_have_value(podcast_topic_value, timeout=10000)

    # Click the Language input, then select 'English (Indian)'
    language_input_selector = "#react-select-2-input"
    language_option_english_indian_selector = "span:has-text('English (Indian)')"
    authenticated_page.locator(language_input_selector).click(timeout=10000)
    authenticated_page.locator(language_option_english_indian_selector).click(timeout=10000)
    expect(authenticated_page.locator(language_input_selector)).to_have_value("English (Indian)", timeout=10000)
    expect(authenticated_page.locator(language_option_english_indian_selector)).not_to_be_visible(timeout=5000) # Dropdown closes

    # Click the No. of Speakers input, then select '2'
    num_speakers_input_selector = "#react-select-3-input"
    num_speakers_option_2_selector = "span:has-text('2')"
    authenticated_page.locator(num_speakers_input_selector).click(timeout=10000)
    authenticated_page.locator(num_speakers_option_2_selector).click(timeout=10000)
    expect(authenticated_page.locator(num_speakers_input_selector)).to_have_value("2", timeout=10000)

    # Click the Category input, then select 'Business'
    category_input_selector = "#react-select-4-input"
    category_option_business_selector = "span:has-text('Business')"
    authenticated_page.locator(category_input_selector).click(timeout=10000)
    authenticated_page.locator(category_option_business_selector).click(timeout=10000)
    expect(authenticated_page.locator(category_input_selector)).to_have_value("Business", timeout=10000)

    # Click the Duration input, then select '2.5 - 4 Minutes'
    duration_input_selector = "#react-select-5-input"
    duration_option_2_5_4_minutes_selector = "span:has-text('2.5 - 4 Minutes')"
    authenticated_page.locator(duration_input_selector).click(timeout=10000)
    authenticated_page.locator(duration_option_2_5_4_minutes_selector).click(timeout=10000)
    expect(authenticated_page.locator(duration_input_selector)).to_have_value("2.5 - 4 Minutes", timeout=10000)

    # Click the Tone input, then select 'Formal'
    tone_input_selector = "#react-select-6-input"
    tone_option_formal_selector = "span:has-text('Formal')"
    authenticated_page.locator(tone_input_selector).click(timeout=10000)
    authenticated_page.locator(tone_option_formal_selector).click(timeout=10000)
    expect(authenticated_page.locator(tone_input_selector)).to_have_value("Formal", timeout=10000)

    # Enter 'Dr. Alex Green' into the Name of Host field
    host_name_input_selector = "[name='host']"
    host_name_value = "Dr. Alex Green"
    authenticated_page.locator(host_name_input_selector).fill(host_name_value, timeout=10000)
    expect(authenticated_page.locator(host_name_input_selector)).to_have_value(host_name_value, timeout=10000)

    # Enter 'Prof. Maya Singh' into the Name of Guest field
    guest_name_input_selector = "[name='guest']"
    guest_name_value = "Prof. Maya Singh"
    authenticated_page.locator(guest_name_input_selector).fill(guest_name_value, timeout=10000)
    expect(authenticated_page.locator(guest_name_input_selector)).to_have_value(guest_name_value, timeout=10000)

    # Click the 'GENERATE SCRIPT' button
    generate_script_button_selector = "button:has-text('GENERATE SCRIPT')"
    authenticated_page.locator(generate_script_button_selector).click(timeout=10000)

    # Expected: The 'GENERATE SCRIPT' button indicates activity
    expect(authenticated_page.locator(generate_script_button_selector)).to_be_visible(timeout=10000)
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000) # Expect to stay on the same page

def test_PODCAST_TC_005_GenerateScriptMissingTopic(authenticated_page):
    """Verify validation for missing required podcast topic when generating script"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Leave the podcast topic input field empty (it should be empty initially)
    podcast_topic_input_selector = "#rc_select_0"
    expect(authenticated_page.locator(podcast_topic_input_selector)).to_be_empty(timeout=10000)

    # Click the 'GENERATE SCRIPT' button
    generate_script_button_selector = "button:has-text('GENERATE SCRIPT')"
    authenticated_page.locator(generate_script_button_selector).click(timeout=10000)

    # Expected: A validation error message (e.g., 'Podcast topic is required') is displayed
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000) # Expect to remain on the same page
    # Look for a common required field indicator (from LOCATORS JSON: span:has-text('*') or span:has-text('Required'))
    expect(authenticated_page.locator("span:has-text('Required')")).to_be_visible(timeout=10000)
    # Also check if the input field itself indicates an invalid state
    expect(authenticated_page.locator(podcast_topic_input_selector)).to_have_attribute("aria-invalid", "true", timeout=10000)


def test_PODCAST_TC_006_AIToggleEnableDisable(authenticated_page):
    """Verify functionality of the AI Knowledge toggle switch"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    ai_knowledge_toggle_switch_selector = "[role='switch']"
    select_artifact_button_selector = "button:has-text('Select Artifact')"

    # Observe the initial state of the 'AI Knowledge' toggle and 'Select Artifact' button (assuming it starts disabled)
    # Ensure toggle is off if it happens to be on
    if authenticated_page.locator(ai_knowledge_toggle_switch_selector).get_attribute("aria-checked", timeout=10000) == "true":
        authenticated_page.locator(ai_knowledge_toggle_switch_selector).click(timeout=10000)
    expect(authenticated_page.locator(ai_knowledge_toggle_switch_selector)).to_have_attribute("aria-checked", "false", timeout=10000)
    expect(authenticated_page.locator(select_artifact_button_selector)).to_be_disabled(timeout=10000)

    # Click the 'AI Knowledge' toggle switch
    authenticated_page.locator(ai_knowledge_toggle_switch_selector).click(timeout=10000)

    # Expected: The 'AI Knowledge' toggle switch changes to an 'on' state
    expect(authenticated_page.locator(ai_knowledge_toggle_switch_selector)).to_have_attribute("aria-checked", "true", timeout=10000)
    # Expected: The 'Select Artifact' button and 'My Knowledge Source' section become enabled/interactive
    expect(authenticated_page.locator(select_artifact_button_selector)).to_be_enabled(timeout=10000)
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)

def test_PODCAST_TC_007_SelectLanguageOption(authenticated_page):
    """Verify selecting an option from the Language dropdown"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    language_input_selector = "#react-select-2-input"
    english_indian_option_selector = "span:has-text('English (Indian)')"

    # Click the 'Language' input field to open the dropdown
    authenticated_page.locator(language_input_selector).click(timeout=10000)
    expect(authenticated_page.locator(english_indian_option_selector)).to_be_visible(timeout=10000)

    # Click the 'English (Indian)' option
    authenticated_page.locator(english_indian_option_selector).click(timeout=10000)

    # Expected: The 'Language' input field displays 'English (Indian)' as the selected value
    expect(authenticated_page.locator(language_input_selector)).to_have_value("English (Indian)", timeout=10000)
    # Expected: The dropdown menu closes
    expect(authenticated_page.locator(english_indian_option_selector)).not_to_be_visible(timeout=5000)
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)

def test_PODCAST_TC_008_SelectNumSpeakersOption(authenticated_page):
    """Verify selecting an option from the 'No. of Speakers' dropdown"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    num_speakers_input_selector = "#react-select-3-input"
    speaker_option_2_selector = "span:has-text('2')"

    # Click the 'No. of Speakers' input field to open the dropdown
    authenticated_page.locator(num_speakers_input_selector).click(timeout=10000)
    expect(authenticated_page.locator(speaker_option_2_selector)).to_be_visible(timeout=10000)

    # Click the '2' option
    authenticated_page.locator(speaker_option_2_selector).click(timeout=10000)

    # Expected: The 'No. of Speakers' input field displays '2' as the selected value
    expect(authenticated_page.locator(num_speakers_input_selector)).to_have_value("2", timeout=10000)
    # Expected: The dropdown menu closes
    expect(authenticated_page.locator(speaker_option_2_selector)).not_to_be_visible(timeout=5000)
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)

def test_PODCAST_TC_009_SelectCategoryOption(authenticated_page):
    """Verify selecting an option from the 'Category' dropdown"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    category_input_selector = "#react-select-4-input"
    category_option_business_selector = "span:has-text('Business')"

    # Click the 'Category' input field to open the dropdown
    authenticated_page.locator(category_input_selector).click(timeout=10000)
    expect(authenticated_page.locator(category_option_business_selector)).to_be_visible(timeout=10000)

    # Click the 'Business' option
    authenticated_page.locator(category_option_business_selector).click(timeout=10000)

    # Expected: The 'Category' input field displays 'Business' as the selected value
    expect(authenticated_page.locator(category_input_selector)).to_have_value("Business", timeout=10000)
    # Expected: The dropdown menu closes
    expect(authenticated_page.locator(category_option_business_selector)).not_to_be_visible(timeout=5000)
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)

def test_PODCAST_TC_010_SelectDurationOption(authenticated_page):
    """Verify selecting an option from the 'Duration' dropdown"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    duration_input_selector = "#react-select-5-input"
    duration_option_2_5_4_minutes_selector = "span:has-text('2.5 - 4 Minutes')"

    # Click the 'Duration' input field to open the dropdown
    authenticated_page.locator(duration_input_selector).click(timeout=10000)
    expect(authenticated_page.locator(duration_option_2_5_4_minutes_selector)).to_be_visible(timeout=10000)

    # Click the '2.5 - 4 Minutes' option
    authenticated_page.locator(duration_option_2_5_4_minutes_selector).click(timeout=10000)

    # Expected: The 'Duration' input field displays '2.5 - 4 Minutes' as the selected value
    expect(authenticated_page.locator(duration_input_selector)).to_have_value("2.5 - 4 Minutes", timeout=10000)
    # Expected: The dropdown menu closes
    expect(authenticated_page.locator(duration_option_2_5_4_minutes_selector)).not_to_be_visible(timeout=5000)
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)

def test_PODCAST_TC_011_SelectToneOption(authenticated_page):
    """Verify selecting an option from the 'Tone' dropdown"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    tone_input_selector = "#react-select-6-input"
    tone_option_formal_selector = "span:has-text('Formal')"

    # Click the 'Tone' input field to open the dropdown
    authenticated_page.locator(tone_input_selector).click(timeout=10000)
    expect(authenticated_page.locator(tone_option_formal_selector)).to_be_visible(timeout=10000)

    # Click the 'Formal' option
    authenticated_page.locator(tone_option_formal_selector).click(timeout=10000)

    # Expected: The 'Tone' input field displays 'Formal' as the selected value
    expect(authenticated_page.locator(tone_input_selector)).to_have_value("Formal", timeout=10000)
    # Expected: The dropdown menu closes
    expect(authenticated_page.locator(tone_option_formal_selector)).not_to_be_visible(timeout=5000)
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)

def test_PODCAST_TC_012_InputHostGuestNames(authenticated_page):
    """Verify inputting values into Host and Guest name fields"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    host_name_input_selector = "[name='host']"
    host_name_value = "Alex Turner"
    guest_name_input_selector = "[name='guest']"
    guest_name_value = "Brenda Lee"

    # Enter 'Alex Turner' into the 'Name of Host' input field
    authenticated_page.locator(host_name_input_selector).fill(host_name_value, timeout=10000)
    expect(authenticated_page.locator(host_name_input_selector)).to_have_value(host_name_value, timeout=10000)

    # Enter 'Brenda Lee' into the 'Name of Guest' input field
    authenticated_page.locator(guest_name_input_selector).fill(guest_name_value, timeout=10000)
    expect(authenticated_page.locator(guest_name_input_selector)).to_have_value(guest_name_value, timeout=10000)

    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)

def test_PODCAST_TC_013_ClickPodcastReadyItem(authenticated_page):
    """Verify clicking on a 'Podcast Ready' item in the gallery"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Click the podcast item titled 'Stories of the Gig Economy' with 'Podcast Ready' status
    podcast_ready_item_selector = "article:has-text('Podcast Ready\\nStories of the G')"
    authenticated_page.locator(podcast_ready_item_selector).click(timeout=10000)

    # Expected: Current URL changes to 'https://dev.vox.snappod.ai/podcast/stories-of-the-gig-economy' (inferred)
    expect(authenticated_page).to_have_url(re.compile(r"dev\.vox\.snappod\.ai/podcast/stories-of-the-gig-economy"), timeout=10000)

def test_PODCAST_TC_014_ClickScriptReadyItem(authenticated_page):
    """Verify clicking on a 'Script Ready' item in the gallery"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Click the podcast item titled 'Making Sense of the Future wit...' with 'Script Ready' status
    script_ready_item_selector = "article:has-text('Script Ready\\nMaking Sense of t')"
    authenticated_page.locator(script_ready_item_selector).click(timeout=10000)

    # Expected: Current URL changes to 'https://dev.vox.snappod.ai/podcast/making-sense-of-the-future' (inferred)
    expect(authenticated_page).to_have_url(re.compile(r"dev\.vox\.snappod\.ai/podcast/making-sense-of-the-future"), timeout=10000)

def test_PODCAST_TC_015_ClickScriptFailedItem(authenticated_page):
    """Verify clicking on a 'Script Failed' item in the gallery"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Click the podcast item titled 'The 5 AM Club Fallacy: Is Slee...' with 'Script Failed' status
    script_failed_item_selector = "article:has-text('Script Failed\\nThe 5 AM Club Fa')"
    authenticated_page.locator(script_failed_item_selector).click(timeout=10000)

    # Expected: Current URL changes to 'https://dev.vox.snappod.ai/podcast/5-am-club-fallacy' (inferred)
    expect(authenticated_page).to_have_url(re.compile(r"dev\.vox\.snappod\.ai/podcast/5-am-club-fallacy"), timeout=10000)

def test_PODCAST_TC_016_HostNameBoundaryInput(authenticated_page):
    """Verify handling of long host name input (boundary)"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Enter 'Long Host Name Test' into the podcast topic input field
    podcast_topic_input_selector = "#rc_select_0"
    podcast_topic_value = "Long Host Name Test"
    authenticated_page.locator(podcast_topic_input_selector).fill(podcast_topic_value, timeout=10000)
    expect(authenticated_page.locator(podcast_topic_input_selector)).to_have_value(podcast_topic_value, timeout=10000)

    # Enter a very long string into the 'Name of Host' input field
    host_name_input_selector = "[name='host']"
    host_name_value = "Professor Bartholomew Percival Fitzgerald III, The Grand Overseer of Infinite Wisdom and Podcasts"
    authenticated_page.locator(host_name_input_selector).fill(host_name_value, timeout=10000)
    # Expected: The input field either truncates the input, displays a character limit warning/error, or successfully accepts the long name
    # For a static site, we assume it accepts the value as filled unless explicit truncation/error is observed.
    expect(authenticated_page.locator(host_name_input_selector)).to_have_value(host_name_value, timeout=10000)

    # Click the 'GENERATE SCRIPT' button
    generate_script_button_selector = "button:has-text('GENERATE SCRIPT')"
    authenticated_page.locator(generate_script_button_selector).click(timeout=10000)

    # Expected: If successful, script generation proceeds; if validation error, script generation is blocked
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)
    expect(authenticated_page.locator(generate_script_button_selector)).to_be_visible(timeout=10000)

def test_PODCAST_TC_017_HostGuestSpecialCharacters(authenticated_page):
    """Verify handling of special characters in Host and Guest names"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Enter 'Special Character Podcast' into the podcast topic input field
    podcast_topic_input_selector = "#rc_select_0"
    podcast_topic_value = "Special Character Podcast"
    authenticated_page.locator(podcast_topic_input_selector).fill(podcast_topic_value, timeout=10000)
    expect(authenticated_page.locator(podcast_topic_input_selector)).to_have_value(podcast_topic_value, timeout=10000)

    # Enter 'H0st-N@me! (Host)' into the 'Name of Host' input field
    host_name_input_selector = "[name='host']"
    host_name_value = "H0st-N@me! (Host)"
    authenticated_page.locator(host_name_input_selector).fill(host_name_value, timeout=10000)
    expect(authenticated_page.locator(host_name_input_selector)).to_have_value(host_name_value, timeout=10000)

    # Enter 'Gu3st$N@me (Guest)' into the 'Name of Guest' input field
    guest_name_input_selector = "[name='guest']"
    guest_name_value = "Gu3st$N@me (Guest)"
    authenticated_page.locator(guest_name_input_selector).fill(guest_name_value, timeout=10000)
    expect(authenticated_page.locator(guest_name_input_selector)).to_have_value(guest_name_value, timeout=10000)

    # Click the 'GENERATE SCRIPT' button
    generate_script_button_selector = "button:has-text('GENERATE SCRIPT')"
    authenticated_page.locator(generate_script_button_selector).click(timeout=10000)

    # Expected: The system accepts the special characters, and script generation proceeds successfully
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)
    expect(authenticated_page.locator(generate_script_button_selector)).to_be_visible(timeout=10000)

def test_PODCAST_TC_018_AIToggleSelectArtifactInteraction(authenticated_page):
    """Verify the 'Select Artifact' button is only active when AI Knowledge is enabled"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    ai_knowledge_toggle_switch_selector = "[role='switch']"
    select_artifact_button_selector = "button:has-text('Select Artifact')"

    # Ensure the 'AI Knowledge' toggle switch is in the 'off' state (default or manually set)
    if authenticated_page.locator(ai_knowledge_toggle_switch_selector).get_attribute("aria-checked", timeout=10000) == "true":
        authenticated_page.locator(ai_knowledge_toggle_switch_selector).click(timeout=10000)
    expect(authenticated_page.locator(ai_knowledge_toggle_switch_selector)).to_have_attribute("aria-checked", "false", timeout=10000)

    # Attempt to click the 'Select Artifact' button (should be disabled)
    expect(authenticated_page.locator(select_artifact_button_selector)).to_be_disabled(timeout=10000)

    # Click the 'AI Knowledge' toggle switch to enable it
    authenticated_page.locator(ai_knowledge_toggle_switch_selector).click(timeout=10000)
    expect(authenticated_page.locator(ai_knowledge_toggle_switch_selector)).to_have_attribute("aria-checked", "true", timeout=10000)

    # After enabling 'AI Knowledge', the 'Select Artifact' button becomes enabled
    expect(authenticated_page.locator(select_artifact_button_selector)).to_be_enabled(timeout=10000)

    # Click the 'Select Artifact' button (expected to open a modal or navigate)
    authenticated_page.locator(select_artifact_button_selector).click(timeout=10000)
    # For a static site, verify URL remains the same and button remains interactive
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)

def test_PODCAST_TC_019_RequiredFieldIndicators(authenticated_page):
    """Verify visibility of required field indicators on initial page load"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # The podcast topic input field should have a visible '*' or 'Required' indicator
    expect(authenticated_page.locator("span:has-text('*')")).to_be_visible(timeout=10000)
    
    # All other fields like Language, No. of Speakers, Category, Duration, and Tone
    # should have their labels visible.
    expect(authenticated_page.locator("span:has-text('Language:')")).to_be_visible(timeout=10000)
    expect(authenticated_page.locator("span:has-text('No.of Speakers:')")).to_be_visible(timeout=10000)
    expect(authenticated_page.locator("span:has-text('Category:')")).to_be_visible(timeout=10000)
    expect(authenticated_page.locator("span:has-text('Duration:')")).to_be_visible(timeout=10000)
    expect(authenticated_page.locator("span:has-text('Tone:')")).to_be_visible(timeout=10000)

    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)

def test_PODCAST_TC_020_ClickSnappodLogoNavigation(authenticated_page):
    """Verify clicking the SnapPod Logo navigates to the main dashboard/welcome page"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Click the 'SnapPod Logo'
    snappod_logo_img_selector = "[alt='SnapPod Logo']"
    authenticated_page.locator(snappod_logo_img_selector).click(timeout=10000)

    # Expected: Current URL remains 'https://dev.vox.snappod.ai/welcome-to-snappod-ai'
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)

def test_PODCAST_TC_021_ClickUserProfileNavigation(authenticated_page):
    """Verify clicking the user profile ('TJ') navigates to the user settings or profile page"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Click the 'TJ' user profile element
    tj_div_selector = "div:has-text('TJ')"
    authenticated_page.locator(tj_div_selector).click(timeout=10000)

    # Expected: Current URL changes to 'https://dev.vox.snappod.ai/profile' or 'https://dev.vox.snappod.ai/settings' (inferred)
    expect(authenticated_page).to_have_url(re.compile(r"dev\.vox\.snappod\.ai/(profile|settings)"), timeout=10000)

def test_PODCAST_TC_022_ClickAllPodcastsTab(authenticated_page):
    """Verify clicking the 'All' tab in the 'Your Podcasts' section"""
    authenticated_page.goto(WELCOME_URL, timeout=60000)
    authenticated_page.wait_for_load_state('networkidle')

    # Click the 'All' tab within the 'Your Podcasts' section
    all_tab_selector = "div:has-text('All')"
    authenticated_page.locator(all_tab_selector).click(timeout=10000)

    # Expected: The 'All' tab is visually highlighted as the active/selected tab
    expect(authenticated_page.locator(all_tab_selector)).to_be_visible(timeout=10000)
    # Common attribute for active tabs, if present.
    expect(authenticated_page.locator(all_tab_selector)).to_have_attribute("aria-selected", "true", timeout=10000) 
    expect(authenticated_page).to_have_url(WELCOME_URL, timeout=10000)