import os
import subprocess
import time
import socket
import pytest
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/wasp-project"

def wait_for_port(port, timeout=120):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

def test_main_wasp_updates():
    main_wasp_path = os.path.join(PROJECT_DIR, "main.wasp")
    with open(main_wasp_path) as f:
        content = f.read()
    
    # Check for role field in User entity
    assert "role" in content, "Expected 'role' field in User entity."
    assert "String" in content, "Expected 'role' field to be of type String."
    assert "\"USER\"" in content or "'USER'" in content, "Expected default value 'USER' for role field."
    
    # Check for admin route and page
    assert "/admin" in content, "Expected a route for '/admin'."
    assert "authRequired" in content and "true" in content, "Expected 'authRequired: true' for the Admin page."

def test_admin_page_component_exists():
    admin_page_path = os.path.join(PROJECT_DIR, "src", "AdminPage.tsx")
    assert os.path.isfile(admin_page_path), f"AdminPage component not found at {admin_page_path}"
    with open(admin_page_path) as f:
        content = f.read()
    assert "Admin Dashboard" in content, "Expected 'Admin Dashboard' in AdminPage.tsx"

@pytest.fixture(scope="module")
def start_app():
    # Run migrations
    subprocess.run(
        ["wasp", "db", "migrate-dev", "--name", "final_migration"],
        cwd=PROJECT_DIR,
        check=True
    )
    
    # Start the app
    process = subprocess.Popen(
        ["wasp", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the client (3000) and server (3001) to be ready
    if not wait_for_port(3000) or not wait_for_port(3001):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on required ports.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_browser_verification(start_app):
    reason = "The Admin page should be restricted to users with the ADMIN role."
    truth = "Navigate to http://localhost:3000/signup. Create a new user with username `testuser` and password `password123`. The user will have the default role `\"USER\"`. Log in as `testuser`. Navigate to http://localhost:3000/admin. Verify that the browser redirects to http://localhost:3000/ and does not display `\"Admin Dashboard\"`. Use the sqlite3 CLI to update the `User` table in `.wasp/db/dev.db` to change `testuser`'s role to `\"ADMIN\"`. Navigate to http://localhost:3000/admin again. Verify that the page now loads and displays the `<h1>Admin Dashboard</h1>` heading."

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_verification"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
