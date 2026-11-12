---
name: vps-hosting-test
description: >-
  Rehearse a project's VPS hosting end to end on a disposable Multipass Ubuntu VM on the user's Mac: fresh box, first provision, deploy, re-provision, --check, a second deploy, a rollback, and the health check through nginx. Also readies a test VM for the user to click around by hand in a browser (a .test name, trusted HTTPS via mkcert, an admin account) so passkeys and the Django admin work. Use after changing hosting/ scripts or docs in greenfield-boilerplate (or a project built from it), after changing vpshome's base server setup, when the user asks to test, rehearse or dry-run hosting, provisioning or deploys locally, or when they want to try the deployed site themselves. Not for deploying to a real server.
---

# VPS hosting test

Proves that a project's `hosting/` scripts take a brand-new server to a working, re-deployable app, and that what changed didn't break that. The box is a Multipass VM: real Ubuntu with systemd, its own IP, and an `ubuntu` user with passwordless sudo and no password, which is how most cloud VPS images ship.

Read the project's `docs/vps-hosting.md` and `hosting/.env.example` first. The scripts evolve; they are the source of truth for flags and settings, not this file. What this skill adds is the test procedure and the traps found while building it.

Helper: [`scripts/vm.sh`](scripts/vm.sh) (`up`, `ip`, `push`, `grant-deploy-key`, `down`). Run it by its absolute path from the project root.

## Ground rules

- **Never commit, push to a real remote, or touch the user's branch, index or working tree.** `vm.sh push` snapshots the working tree into a commit outside every branch and pushes it only to a bare repo on the VM.
- **Don't edit `~/.ssh/config`.** Use `DEPLOY_HOST=ubuntu@<ip>`; `vm.sh up` puts the VM's host key in `known_hosts`. The user may have their own `Host` entries for the VM, and those are theirs.
- **Never rewrite a VM user's `authorized_keys` with a filter** (`grep -v "$pattern"`): an empty pattern matches every line and removes all keys, including Multipass's own (which `multipass exec`/`shell` need). Only append. If keys do get lost, `multipass exec VM -- ...` still works only while Multipass's key is intact; its public key is in `/var/lib/cloud/instance/vendor-data.txt` on the VM.
- **Anything needing the user's Mac password is theirs to run** (`/etc/hosts`, recovering a stuck Multipass). Give them the exact command with the `!` prefix.
- **You have no terminal.** Interactive prompts can't be exercised; pass a complete settings file or `-y`, and tell the user which prompts went untested.
- **Run long steps in the background** with output to log files in the scratchpad, and grep the logs instead of reading them whole.
- **Fix bugs in the working tree only**, say which file and line, re-run `vm.sh push`, and repeat from the failing step. Finish with one clean run on a fresh VM before calling it done.

## Before starting

1. `command -v multipass` and `multipass list`. Not installed: the user runs `brew install --cask multipass`. An existing VM with the same name: ask before deleting it, or use another name.
2. Confirm the project has `hosting/provision.sh`, `hosting/deploy.sh` and `hosting/.env.example`, and that `hosting/.env.*` is gitignored (`git check-ignore hosting/.env.test`).
3. Note what changed (`git status`, `git diff --stat`) in the project and, if relevant, in vpshome, so the report can say what was exercised.

## The run

`APP` is the project name on the server (e.g. `gfb`), `SKILL` the path to this skill's folder, `S` the scratchpad.

1. **Fresh box.** Always a new VM for a full run; an upgraded box hides first-run bugs (a missing `/srv/APP/.env`, missing `pnpm`, first-time sudo).
   ```bash
   $SKILL/scripts/vm.sh up hosting-test 1G
   ```
   1 GB matches a small VPS. 512 MB stalls on first boot and leaves the instance in state `Unknown` (see Recovery).

2. **Base server setup, when vpshome changed.** Follow vpshome's README order on the VM as far as it applies (the `ubuntu` user stands in for the admin user): `./sync.sh ubuntu@IP`, then `ssh -t ubuntu@IP ./bootstrap.sh`, then the scriptable parts of `SERVER_SETUP.md`. Skip sshd lockdown steps that could cut off `ubuntu@IP` key login. Not changed: skip; the hosting scripts need only a sudo user with key login.

3. **Code to deploy**, as the server would fetch it:
   ```bash
   SHA1=$($SKILL/scripts/vm.sh push APP hosting-test .)
   ```

4. **Settings**: write `hosting/.env.test` with every key the first run would ask for, so nothing prompts:
   ```
   DEPLOY_HOST=ubuntu@<ip from vm.sh up>
   DEPLOY_NAME=APP
   DEPLOY_DOMAIN=APP.test
   DEPLOY_EMAIL=test@example.com
   DEPLOY_DB=postgres
   DEPLOY_REPO=ubuntu@localhost:/home/ubuntu/APP.git
   DEPLOY_BRANCH=main
   ```
   The repo URL points the server at the bare repo on itself, so no GitHub deploy key is needed. Use `.test` domains (`.local` clashes with mDNS).

