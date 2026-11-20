#!/usr/bin/env bash
# vm.sh: a disposable Multipass "VPS" for rehearsing a project's hosting/ scripts on a Mac.
#
#   vm.sh up [VM] [MEMORY]             fresh Ubuntu 24.04 VM (default hosting-test, 1G); allows your
#                                      SSH key, trusts its host key, prints DEPLOY_HOST=ubuntu@IP
#   vm.sh ip [VM]                      print its IPv4
#   vm.sh push APP [VM] [REPO]         snapshot REPO's working tree (uncommitted files included) as a
#                                      commit outside your branches; push it as main (plus a snap-* tag)
#                                      to the bare repo ~/APP.git on the VM; print the sha
#   vm.sh grant-deploy-key APP [VM]    let the server's deploy key (made by provision) read ~/APP.git
#   vm.sh down [VM]                    delete the VM and forget its host key
#
# The VM's ubuntu user has passwordless sudo, like a cloud VPS image. Your branch, index and
# working tree are never changed. Env: VM_SSH_KEY (public key to allow, default ~/.ssh/id_rsa.pub;
# its private half must be one ssh tries by default, or loaded in ssh-agent).
set -euo pipefail

VM_DEFAULT=hosting-test
KEY=${VM_SSH_KEY:-$HOME/.ssh/id_rsa.pub}

die() { printf 'vm.sh: %s\n' "$*" >&2; exit 1; }

forget_host() { # forget_host IP: drop its known_hosts entries
  local kh="$HOME/.ssh/known_hosts" tmp
  [ -f "$kh" ] || return 0
  ssh-keygen -R "$1" >/dev/null 2>&1 && return 0
  # ssh-keygen refuses to touch a file with any malformed line; drop only lines for exactly this IP
  tmp=$(mktemp)
  awk -v ip="$1" '$1 != ip && $1 != "["ip"]:22" && $0 != "# "ip":22" && index($0, "# "ip":22 ") != 1' "$kh" > "$tmp"
  cat "$tmp" > "$kh"
  rm -f "$tmp"
}

vm_ip() {
  local ip
  ip=$(multipass info "$1" 2>/dev/null | awk '/^IPv4:/ {print $2; exit}')
  [ -n "$ip" ] && [ "$ip" != -- ] || die "no IPv4 for VM '$1' (multipass list)"
  printf '%s\n' "$ip"
}

cmd_up() {
  local vm=${1:-$VM_DEFAULT} mem=${2:-1G} ip
  ! multipass info "$vm" >/dev/null 2>&1 || die "VM '$vm' already exists (vm.sh down $vm first)"
  [ -f "$KEY" ] || die "no public key at $KEY (set VM_SSH_KEY)"
  multipass launch 24.04 --name "$vm" --cpus 1 --memory "$mem" --disk 10G
  multipass exec "$vm" -- bash -c 'printf "%s\n" "$1" >> ~/.ssh/authorized_keys' _ "$(cat "$KEY")"
  ip=$(vm_ip "$vm")
  # Multipass reuses IPs, so an older VM's host key may still be on file for this one.
  forget_host "$ip"
  ssh-keyscan -t ed25519 "$ip" 2>/dev/null | grep -v '^#' >> "$HOME/.ssh/known_hosts"
  ssh -o BatchMode=yes "ubuntu@$ip" 'sudo -n true' || die "can't ssh to ubuntu@$ip with passwordless sudo"
  printf 'VM %s is up. DEPLOY_HOST=ubuntu@%s\n' "$vm" "$ip"
}

cmd_push() {
  local app=${1:?usage: vm.sh push APP [VM] [REPO]} vm=${2:-$VM_DEFAULT} repo=${3:-.}
  local ip root idx sha
  ip=$(vm_ip "$vm")
  root=$(git -C "$repo" rev-parse --show-toplevel)
  idx=$(mktemp)
  cp "$(git -C "$root" rev-parse --path-format=absolute --git-path index)" "$idx"
  sha=$(cd "$root" && export GIT_INDEX_FILE="$idx" && git add -A &&
        git commit-tree "$(git write-tree)" -p HEAD -m "vm.sh snapshot of the working tree")
  rm -f "$idx"
  ssh -o BatchMode=yes "ubuntu@$ip" "[ -d ~/$app.git ] || git init -q --bare -b main ~/$app.git"
  # The snap-* tag keeps every snapshot fetchable, so older ones can be deployed to test rollback.
  git -C "$root" push -q -f "ubuntu@$ip:$app.git" "$sha:refs/heads/main" "$sha:refs/tags/snap-${sha:0:7}"
  printf '%s\n' "$sha"
}

cmd_grant_deploy_key() {
  local app=${1:?usage: vm.sh grant-deploy-key APP [VM]} vm=${2:-$VM_DEFAULT}
  ssh -o BatchMode=yes "ubuntu@$(vm_ip "$vm")" "
    k=~/.ssh/deploy_$app.pub
    [ -f \"\$k\" ] || { echo 'no deploy key yet: provision first' >&2; exit 1; }
    grep -qxF \"\$(cat \"\$k\")\" ~/.ssh/authorized_keys || cat \"\$k\" >> ~/.ssh/authorized_keys
    echo 'deploy key can read ~/$app.git'"
}

cmd_down() {
  local vm=${1:-$VM_DEFAULT} ip
  ip=$(vm_ip "$vm" 2>/dev/null || true)
  multipass delete --purge "$vm"
  [ -z "$ip" ] || forget_host "$ip"
  printf 'VM %s deleted\n' "$vm"
}

case "${1:-}" in
  up)               shift; cmd_up "$@" ;;
  ip)               shift; vm_ip "${1:-$VM_DEFAULT}" ;;
  push)             shift; cmd_push "$@" ;;
  grant-deploy-key) shift; cmd_grant_deploy_key "$@" ;;
  down)             shift; cmd_down "$@" ;;
  *) sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
