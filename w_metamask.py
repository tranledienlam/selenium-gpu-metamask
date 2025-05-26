# version 20250402
import argparse
from selenium.webdriver.common.by import By

from browser_automation import BrowserManager, Node
from utils import Utility

EXTENSION_URL = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn'

class Setup:
    def __init__(self, node: Node, profile) -> None:
        self.node = node
        self.profile = profile
        
    def _run(self):
        # Chuyển đến trang extension
        self.node.go_to(f'{EXTENSION_URL}/home.html', method="get")
        self.node.new_tab('https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn')

class Auto:
    def __init__(self, node: Node, profile: dict) -> None:
        self.driver = node._driver
        self.node = node
        self.profile_name = profile.get('profile_name')
        self.password = profile.get('password')
        self.seeds = profile.get('seeds')

    def _handle_duplicate_tabs(self):
        """Xử lý trường hợp MetaMask tự mở nhiều tab"""
        # Lấy tất cả các tab hiện tại
        Utility.wait_time(5)
        all_handles = self.driver.window_handles
        
        if len(all_handles) > 2:
            self.node.log(f'Phát hiện {len(all_handles)} tab đang mở')
            metamask_tabs = []
            
            # Tìm tất cả các tab MetaMask
            for handle in all_handles:
                self.driver.switch_to.window(handle)
                if EXTENSION_URL in self.driver.current_url:
                    metamask_tabs.append(handle)
            
            # Nếu có nhiều tab MetaMask, giữ lại tab đầu tiên và đóng các tab còn lại
            if len(metamask_tabs) > 2:
                self.node.log(f'Phát hiện {len(metamask_tabs)} tab MetaMask, đang dọn dẹp...')
                # Giữ lại tab đầu tiên
                first_tab = metamask_tabs[0]
                # Đóng các tab còn lại
                for handle in metamask_tabs[1:]:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
                # Chuyển về tab đầu tiên
                self.driver.switch_to.window(first_tab)
                self.node.log('Đã đóng các tab MetaMask trùng lặp')
                return True
        return False

    def metamask_loaded(self) -> bool:
        """Kiểm tra MetaMask đã load xong chưa"""
        metamask_loaded =  self.node.find(By.CSS_SELECTOR, '.app', timeout=60)
        if not metamask_loaded:
            self.node.log('MetaMask không tải được, thử tải lại trang')
            self.node.reload_tab(wait=2)
            metamask_loaded = self.node.find(By.CSS_SELECTOR, '.app', timeout=60)
            
        if not metamask_loaded:
            self.node.snapshot('MetaMask vẫn không tải được sau khi reload')
            return False
            
        self.node.log('MetaMask đã tải thành công')
        return True

    def import_wallet(self) -> bool:
        """Import ví mới từ seed phrase"""
        if not self.seeds:
            self.node.snapshot('Không tìm thấy seed trong data.txt')
            return False
            
        self.seeds = self.seeds.split(' ')
        
        # Click vào nút import
        self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="onboarding-terms-checkbox"]')
        self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="onboarding-import-wallet"]')

        self.node.find_and_click(By.CSS_SELECTOR, '[id="metametrics-opt-in"]')
        self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="metametrics-i-agree"]')
        
        # Đợi form và import 12 seed
        for i in range(12):
            self.node.find_and_input(By.CSS_SELECTOR, f'[id="import-srp__srp-word-{i}"]', self.seeds[i], delay=0, wait=0.1)

        # Click confirm sau khi nhập seed
        self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="import-srp-confirm"]')

        # Tạo mật khẩu mới
        self.node.find_and_input(By.CSS_SELECTOR, '[data-testid="create-password-new"]', self.password)
        self.node.find_and_input(By.CSS_SELECTOR, '[data-testid="create-password-confirm"]', self.password)
        self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="create-password-terms"]')
        self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="create-password-import"]')

        # Kiểm tra màn hình "Your wallet is ready"
        wallet_ready = self.node.find(By.XPATH, "//h2[contains(text(), 'Your wallet is ready')]", timeout=10)
        if wallet_ready:
            # Click nút Done để hoàn tất
            self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="onboarding-complete-done"]')
            self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="pin-extension-next"]')
            self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="pin-extension-done"]')
        else:
            self.node.log('Không tìm thấy màn hình "Your wallet is ready"')
        
        # Đợi và kiểm tra đã vào được màn hình chính
        home_screen = self.node.find(By.CSS_SELECTOR, '[data-testid="account-overview__asset-tab"]')
        if not home_screen:
            self.node.snapshot('Import ví thất bại - Không vào được màn hình chính')
            return False
            
        self.node.log('Import ví thành công')
        return True

    def unlock_wallet(self) -> bool:
        """Unlock ví với mật khẩu"""
        # Nhập mật khẩu để unlock
        self.node.find_and_input(By.CSS_SELECTOR, '[data-testid="unlock-password"]', self.password, None,0.1)
        self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="unlock-submit"]')
        
        # Kiểm tra màn hình "Your wallet is ready"
        wallet_ready = self.node.find(By.XPATH, "//h2[contains(text(), 'Your wallet is ready')]", timeout=10)
        if wallet_ready:
            # Click nút Done để hoàn tất
            self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="onboarding-complete-done"]')
            self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="pin-extension-next"]')
            self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="pin-extension-done"]')
        else:
            self.node.log('Không tìm thấy màn hình "Your wallet is ready"')
        
        # Đợi và kiểm tra đã vào được màn hình chính
        home_screen = self.node.find(By.CSS_SELECTOR, '[data-testid="account-overview__asset-tab"]')
        if not home_screen:
            self.node.snapshot('Unlock ví thất bại - Không vào được màn hình chính')
            return False
            
        self.node.log('Unlock ví thành công')
        return True
    
    def confirm(self, text: str = 'Cancel') -> bool:
        """
        Tìm và click nút có nội dung `text` trên giao diện extension, sau đó trở lại tab hiện tại.

        Args:
            text (str): Nội dung của nút cần click (ví dụ: 'Cancel', 'Confirm').

        Returns:
            bool: True nếu click thành công, False nếu không.
        """
        done = False
        current_window = self.driver.current_window_handle

        # Chuyển sang tab chứa extension hoặc mở mới nếu chưa có
        if not self.node.switch_tab(f'{EXTENSION_URL}'):
            self.node.new_tab(f'{EXTENSION_URL}/home.html')
        else:
            self.node.reload_tab()

        # Tìm phần chứa các nút
        footer_box = self.node.find(By.CSS_SELECTOR, '[class*="footer"], [class="footerBox"]')
        if not footer_box:
            self.node.log('❌ Không tìm thấy footer chứa các nút.')
        else:
            buttons = self.node.find_all(By.TAG_NAME, 'button', parent_element=footer_box, wait=0, timeout=0)
            if not buttons:
                self.node.log('❌ Không tìm thấy nút nào trong footer.')
            else:
                # Tìm nút theo nội dung
                for button in buttons:
                    if button.text.strip().lower() == text.strip().lower():
                        if self.node.click(button):
                            self.node.log(f'✅ Đã click button: {text}')
                            done = True
                        else:
                            self.node.log(f'❌ Không thể click button: {text}')
                        break
                else:
                    self.node.log(f'❌ Không tìm thấy button với nội dung: "{text}"')

        # Quay lại tab ban đầu
        self.driver.switch_to.window(current_window)
        return done

    
    def change_network(self, network_name: str, rpc_url: str, chain_id: str, symbol: str, block_explorer: str = None):
        """Thay đổi mạng lưới"""
        # Kiểm tra và chọn network
        current_network = self.node.get_text(By.CSS_SELECTOR, '[data-testid="network-display"]')
        
        if network_name in current_network:
            self.node.log(f"Đang ở network {network_name}, không cần chuyển")
            return True
        else:
            self.node.find_and_click(By.CSS_SELECTOR, '[data-testid="network-display"]')
            
            # Kiểm tra xem có network_name trong danh sách không
            if not self.node.find_and_click(By.CSS_SELECTOR, f'[data-testid="{network_name}"]', timeout=10):
                actions_add_network = [
                    # add a custom network
                    (self.node.find_and_click, By.XPATH, '//button[text()="Add a custom network"]'),
                    # nhập network name
                    (self.node.find_and_input, By.CSS_SELECTOR, '[data-testid="network-form-network-name"]', network_name, None, 0.1),
                    (self.node.find_and_click, By.CSS_SELECTOR, '[data-testid="test-add-rpc-drop-down"]'),
                    (self.node.find_and_click, By.XPATH, '//button[text()="Add RPC URL"]'),
                    (self.node.find_and_input, By.CSS_SELECTOR, '[data-testid="rpc-url-input-test"]', rpc_url, None, 0.1),
                    (self.node.find_and_click, By.XPATH, '//button[text()="Add URL"]'),
                    # nhập chain id
                    (self.node.find_and_input, By.CSS_SELECTOR, '[data-testid="network-form-chain-id"]', chain_id, None, 0.1),
                    # nhập symbol
                    (self.node.find_and_input, By.CSS_SELECTOR, '[data-testid="network-form-ticker-input"]', symbol, None, 0.1),
                    # nhập block explorer
                    (self.node.press_key, 'Tab'),
                    (self.node.press_key, 'Enter'),
                    (self.node.find_and_click, By.XPATH, '//button[text()="Add a block explorer URL"]'),
                    (self.node.find_and_input, By.CSS_SELECTOR, '[data-testid="explorer-url-input"]', block_explorer, False),
                    (self.node.find_and_click, By.XPATH, '//button[text()="Add URL"]'),
                    # save network
                    (self.node.find_and_click, By.XPATH, '//button[text()="Save"]'),
                    # chuyển qua network mới
                    (self.node.find_and_click, By.CSS_SELECTOR, '[data-testid="network-display"]'),
                    (self.node.find_and_click, By.CSS_SELECTOR, f'[data-testid="{network_name}"]', None, None, 10)
                ]
                self.node.execute_chain(actions=actions_add_network, message_error=f'Add network {network_name} thất bại')

            current_network = self.node.get_text(By.CSS_SELECTOR, '[data-testid="network-display"]')
            if network_name in current_network:
                self.node.log(f'Đã chuyển sang network {network_name}')
                return True
            else:
                self.node.snapshot(f'Chuyển network thất bại')
                return False

    def _run(self):

        # Chuyển đến trang extension
        self.node.go_to(f'{EXTENSION_URL}/home.html', method="get")
        
        # Kiểm tra MetaMask đã load xong chưa bằng cách tìm các phần tử UI đặc trưng
        if not self.metamask_loaded():
            self.node.snapshot('MetaMask không tải được')
            return False
        # Xử lý trường hợp có nhiều tab
        self._handle_duplicate_tabs()

        # Kiểm tra xem có cần unlock ví không
        unlock_page = self.node.find(By.CSS_SELECTOR, '[data-testid="unlock-page"]', timeout=10)
        if unlock_page:
            self.node.log('Phát hiện cần unlock ví')
            self.unlock_wallet()
        else:
            # Kiểm tra xem có cần import ví mới không
            import_button = self.node.find(By.CSS_SELECTOR, '[data-testid="onboarding-import-wallet"]', timeout=10)
            if import_button:
                self.node.log('Phát hiện cần import ví mới')
                self.import_wallet()
            else:
                self.node.snapshot('Không tìm thấy màn hình import hoặc unlock')
                return False
        if self.node.find(By.XPATH, '//h2[contains(text(), "Protect your funds")]', timeout=15):
            self.node.find_and_click(By.XPATH, '//button[contains(text(), "Got it")]')

        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', action='store_true', help="Chạy ở chế độ tự động")
    parser.add_argument('--headless', action='store_true', help="Chạy trình duyệt ẩn")
    parser.add_argument('--disable-gpu', action='store_true', help="Tắt GPU")
    args = parser.parse_args()

    profiles = Utility.get_data('profile_name', 'password', 'seeds')
    
    if not profiles:
        print("Không có dữ liệu để chạy")
        exit()

    browser_manager = BrowserManager(AutoHandlerClass=Auto, SetupHandlerClass=Setup)
    browser_manager.config_extension('meta-wallet-*.crx')
    # browser_manager.run_browser(profiles[1])
    browser_manager.run_terminal(
        profiles=profiles,
        max_concurrent_profiles=4,
        block_media=True,
        auto=args.auto,
        headless=args.headless,
        disable_gpu=args.disable_gpu,
    )