5. **Sequence**, each step logged to `$S/<step>.log`. Expected results:

   | Step | Command | Pass when |
   |---|---|---|
   | first provision | `./hosting/provision.sh --env hosting/.env.test` | exit 0; only nginx/HTTPS (no DNS), App and Start are `skipped` |
   | grant key | `$SKILL/scripts/vm.sh grant-deploy-key APP` | prints that the key can read the repo |
   | first deploy | `./hosting/deploy.sh --env hosting/.env.test` | tests pass, build passes, ends `Deployed <sha> (main)` |
   | re-provision | `./hosting/provision.sh --env hosting/.env.test` | exit 0, every step `ok` except HTTPS; no `wrote` or `set` lines in the log (idempotent) |
   | check | `./hosting/provision.sh --env hosting/.env.test --check` | exit 0, no `FAIL` lines |
   | second deploy | `SHA2=$(vm.sh push APP …)`, then deploy | `Deployed <SHA2>` |
   | rollback | `./hosting/deploy.sh --env hosting/.env.test ${SHA1:0:12}` | `Deployed <SHA1>`; `/srv/APP/REVISION` starts with `SHA1` |
   | health via nginx | `ssh ubuntu@IP 'curl -s -w " %{http_code} %{content_type}" -H "Host: APP.test" http://127.0.0.1/health/'` | JSON from Django with 200, not the SPA's `index.html` |

   Also confirm on the server: settings live only in `/srv/APP/.env` (the `DEPLOY_*` block), and `ls -a /srv/APP` shows no stray config files.

