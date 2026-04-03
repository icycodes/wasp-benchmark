FROM pochi-browser-verification-base

RUN npm i -g @wasp.sh/wasp-cli@latest

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Wasp project with basic user authentication in /home/user/wasp-project."

# Create a basic Wasp project with auth
RUN cd /home/user && \
    wasp new wasp-project && \
    cd wasp-project && \
    cat > main.wasp <<'EOF'
app waspProject {
  wasp: {
    version: "^0.15.0"
  },
  title: "Wasp Role Auth",
  auth: {
    userEntity: User,
    methods: {
      usernameAndPassword: {}
    },
    onAuthFailedRedirectTo: "/login"
  }
}

route RootRoute { path: "/", to: MainPage }
page MainPage {
  component: import { MainPage } from "@src/MainPage"
}

route LoginRoute { path: "/login", to: LoginPage }
page LoginPage {
  component: import { LoginPage } from "@src/LoginPage"
}

route SignupRoute { path: "/signup", to: SignupPage }
page SignupPage {
  component: import { SignupPage } from "@src/SignupPage"
}

entity User {
  id Int @id @default(autoincrement())
}
EOF

# Create basic pages
RUN cd /home/user/wasp-project && \
    mkdir -p src && \
    cat > src/MainPage.tsx <<'EOF'
import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth, logout } from 'wasp/client/auth'

export const MainPage = () => {
  const { data: user } = useAuth()
  return (
    <div>
      <h1>Home</h1>
      {user ? (
        <div>
          <p>Welcome, {user.username}!</p>
          <button onClick={logout}>Logout</button>
        </div>
      ) : (
        <p>Please <Link to="/login">login</Link> or <Link to="/signup">signup</Link></p>
      )}
    </div>
  )
}
EOF

RUN cd /home/user/wasp-project && \
    cat > src/LoginPage.tsx <<'EOF'
import React from 'react'
import { LoginForm } from 'wasp/client/auth'

export const LoginPage = () => {
  return (
    <div>
      <h1>Login</h1>
      <LoginForm />
    </div>
  )
}
EOF

RUN cd /home/user/wasp-project && \
    cat > src/SignupPage.tsx <<'EOF'
import React from 'react'
import { SignupForm } from 'wasp/client/auth'

export const SignupPage = () => {
  return (
    <div>
      <h1>Signup</h1>
      <SignupForm />
    </div>
  )
}
EOF

# Container contents:
#   - Wasp CLI installed globally.
#   - /home/user/wasp-project  — basic Wasp project with auth
#   - main.wasp with User entity and basic routing

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
