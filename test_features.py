"""
Playwright를 사용한 Contact App 기능 테스트 및 스크린샷 캡처
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import time

# 스크린샷 저장 경로
DESKTOP = Path.home() / "Desktop"
SCREENSHOT_DIR = DESKTOP / "contact_app_tests"
SCREENSHOT_DIR.mkdir(exist_ok=True)

# 테스트 데이터
TEST_USERNAME = f"testuser_{int(time.time())}"
TEST_PASSWORD = "Test@12345"
TEST_EMAIL = f"test_{int(time.time())}@example.com"

async def test_contact_app():
    """연락처 관리 앱 기능 테스트"""

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})

        await page.goto("http://127.0.0.1:8000/")
        await page.wait_for_load_state("networkidle")

        try:
            # ============================================
            # Test A: 회원가입 페이지
            # ============================================
            print("📸 Test A: 회원가입 페이지...")
            await page.screenshot(path=str(SCREENSHOT_DIR / "testA_signup_page.png"))

            # 회원가입 폼 입력
            await page.fill('input[name="username"]', TEST_USERNAME)
            await page.fill('input[name="password"]', TEST_PASSWORD)
            await page.screenshot(path=str(SCREENSHOT_DIR / "testA_signup_filled.png"))

            # 회원가입 버튼 클릭
            signup_btn = await page.query_selector("button:has-text('Sign Up')")
            if signup_btn:
                await signup_btn.click()
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(1)

            # ============================================
            # Test B: 로그인 확인
            # ============================================
            print("📸 Test B: 로그인 완료...")
            await page.screenshot(path=str(SCREENSHOT_DIR / "testB_logged_in.png"))

            # 로그아웃 전에 main 페이지 대기
            await page.wait_for_selector("[data-auth='true']", timeout=5000).catch(lambda e: None)
            await asyncio.sleep(1)

            # ============================================
            # Test C: 카테고리 추가
            # ============================================
            print("📸 Test C: 카테고리 추가...")

            # 카테고리 추가 버튼 찾기
            category_add_btn = await page.query_selector("button:has-text('Add Category')")
            if category_add_btn:
                await category_add_btn.click()
                await asyncio.sleep(0.5)

                # 모달에서 카테고리 이름 입력
                category_input = await page.query_selector("input[placeholder*='category'], input[placeholder*='Category']")
                if category_input:
                    await category_input.fill("Friends")
                    await page.screenshot(path=str(SCREENSHOT_DIR / "testC_category_add.png"))

                    # 저장 버튼 클릭
                    save_btn = await page.query_selector("button:has-text('Save'), button:has-text('Add'), button:has-text('Create')")
                    if save_btn:
                        await save_btn.click()
                        await asyncio.sleep(1)

            # ============================================
            # Test D: 연락처 추가
            # ============================================
            print("📸 Test D: 연락처 추가...")

            # 연락처 추가 버튼 찾기
            contact_add_btn = await page.query_selector("button:has-text('Add Contact'), button:has-text('New Contact')")
            if contact_add_btn:
                await contact_add_btn.click()
                await asyncio.sleep(0.5)
                await page.screenshot(path=str(SCREENSHOT_DIR / "testD_contact_form.png"))

                # 연락처 정보 입력
                inputs = await page.query_selector_all("input[type='text'], input[type='email'], input[type='tel']")
                if len(inputs) >= 3:
                    await inputs[0].fill("John Doe")  # 이름
                    await inputs[1].fill("john@example.com")  # 이메일
                    await inputs[2].fill("010-1234-5678")  # 전화번호
                    await page.screenshot(path=str(SCREENSHOT_DIR / "testD_contact_filled.png"))

                    # 저장 버튼 클릭
                    save_btn = await page.query_selector("button:has-text('Save'), button:has-text('Add'), button:has-text('Create')")
                    if save_btn:
                        await save_btn.click()
                        await asyncio.sleep(1)

            # ============================================
            # Test E: 연락처 목록 조회
            # ============================================
            print("📸 Test E: 연락처 목록...")
            await page.screenshot(path=str(SCREENSHOT_DIR / "testE_contact_list.png"))

            # ============================================
            # Test F: 연락처 수정
            # ============================================
            print("📸 Test F: 연락처 수정...")

            # 첫 번째 연락처의 수정 버튼 찾기
            edit_btn = await page.query_selector("button:has-text('Edit'), a:has-text('Edit')")
            if edit_btn:
                await edit_btn.click()
                await asyncio.sleep(0.5)
                await page.screenshot(path=str(SCREENSHOT_DIR / "testF_contact_edit.png"))

                # 연락처 정보 수정
                inputs = await page.query_selector_all("input[type='text'], input[type='email'], input[type='tel']")
                if len(inputs) >= 1:
                    await inputs[0].fill("")
                    await inputs[0].fill("John Smith")
                    await page.screenshot(path=str(SCREENSHOT_DIR / "testF_contact_edit_filled.png"))

                    # 저장 버튼 클릭
                    save_btn = await page.query_selector("button:has-text('Save'), button:has-text('Update')")
                    if save_btn:
                        await save_btn.click()
                        await asyncio.sleep(1)

            # ============================================
            # Test G: 연락처 삭제
            # ============================================
            print("📸 Test G: 연락처 삭제...")

            # 삭제 버튼 찾기
            delete_btn = await page.query_selector("button:has-text('Delete')")
            if delete_btn:
                await delete_btn.click()
                await asyncio.sleep(0.5)
                await page.screenshot(path=str(SCREENSHOT_DIR / "testG_delete_confirm.png"))

                # 확인 버튼 클릭
                confirm_btn = await page.query_selector("button:has-text('Confirm'), button:has-text('Yes'), button:has-text('Delete')")
                if confirm_btn:
                    await confirm_btn.click()
                    await asyncio.sleep(1)

            # ============================================
            # Test H: 로그아웃
            # ============================================
            print("📸 Test H: 로그아웃...")

            # 로그아웃 버튼 찾기
            logout_btn = await page.query_selector("button:has-text('Logout')")
            if logout_btn:
                await logout_btn.click()
                await asyncio.sleep(1)
                await page.screenshot(path=str(SCREENSHOT_DIR / "testH_logout.png"))

            # ============================================
            # Test I: 로그아웃 후 로그인 페이지
            # ============================================
            print("📸 Test I: 로그인 페이지로 복귀...")
            await page.screenshot(path=str(SCREENSHOT_DIR / "testI_back_to_login.png"))

            print(f"\n✅ 모든 테스트 완료!")
            print(f"📁 스크린샷 저장 위치: {SCREENSHOT_DIR}")

        except Exception as e:
            print(f"❌ 테스트 중 오류: {e}")
            await page.screenshot(path=str(SCREENSHOT_DIR / "error_screenshot.png"))

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_contact_app())
