# Wasp Role-Based Authentication

## Background
You have an existing Wasp project that includes basic user authentication. Your task is to implement role-based access control by adding a `role` field to the `User` entity and restricting access to a specific admin page.

## Requirements
1. Update the `User` entity in `main.wasp` to include a `role` field of type `String` with a default value of `"USER"`.
2. Create an `AdminPage` component in `src/AdminPage.tsx` that displays an `<h1>` element with the exact text `"Admin Dashboard"`.
3. In `main.wasp`, add a `route` for path `/admin` pointing to the `AdminPage`.
4. Set `authRequired: true` for the `AdminPage` in `main.wasp`.
5. In `src/AdminPage.tsx`, verify the user's role. If the user's role is not `"ADMIN"`, redirect them to the home page (`/`) immediately upon rendering.

## Constraints
- **Project path**: `/home/user/wasp-project`
- **Start command**: `wasp db migrate-dev --name role_migration && wasp start`
- **Port**: 3000
- **Environment**: Wasp CLI and Node.js are pre-installed. The project is already created.