import pexpect
import time
import requests

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Notification sent to Telegram.")
        else:
            print(f"Failed to send notification. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Telegram notification: {e}")

def main():
    wallet_name = "c3"
    net_uid = "30"
    hot_key_list = ["h3"]  # List of hot keys
    password = "111111"  # Replace with your actual password

    # Telegram bot configuration
    bot_token = ""  # Replace with your bot token
    chat_id = "1137861791"      # Replace with your chat ID

    for hot_key_name in hot_key_list:
        success = False
        while not success:
            command = f"btcli s register --wallet.name {wallet_name} --hotkey {hot_key_name} --netuid {net_uid}"
            
            try:
                print(f"Executing command for hotkey: {hot_key_name}")
                # Spawn the command
                process = pexpect.spawn(command, encoding='utf-8')
                
                # Expect the "y/n" prompt and send "y"
                process.expect("y/n")
                process.sendline("y")
                
                # Expect the password prompt and send the password
                process.expect("Password:")
                process.sendline(password)
                
                # Wait for the process to complete
                process.expect(pexpect.EOF)
                output = process.before
                print("Command executed successfully:")
                print(output)
                
                # Extract UID from the output
                if "✅ Registered on netuid" in output:
                    success = True
                    # Extract UID using string parsing
                    uid_line = next((line for line in output.splitlines() if "✅ Registered on netuid" in line), None)
                    if uid_line:
                        uid = uid_line.split("UID")[1].strip()
                        print(f"Extracted UID: {uid}")
                    
                    # Send Telegram notification
                    message = f"Hotkey {hot_key_name} registered successfully to netuid {net_uid} with UID {uid}!"
                    send_telegram_message(bot_token, chat_id, message)
                else:
                    print(f"Retrying for hotkey {hot_key_name}...")
                    time.sleep(5)  # Wait before retrying
            except pexpect.exceptions.EOF:
                print(f"Unexpected end of file for hotkey {hot_key_name}. Retrying...")
                time.sleep(5)  # Wait before retrying
            except pexpect.exceptions.TIMEOUT:
                print(f"Timeout occurred for hotkey {hot_key_name}. Retrying...")
                time.sleep(5)  # Wait before retrying  # Wait before retrying

if __name__ == "__main__":
    main()