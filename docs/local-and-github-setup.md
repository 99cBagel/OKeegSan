# Local, GitHub, and iPhone setup

## Recommended account arrangement

- **Repository owner:** GitHub account `99cBagel`
- **ChatGPT sign-in:** `presenter.simon@gmail.com` is fine; it does not need to
  match the GitHub account email.
- **Access bridge:** While signed into that ChatGPT account, connect/authorize the
  GitHub app and grant it access to the private `99cBagel/OKeegSan` repository.
- **Commit identity:** Configure this repository (not all repositories) with the
  name and a verified email belonging to `99cBagel`. A GitHub-provided `noreply`
  address is preferable if the personal email should remain private.

Authentication decides which GitHub account can push. `git user.name` and
`user.email` only label commits; they do not sign you into GitHub.

## One-time local setup

From the `OKeegSan` folder:

```powershell
git init -b main
git config user.name "99cBagel"
git config user.email "YOUR_99CBAGEL_VERIFIED_OR_NOREPLY_EMAIL"
gh auth login --hostname github.com --web --git-protocol https
gh auth status
git add .
git commit -m "Initialize O'KeegSan activity companion"
gh repo create OKeegSan --private --source . --remote origin --push
```

When the browser opens for `gh auth login`, sign into GitHub as `99cBagel` and
verify the account shown before approving access.

## Connect from ChatGPT on iPhone

1. Push the repository to GitHub first.
2. In ChatGPT, open **Settings**, then **Apps** or **Plugins** (the label depends on
   the available product experience), and select GitHub.
3. Authorize using GitHub account `99cBagel`; choose access to selected repositories
   and select the private `OKeegSan` repo.
4. Allow several minutes for a new private repository to appear.
5. In a supported chat/agent experience, reference the repo and exact prompt path.

The ChatGPT sign-in email and GitHub sign-in email can differ. Repository access is
controlled by the GitHub authorization and selected-repository permission.
The ChatGPT GitHub connection is read-only; use Codex or local Git to save changes.

## Normal maintenance

```powershell
git status
git add .
git commit -m "Add 20260828 run log"
git push
```

Before committing a generated log, review it for inaccurate values, secrets, and
precise private location information.
