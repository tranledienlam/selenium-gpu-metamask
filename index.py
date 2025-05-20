
import argparse
import re
from selenium.webdriver.common.by import By

from browser_automation import BrowserManager, Node
from utils import Utility
from w_metamask import Auto as MetamaskAuto, Setup as MetamaskSetup

class Setup:
    def __init__(self, node: Node, profile) -> None:
        self.node = node
        self.profile = profile
        self.metamask_setup = MetamaskSetup(node, profile)
        
    def _run(self):
        self.metamask_setup._run()
        self.node.new_tab('https://token.gpu.net/?ref=YW0IAN', method="get")

class Auto:
    def __init__(self, node: Node, profile: dict) -> None:
        self.driver = node._driver
        self.node = node
        self.metamask_auto = MetamaskAuto(node, profile)
        self.profile_name = profile.get('profile_name')
    
    def is_connected(self):
        h1_els = self.node.find_all(By.TAG_NAME, 'h1')
        for h1 in h1_els:
            if h1 and "Connect a Wallet".lower() in h1.text.lower():
                self.node.log(f"Cần connect ví")

        buttons = self.node.find_all(By.TAG_NAME, 'button')
        for button in buttons:
            if button.text.startswith('0x'):
                self.node.log(f'Đã connect ví')
                return True
        
        return False
    
    def is_popup(self):
        h3_els = self.node.find_all(By.XPATH, '//div[div[h3]]', wait=10)
        for h3 in h3_els:
            if 'Connect Your Twitter Account'.lower() in h3.text.lower():
                self.node.snapshot(f'Thực hiện connect X')
                self.node.find_and_click(By.TAG_NAME, 'button')
                return True
        return False
    
    def _run(self):
        self.metamask_auto._run()
        self.node.new_tab('https://token.gpu.net/?ref=YW0IAN', method="get")

        #connect
        if not self.is_connected():
            self.node.find_and_click(By.XPATH, '//div[contains(text(),"MetaMask")]')
            self.metamask_auto.confirm('Connect')
            self.metamask_auto.confirm('Approve')
            self.node.find_and_click(By.XPATH, '//div[contains(text(), "Sign message")]')
            self.metamask_auto.confirm('Confirm')
            if not self.is_connected():
                self.node.log('Connect thất bại')
                return False
        
        self.is_popup()
        
        #check-in
        try_check_in = 1
        while True:
            buttons = self.node.find_all(By.TAG_NAME, 'button')
            countdown = None
            for button in buttons:
                if button.text:
                    match = re.search(r'(\d{1,2})h (\d{1,2})m (\d{1,2})s', button.text)
                    if match:
                        hours, minutes, seconds = match.groups()
                        countdown = f'Giờ: {hours}, Phút: {minutes}, Giây: {seconds}'

            if countdown:
                self.node.snapshot(f'Quay lại check-in sau: {countdown}')
            
            for button in buttons:
                if "Say GM".lower() in button.text.lower():
                    self.node.click(button)
                    self.node.reload_tab()
                    Utility.wait_time(5)
            
            try_check_in -= 1
            if try_check_in < 0:
                self.node.snapshot(f'Check-in bị lỗi')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', action='store_true', help="Chạy ở chế độ tự động")
    parser.add_argument('--headless', action='store_true', help="Chạy trình duyệt ẩn")
    parser.add_argument('--disable-gpu', action='store_true', help="Tắt GPU")
    args = parser.parse_args()

    browser_manager = BrowserManager(AutoHandlerClass=Auto, SetupHandlerClass=Setup)
    
    profiles = Utility.get_data('profile_name', 'password', 'seeds')
    if not profiles:
        print("Thực hiện fake data")
        # Fake profile data khi file data.txt rỗng hoặc không tồn tại
        profiles = Utility.fake_data('profile_name', 30)
        browser_manager.run_fake_data(
            profiles=profiles,
            max_concurrent_profiles=8,
            block_media=True,
            headless=args.headless,
            disable_gpu=args.disable_gpu,
        )
    else:
        browser_manager.config_extension('meta-wallet-*.crx')
        browser_manager.run_terminal(
            profiles=profiles,
            max_concurrent_profiles=4,
            block_media=True,
            auto=args.auto,
            headless=args.headless,
            disable_gpu=args.disable_gpu,
        )