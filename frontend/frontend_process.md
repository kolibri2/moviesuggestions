### Process used for setting up a frontend

##### 1. Create a new feature branch in Git.

a branch /feature/react-frontend was added to git.

##### 2. Install Node.js and ensure correct file types.

Installed through webpage though npm. Verify .ts and .tsx are associated with Typescript.

##### 3. Scaffold React+TS project.

```
cd path/to/moviesuggestions
npx create-react-app frontend --template typescript
```

##### 4. Add frontend folder to Git and commit.

##### 5. Configure run configs

Run>edit configs
name: frontend:dev
package.json: point to frontend/package.json
command: start for CRA

##### 6. Link backend

Add ``` "proxy": "http://localhost:8000",``` in package.json (same url as fastapi backend.)
