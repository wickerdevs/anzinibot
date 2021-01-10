# INSTAGRAM MODULE
logging_in_text = 'Initiating driver and logging in...'
# Follow Module
waiting_scrape_text = 'Scraping followers...'
restricted_account_text = 'Your account has been either restricted or blocked due to sospicious activity. Please open Instagram and log in and use it normally for at least 24 hours before trying again.'
starting_follows_text = '{}\'s followers have been scraped. Starting to follow {} users...'
followed_user_text = 'Interacted with {} user(s) out of {}...'
invalid_credentials_text = 'Your instagram credentials are incorrect... Please log int again with /login'
verification_code_necessary = 'Your instagram account has 2FA turned on... In order for the bot to work, please turn it off.'
private_account_error_text = 'The account {} is private - hence it\'s impossible to get it\'s followers. Please try again with another account using /follow'
operation_error_text = 'There was an error when executing your request... The developer has been informed. The bot has interacted with {} users.'
follow_successful_text = 'Operation successful! The bot has interacteed with {} of {}\'s followers!'


# START COMMAND
welcome = 'Hi! I will be your own Instagram Bot!\n\nLet\'s start by logging into your instagram account. Press Next to continue.'
end = 'Alright! You can now use this bot with the account <b>{}</b> as well! Press the button below to view a list of available commands:'
startup_done = 'Seems you already have gone through the initial bot startup. You can edit your settings with the button below:'


# ACCOUNT COMMAND
checking_accounts_connection = 'Checking account connection...'
no_connection = 'No instagram connection found.'
problem_connecting = 'There was a problem when checking the connection... The developer has been notified.'
connection_found_text = '<b>Instagram Account</b>\nYou are currently logged into Instagram with the account <a href="https://www.instagram.com/{}/">{}</a>\nYou can switch account or log out entirely with the buttons below.'
switch_account_text = 'Select below the account you\'d like to switch to, or log into another account:'
no_accounts_available_text = 'No other accounts available. Click the button below to add another account to the selection.'
switched_account_text = 'You switched to the <a href="https://www.instagram.com/{}/">{}</a> account. The bot\'s commands will now affect that account.'

# Scrape Data
confirm_clear_data_text = 'Are you sure you want to delete all scraped data (e.g. scraped followers, etc)?'
scraped_data_cleared_text = 'All of your scraped data has been cleared.'
cancelled_clear_data_text = 'Operation cancelled. None of your scraped data has been cleared.'


#INSTAGRAM LOGIN CONVERSATION
checking_ig_status = 'Checking instagram connection...'
user_logged_in_text = 'You are already logged in!'
checking_ig_credentials_text = 'Instagram is not connected. Checking credentials...'
logging_in_with_credentials_text = 'Instagram credentials found. Logging in...'
input_verification_code_text = 'Send below the verification code generated by your Authenticator App or that was sent to you via SMS by Instagram:'
input_security_code_text = 'Send below the security code that was sent to you via SMS by Instagram (The code might take up to a couple of minutes to get sent by Instagram\'s servers...): '
input_security_code_text_email = 'Send below the security code that was sent to you by Instagram via email to the email address tied to your account (The code might take up to a couple of minutes to get sent by Instagram\'s servers...):'
security_code_resent = 'The security code has been sent again via {} (attempt {})... Type it below:'
input_ig_username_text = 'Input below your instagram username:'
checking_user_vadility_text = 'Checking username vadility...'
invalid_user_text = 'The username you have provided, {}, does not exist. Please try again with a correct instagram username:'
input_password_text = 'Input your instagram password below:'
attempting_login_text = 'Attempting to log into instagram...'
invalid_password_text = 'The password you provided, {}, is incorrect. Please try again:'
login_successful_text = 'You successfully logged into your instagram account! \nNow please enter below the message you would like me to send to your new followers:'
validating_code_text = 'Validating instagram 2FA security code...'
invalid_security_code_text = 'The security code you provided is invalid. Please try again below:'
cancelled_instagram_text = 'Instagram log in procedure has been cancelled.'


# INSTAGRAM LOG OUT COMMAND
logging_out = 'Logging out of instagram...'
instagram_loggedout_text = 'Instagram log out successful! To log in again, use /login'
error_loggingout_text = 'There was an error when trying to log out of instagram... Try again later or contact a developer.'