6. **Optional, when relevant to the change**: `DEPLOY_DB=external`; `DEPLOY_REPO=none` with `./hosting/deploy-rsync.sh --env hosting/.env.test`; a TLS run with [`mkcert`](https://github.com/FiloSottile/mkcert) (`mkcert -cert-file APP.test.pem -key-file APP.test-key.pem APP.test`, install them on the VM as `/etc/letsencrypt/live/APP.test/fullchain.pem` (644) and `privkey.pem` (600), re-provision, expect `https is configured`). Needed to try passkeys or the Django admin in a browser.

## Manual testing in a browser

When the user wants to use the site themselves (after a run, or on a VM that's already up), get it to where passkeys would work, not just to where the page loads. Passkeys (WebAuthn) need all of:

- **a name, not an IP**: browsers refuse passkeys on IP addresses;
- **https, with a certificate the browser trusts**: Chrome turns passkeys off on a page with a certificate error, even after the user clicks through it. Plain http works only on `localhost`. The Django admin needs https too (production cookies are secure-only);
- **that name in Django's `ALLOWED_HOSTS`**: provision sets it from `DEPLOY_DOMAIN`, so `DEPLOY_DOMAIN` must be the name the user types.

Steps. The user runs anything that needs their Mac password (`!` prefix):

1. **Name**: check `grep -n APP.test /etc/hosts`. If it's missing, the user runs `! echo "IP APP.test" | sudo tee -a /etc/hosts`. Multipass on macOS has no DNS names for VMs.
2. **Local CA, once per Mac**: if `command -v mkcert` fails or `$(mkcert -CAROOT)/rootCA.pem` doesn't exist, the user runs `! brew install mkcert && mkcert -install`. The `certutil is not available ... Firefox` warning only matters for Firefox (below).
3. **Certificate**, created in the scratchpad and installed where certbot would put it:
   ```bash
   cd "$S" && mkcert -cert-file APP.test.pem -key-file APP.test-key.pem APP.test
   scp -q APP.test.pem APP.test-key.pem ubuntu@IP:
   ssh ubuntu@IP 'sudo install -d /etc/letsencrypt/live/APP.test &&
     sudo install -m 644 APP.test.pem /etc/letsencrypt/live/APP.test/fullchain.pem &&
     sudo install -m 600 APP.test-key.pem /etc/letsencrypt/live/APP.test/privkey.pem && rm APP.test*.pem'
   rm "$S/APP.test-key.pem"
   ```
4. **Re-provision** (`./hosting/provision.sh --env hosting/.env.test`): expect `https is configured (certificate present)` in the nginx step and `Done. https://APP.test/`.
5. **Verify from the Mac**, with no `Host` header tricks, as the browser will:
   ```bash
   curl -s -o /dev/null -w '%{http_code} verify=%{ssl_verify_result}\n' https://APP.test/        # 200 verify=0
   curl -s https://APP.test/api/v1/auth/config/
   curl -s -o /dev/null -w '%{http_code}\n' -X POST -H 'Origin: https://APP.test' \
     https://APP.test/api/v1/auth/passkeys/login/begin/                                          # 200
   curl -s -o /dev/null -w '%{http_code}\n' -I http://APP.test/                                  # 301 to https
   ```
   `verify=0` means the macOS trust store accepts the certificate. A 403 from `passkeys/login/begin/` means `ALLOWED_HOSTS` doesn't include the name.
6. **Account**: the password prompt is interactive, so the user runs `! ssh -t ubuntu@IP 'sudo -u APP /srv/APP/bin/manage add_user you@example.com --name You --admin'`. Check whether one exists first with `bin/manage shell -c` and a user count.
7. **Tell the user**:
   - **Open `https://APP.test` in Chrome (or Safari).** Firefox keeps its own trust store. Even after `brew install nss`, a second `mkcert -install` and a restart, it didn't trust the mkcert CA in testing, so don't promise it. If they insist, `security.enterprise_roots.enabled = true` in `about:config` (untested here) makes Firefox use the macOS store.
   - **What to try**: sign in with the password; an `--admin` account must add a passkey straight away. Log out, sign in with the passkey, then open Admin in the account menu. The admin path is in `grep ^ADMIN_URL /srv/APP/.env`, and provision prints it.
   - **Stale passkeys**: passkeys belong to `APP.test`. After the VM is deleted, the test passkey stays in Chrome's password manager or iCloud Passwords until they remove it.

Leave the VM running afterwards unless the user says otherwise.

## Report

A table of steps with pass/fail, then each bug: symptom, cause, file:line, the fix (working tree only), and whether it would hit a real server. Then what wasn't exercised (interactive prompts, rsync path, TLS, vpshome steps skipped). Then offer, don't do:

- to get it ready for them to try in a browser, with https and passkeys working (see Manual testing in a browser);
- to commit the fixes;
- to tear down: `$SKILL/scripts/vm.sh down hosting-test`, plus the `/etc/hosts` line if added.

## Traps found so far

Check these first when something fails; each was a real bug or a real snag.

| Symptom | Cause |
|---|---|
| provision stops at once: `sudo access is required` | `sudo -v` asks for a password even with `NOPASSWD: ALL` when the user has none (Ubuntu cloud images). Must try `sudo -n true` first |
| Node step: `/usr/bin/env: 'node': No such file or directory` | `corepack` run under `sudo`, whose PATH lacks the new Node; run it as `node corepack` |
| re-run leaves the server without `pnpm` | "already installed" check looked only for `node` and `corepack` |
| deploy dies at `sudo -u "" backup-db`, or health check sends the wrong Host | config from the deployed commit overrode the server's own name/domain |
| editing project settings has no effect after the first provision | a server-side config file pinned every key |
| `/health/` returns `text/html` 200 through nginx | no nginx location for it, so the SPA fallback answers; uptime monitors always see green |
| `--check` always FAILs on `venv/.lock` | uv creates it mode 0666 on purpose |
| Mac side: `!v: unbound variable` | macOS `/bin/bash` 3.2: `printf -v VAR ''` (empty format) assigns nothing. Mac-side code must work in bash 3.2 |
| first provision exits 1 with no message | a lookup in a not-yet-existing `/srv/APP/.env` failed as the last command of an `a \|\| b` list under `set -e` |
| `Pseudo-terminal will not be allocated` | harmless: `ssh -t` without a local terminal |
| browser says passkeys aren't available, or nothing happens | page is on an IP, plain http, or has a certificate warning (often Firefox not trusting the mkcert CA). See Manual testing in a browser |
| `passkeys/login/begin/` answers 403 | the hostname isn't in `ALLOWED_HOSTS`: `DEPLOY_DOMAIN` differs from the name in the browser |
| a reused VM IP fails host-key checks after `vm.sh down`/`up` | `ssh-keygen -R` refuses to edit a `known_hosts` that has any malformed line; `vm.sh` falls back to removing only that IP's lines. Mention the malformed line to the user rather than fixing it |

## Recovery

- **Instance stuck in `Unknown`, can't delete it** (usually 512 MB): its QEMU process is still running. The user runs `! sudo kill -9 <pid>` (find it: `ps aux | grep qemu-system`), then `! sudo launchctl kickstart -k system/com.canonical.multipassd`, waits ~20 s, and `multipass delete --purge VM`. `cannot connect to the multipass socket` right after a restart means the daemon is still spinning on the old VM: the kill didn't take.
- **Last resort**: with the daemon stopped (`sudo launchctl bootout system/com.canonical.multipassd`), remove the VM from `/var/root/Library/Application Support/multipassd/qemu/vault/instances/VM/` and from both `multipassd-vm-instances.json` and `vault/multipassd-instance-image-records.json`, then `sudo launchctl bootstrap system /Library/LaunchDaemons/com.canonical.multipassd.plist`. Deleting only the folder leaves the name taken.
- **`Permission denied (publickey)` for a user the user added themselves**: compare their `authorized_keys` line with their real `~/.ssh/*.pub`; a shortened placeholder (`AAAA...`) copied from docs is a common cause.