# SEND DM CONVERSATION
dm_queue_full_text = 'A DM task is already running. Please wait for that task to finish first, before launching another.'
select_scrape_text = 'Select below the selection of users to send your DM to:'
incorrect_user_text = 'The username <b>{}</b> is invalid. Please try again with another instagram username:'
input_message_text = 'Input below the message you would like me to send. (Try avoiding emojis or special characters as they might not get recognized by instagram)'
input_accounts_text = 'Send below a text file containing a list of credentials of the accounts the bot should use for this operation:'
confirm_dms_text = 'Are you sure you want to send your message to {} users?'
enqueing_dms_text = 'Enqueuing DM tasks...'
enqueued_dms_text = 'DMs task enqueued successfully.'
# Instagram
inform_messages_status_text = 'Sending messages to {} users... {} sent so far...'


# TAG CONVERSATION
tag_queue_full_text = 'A Tag task is already running. Please wait for that task to finish first, before launching another.'
select_tag_scrape_text = 'Select below the selection of users to tag under your post:'
input_post_url_text = 'Input below the url link of the target post below, as follows: \n<code>https://www.instagram.com/p/CIqua7YHtha/</code>:'
checking_post_text = 'Checking post url...'
invalid_post_url_text = 'The url you entered is not valid. Please try again: '
confirm_tags_text = 'Are you sure you want to tag {} users under your post?'
enqueing_tags_text = 'Enqueuing DM tasks...'
enqueued_tags_text = 'TAGs task enqueued successfully.'
# Instagram
inform_tags_status_text = 'Attaching {} tags to <a href="{}">this post</a>... {} sent so far...'
error_getting_post_text = 'There was an error loading the post with shortcode <b>{}</b>... Please try again later.'


# SCRAPE CONVERSATION
select_account_text = 'Insert below the username of the account you want to scrape:'
error_when_checking_account = 'There was an error when checking {}\'s vadility... The account might be inexistent or private. Please choose another account:'
select_count_text = 'Select below the amount of users you would like to send your message to:'
select_tag_count_text = 'Select below the amount of users you would like to tag under your post:'
launching_operation_text = 'Starting operation...'
scrape_followers_callback_text = 'Scraped {} followers...'
follow_cancelled_text  = 'The request cancelled.'


# SETTINGS CONVERSATION
select_setting_text = 'Select below which setting you would like to edit:'
select_text_text = 'Input below the comment text you would like me to send on the posts of the users you interact with - note that emojis and special characters, as well as markdown formatting might not translate to Instagram formatting.'
edited_text_text = 'The default comment text to greet new followers has been edited successfully!'
cancelled_editing_settings = 'Settings have not been altered.'


# GENERAL
incorrect_command_text = 'The command or message \'{}\' is not a recognized command...'
invalid_text_text = 'Please make sure the message does not contain special characters (such emojis), and try again'
# MULTIPLE UTILITIES
error_checking_connection = 'There was a problem in authenticating the client. Please try again or contact @davidwickerhf.'
incorrect_credentials_error = 'When sending the messages the client wasn\'t able to log into the account due to incorrect credentials... Please check and edit your credentials with /instagram\n{} Send DM requests completed so far.'
suspicious_login = 'There was a problem connecting to the client when processing your request... Please log out with /iglogout and then log back into the client with /instagram\n{} Send DM requests completed so far.'
verification_necessary = 'Your account has 2FA turned on. In order to process this request, you must turn 2FA off from your account.\n{} Send DM requests completed so far.'
restricted_account = 'Your account has been restricted from Instagram! \nLog into your account manually and try to engage with the website. Try to send this request again after at least 24 hours.\n{} Send DM requests completed so far.'
blocked_account = 'Your account has been blocked! \nLog into your account from your own device to unblock the account - then, wait at least 24 hours before sending another request\n{} Send DM requests completed so far.'
not_admin_text = 'Sorry, this command can only be used by an admin.'
not_authorized_text = 'You are not authorized to use this bot\'s features'
not_logged_in_text = 'To use this command you must log in first with /login'
no_settings_found_text = 'No settings where found... Please use /start to set up the bot first.'

# HELP COMMAND
help_text = '<b>FF INSTA BOT</b>\n/account - Check instagram connection(s)\n\n/login - Log into another instagram account\n\n/logout - Log out of current instagram\n\n/dm - Send DMs\n\n/tag - Tag users to a post\n\n/start - Run Bot Setup'
