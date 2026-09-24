#!/bin/sh
# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Install the Spacecraft Software theme extensions into VS Code-family
# editors. POSIX sh; the Nushell twin is install-extensions.nu. Run with
# --help for usage.

set -u

PROG=install-extensions
PROG_VERSION=1.0.0
REPO=Spacecraft-Software/Theme
PUBLISHER=spacecraft-software
WEBSITE=https://Theme.SpacecraftSoftware.org/
SIGNER=Mohamed.Hammad@SpacecraftSoftware.org
SIGNER_KEY='ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICAwZ9xGo7DR5LMIyJv6VoyoRrcgZXLPF76zdSYrQT/f'
# `antigravity` is the legacy Antigravity 1.x IDE command; Antigravity 2.0
# reuses that name for an app that takes no extensions, so it is never
# auto-detected, only installed into when named with --editor.
AUTO_EDITORS='code code-flatpak codium codium-flatpak antigravity-ide'

EXIT_FAIL=1
EXIT_USAGE=2
EXIT_NOT_FOUND=3
EXIT_VERIFY=6

INVOCATION="$PROG $*"
OPT_SOURCE=auto
OPT_METHOD=auto
OPT_RELEASE=latest
OPT_EDITORS=
OPT_EXTDIR=
OPT_SKIP_SIG=0
DRY_RUN=0
QUIET=0
VERBOSE=0
FORMAT=

usage() {
	cat <<EOF
Usage: $PROG [OPTIONS]

Install the Spacecraft Software colour themes into every detected
VS Code-family editor: VS Code, VSCodium, Antigravity, Antigravity IDE,
native or Flatpak.

Options:
  --source <src>      Where the extension comes from:
                        marketplace  the editor's own gallery (VS Code
                                     Marketplace or Open VSX), by ID
                        local        the VSIX files beside this script
                        release      a GitHub release of $REPO
                        auto         local when run from a checkout,
                                     otherwise marketplace (default)
  --release <tag>     Release tag for --source release (default: latest)
  --editor <list>     Comma-separated editors to target (default: all
                      detected): $AUTO_EDITORS
                      antigravity (the Antigravity 1.x IDE) only when named
  --method <m>        cli     the editor's --install-extension
                      unpack  extract the VSIX into the extensions
                              directory and register it
                      auto    cli, or unpack when the editor has no
                              usable CLI (default; Nix-wrapped
                              Antigravity launches its GUI instead)
  --extensions-dir <dir>
                      Use this extensions directory (one editor only)
  --insecure-skip-signature
                      Check SHA-256 sums without verifying their
                      signature (checksums are still enforced)
  --dry-run           Show what would be installed; change nothing
  --json              Machine-readable output (same as --format json)
  --format <fmt>      json (the only structured format supported)
  -q, --quiet         Errors only on stderr
  -v, --verbose       Everything on stderr, including editor CLI output
  --no-color          Accepted for compatibility; output is never coloured
  -h, --help          Show this help
  --version           Show version

Exit codes:
  0 success   1 an editor failed   2 usage error   3 not found
  6 checksum or signature verification failed

Examples:
  $PROG --source local --dry-run
  $PROG --source release --editor code,codium --json
  $PROG --editor antigravity-ide --method unpack --source local

Maintained by Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
$WEBSITE
EOF
}

now() { date -u +%Y-%m-%dT%H:%M:%SZ; }

json_str() {
	printf '"%s"' "$(printf '%s' "$1" | tr '\n\r' '  ' | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/	/\\t/g')"
}

agent_env() {
	[ -n "${AI_AGENT:-}" ] || [ -n "${AGENT:-}" ]
}

ci_env() {
	case ${CI:-} in '' | 0 | false | FALSE | False) return 1 ;; *) return 0 ;; esac
}

# Severity floor: error > warn > ok > info.
floor_allows() {
	if [ "$QUIET" = 1 ]; then
		[ "$1" = error ]
	elif [ "$VERBOSE" = 1 ]; then
		return 0
	elif agent_env; then
		case $1 in error | warn) return 0 ;; *) return 1 ;; esac
	else
		[ "$1" != info ]
	fi
}

# diag <severity> <CODE> <message> [hint]
diag() {
	floor_allows "$1" || return 0
	if [ "$FORMAT" = json ]; then
		if [ "$1" = error ]; then
			return 0
		fi
		{
			printf '{"diagnostic":{"severity":%s,"code":%s,"message":%s' \
				"$(json_str "$1")" "$(json_str "$2")" "$(json_str "$3")"
			[ -n "${4:-}" ] && printf ',"hint":%s' "$(json_str "$4")"
			printf ',"timestamp":%s,"command":%s}}\n' "$(json_str "$(now)")" "$(json_str "$INVOCATION")"
		} >&2
	else
		case $1 in
		error) tag=ERROR ;; warn) tag=WARN ;; ok) tag=OK ;; *) tag=INFO ;;
		esac
		printf '[%s] %s\n' "$tag" "$3" >&2
		[ -n "${4:-}" ] && printf '  hint: %s\n' "$4" >&2
	fi
	return 0
}

# Output-mode cascade: explicit flag, agent/CI environment, TTY, else json.
# Sets FORMAT unless a flag already did; not called in a subshell, since
# the TTY test must see the real stdout.
detect_format() {
	[ -n "$FORMAT" ] && return 0
	if agent_env || ci_env; then
		FORMAT=json
	elif [ -t 1 ]; then
		FORMAT=text
	else
		FORMAT=json
	fi
}

# die <exit> <CODE> <message> <hint>
die() {
	detect_format
	if [ "$FORMAT" = json ]; then
		printf '{"error":{"code":%s,"exit_code":%s,"message":%s,"hint":%s,"timestamp":%s,"command":%s,"docs_url":%s}}\n' \
			"$(json_str "$2")" "$1" "$(json_str "$3")" "$(json_str "$4")" \
			"$(json_str "$(now)")" "$(json_str "$INVOCATION")" "$(json_str "$WEBSITE")" >&2
	else
		printf '[ERROR] %s\n  hint: %s\n' "$3" "$4" >&2
	fi
	exit "$1"
}

need_value() {
	[ $# -ge 2 ] || die "$EXIT_USAGE" USAGE "option $1 needs a value" "$PROG --help"
}

while [ $# -gt 0 ]; do
	case $1 in
	--source) need_value "$@"; OPT_SOURCE=$2; shift ;;
	--source=*) OPT_SOURCE=${1#*=} ;;
	--release) need_value "$@"; OPT_RELEASE=$2; shift ;;
	--release=*) OPT_RELEASE=${1#*=} ;;
	--editor) need_value "$@"; OPT_EDITORS=$2; shift ;;
	--editor=*) OPT_EDITORS=${1#*=} ;;
	--method) need_value "$@"; OPT_METHOD=$2; shift ;;
	--method=*) OPT_METHOD=${1#*=} ;;
	--extensions-dir) need_value "$@"; OPT_EXTDIR=$2; shift ;;
	--extensions-dir=*) OPT_EXTDIR=${1#*=} ;;
	--insecure-skip-signature) OPT_SKIP_SIG=1 ;;
	--dry-run) DRY_RUN=1 ;;
	--json) FORMAT=json ;;
	--format) need_value "$@"; FORMAT=$2; shift ;;
	--format=*) FORMAT=${1#*=} ;;
	-q | --quiet) QUIET=1 ;;
	-v | --verbose) VERBOSE=1 ;;
	--no-color | --color=never) ;;
	-h | --help) usage; exit 0 ;;
	--version) VERSION_ASKED=1 ;;
	*) die "$EXIT_USAGE" USAGE "unknown argument: $1" "$PROG --help" ;;
	esac
	shift
done

detect_format

case $FORMAT in
json | text) ;;
*) bad=$FORMAT; FORMAT=text; die "$EXIT_USAGE" USAGE "unsupported format: $bad (only json)" "$PROG --json" ;;
esac

[ "$QUIET" = 1 ] && [ "$VERBOSE" = 1 ] &&
	die "$EXIT_USAGE" USAGE "--quiet and --verbose are mutually exclusive" "$PROG --quiet"

if [ "${VERSION_ASKED:-0}" = 1 ]; then
	if [ "$FORMAT" = json ]; then
		printf '{"metadata":{"tool":"%s","version":"%s","command":%s,"timestamp":"%s","maintainer":"Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>","website":"%s"},"data":{"version":"%s"}}\n' \
			"$PROG" "$PROG_VERSION" "$(json_str "$INVOCATION")" "$(now)" "$WEBSITE" "$PROG_VERSION"
	else
		printf '%s %s\nMaintained by Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>\n%s\n' \
			"$PROG" "$PROG_VERSION" "$WEBSITE"
	fi
	exit 0
fi

case $OPT_SOURCE in auto | marketplace | local | release) ;;
*) die "$EXIT_USAGE" USAGE "unknown source: $OPT_SOURCE" "$PROG --source local" ;;
esac
case $OPT_METHOD in auto | cli | unpack) ;;
*) die "$EXIT_USAGE" USAGE "unknown method: $OPT_METHOD" "$PROG --method cli" ;;
esac

SCRIPT_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" 2>/dev/null && pwd) || SCRIPT_DIR=.

SOURCE=$OPT_SOURCE
if [ "$SOURCE" = auto ]; then
	if [ -f "$SCRIPT_DIR/SHA256SUMS" ] && [ -f "$SCRIPT_DIR/SHA256SUMS.sig" ]; then
		SOURCE=local
	else
		SOURCE=marketplace
	fi
fi

# Editor table. Sets E_KIND E_CMD E_APP E_DIR E_EXT for editor $1.
editor_info() {
	case $1 in
	code)
		E_KIND=bin E_CMD=code E_APP=''
		E_DIR=$HOME/.vscode/extensions E_EXT=themes ;;
	code-flatpak)
		E_KIND=flatpak E_CMD=code E_APP=com.visualstudio.code
		E_DIR=$HOME/.var/app/com.visualstudio.code/data/vscode/extensions E_EXT=themes ;;
	codium)
		E_KIND=bin E_CMD=codium E_APP=''
		E_DIR=$HOME/.vscode-oss/extensions E_EXT=themes ;;
	codium-flatpak)
		E_KIND=flatpak E_CMD=codium E_APP=com.vscodium.codium
		E_DIR=$HOME/.var/app/com.vscodium.codium/data/codium/extensions E_EXT=themes ;;
	antigravity)
		E_KIND=bin E_CMD=antigravity E_APP=''
		E_DIR=$HOME/.antigravity/extensions E_EXT=themes-antigravity ;;
	antigravity-ide)
		E_KIND=bin E_CMD=antigravity-ide E_APP=''
		E_DIR=$HOME/.antigravity-ide/extensions E_EXT=themes-antigravity ;;
	*) return 1 ;;
	esac
	[ -n "$OPT_EXTDIR" ] && E_DIR=$OPT_EXTDIR
	return 0
}

cli_present() {
	case $E_KIND in
	bin) command -v "$E_CMD" >/dev/null 2>&1 ;;
	flatpak) command -v flatpak >/dev/null 2>&1 && flatpak info "$E_APP" >/dev/null 2>&1 ;;
	esac
}

run_cli() {
	if [ "$E_KIND" = flatpak ]; then
		flatpak run --command="$E_CMD" "$E_APP" "$@"
	else
		"$E_CMD" "$@"
	fi
}

# Sets M to cli or unpack, or empty when the editor is not installed.
resolve_method() {
	M=
	have_cli=0
	cli_present && have_cli=1
	# A bare extensions directory can be a leftover, so it only counts when
	# the user named the editor.
	have_dir=0
	if [ "$EXPLICIT" = 1 ] && { [ -d "$E_DIR" ] || [ -n "$OPT_EXTDIR" ]; }; then
		have_dir=1
	fi
	case $OPT_METHOD in
	cli) [ "$have_cli" = 1 ] && M=cli ;;
	unpack) { [ "$have_cli" = 1 ] || [ "$have_dir" = 1 ]; } && M=unpack ;;
	auto)
		if [ "$have_cli" = 1 ]; then
			M=cli
			if [ "$E_EXT" = themes-antigravity ]; then
				resolved=$(readlink -f "$(command -v "$E_CMD")" 2>/dev/null) || resolved=
				case $resolved in /nix/store/*) M=unpack ;; esac
			fi
		elif [ "$have_dir" = 1 ]; then
			M=unpack
		fi ;;
	esac
	[ -n "$M" ]
}

if [ -n "$OPT_EDITORS" ]; then
	EDITORS=$(printf '%s' "$OPT_EDITORS" | tr ',' ' ')
	for e in $EDITORS; do
		editor_info "$e" || die "$EXIT_USAGE" USAGE "unknown editor: $e" "$PROG --editor code"
	done
	EXPLICIT=1
else
	EDITORS=$AUTO_EDITORS
	EXPLICIT=0
fi
if [ -n "$OPT_EXTDIR" ]; then
	# shellcheck disable=SC2086 # split the space-separated editor list
	set -- $EDITORS
	[ "$EXPLICIT" = 1 ] && [ $# -eq 1 ] ||
		die "$EXIT_USAGE" USAGE "--extensions-dir needs exactly one --editor" "$PROG --editor code --extensions-dir $OPT_EXTDIR"
fi

WORK=$(mktemp -d "${TMPDIR:-/tmp}/$PROG.XXXXXX") ||
	die "$EXIT_FAIL" TEMPDIR "cannot create a temporary directory" "TMPDIR=\$HOME/.cache $PROG"
trap 'rm -rf "$WORK"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

fetch() {
	if command -v curl >/dev/null 2>&1; then
		curl -fsL --proto '=https' --tlsv1.2 -o "$2" "$1"
	elif command -v wget >/dev/null 2>&1; then
		wget -q -O "$2" "$1" 2>/dev/null
	else
		return 127
	fi
}

sha256_of() {
	if command -v sha256sum >/dev/null 2>&1; then
		sha256sum "$1" | cut -d' ' -f1
	elif command -v shasum >/dev/null 2>&1; then
		shasum -a 256 "$1" | cut -d' ' -f1
	else
		return 1
	fi
}

# Load and verify the signed manifest for local and release sources.
if [ "$SOURCE" != marketplace ]; then
	if [ "$SOURCE" = local ]; then
		MANIFEST=$SCRIPT_DIR/SHA256SUMS
		[ -f "$MANIFEST" ] && [ -f "$MANIFEST.sig" ] ||
			die "$EXIT_NOT_FOUND" MANIFEST_NOT_FOUND "no signed SHA256SUMS beside this script" "$PROG --source release"
	else
		if [ "$OPT_RELEASE" = latest ]; then
			BASE_URL=https://github.com/$REPO/releases/latest/download
		else
			BASE_URL=https://github.com/$REPO/releases/download/$OPT_RELEASE
		fi
		MANIFEST=$WORK/SHA256SUMS
		diag info FETCH "downloading $BASE_URL/SHA256SUMS"
		if ! { fetch "$BASE_URL/SHA256SUMS" "$MANIFEST" && fetch "$BASE_URL/SHA256SUMS.sig" "$MANIFEST.sig"; }; then
			die "$EXIT_NOT_FOUND" RELEASE_NOT_FOUND "cannot download SHA256SUMS from release $OPT_RELEASE" \
				"$PROG --source release --release <tag>"
		fi
	fi
	if [ "$OPT_SKIP_SIG" = 1 ]; then
		diag warn SIGNATURE_SKIPPED "signature not verified (--insecure-skip-signature); checksums still enforced"
	else
		command -v ssh-keygen >/dev/null 2>&1 ||
			die "$EXIT_VERIFY" VERIFIER_MISSING "ssh-keygen (OpenSSH 8.1+) is needed to verify the signature" \
				"$PROG --insecure-skip-signature"
		printf '%s namespaces="file" %s\n' "$SIGNER" "$SIGNER_KEY" >"$WORK/allowed_signers"
		ssh-keygen -Y verify -f "$WORK/allowed_signers" -I "$SIGNER" -n file -s "$MANIFEST.sig" \
			<"$MANIFEST" >/dev/null 2>&1 ||
			die "$EXIT_VERIFY" SIGNATURE_INVALID "SHA256SUMS is not signed by $SIGNER" \
				"$PROG --source marketplace"
		diag info SIGNATURE_OK "SHA256SUMS signature verified for $SIGNER"
	fi
fi

# Sets P_PATH P_VER for extension $1, verifying its checksum.
prepare_vsix() {
	line=$(awk -v n="$1" '{ b = $2; sub(/.*\//, "", b)
		if (b ~ ("^" n "-[0-9][0-9.]*\\.vsix$")) { print $1, $2; exit } }' "$MANIFEST")
	[ -n "$line" ] || { P_ERR="SHA256SUMS lists no $1 VSIX"; return "$EXIT_NOT_FOUND"; }
	expected=${line%% *}
	rel=${line#* }
	base=${rel##*/}
	P_VER=${base#"$1"-}
	P_VER=${P_VER%.vsix}
	if [ "$SOURCE" = local ]; then
		P_PATH=$SCRIPT_DIR/$rel
	else
		P_PATH=$WORK/$base
		if [ ! -f "$P_PATH" ]; then
			[ "$DRY_RUN" = 1 ] && return 0
			fetch "$BASE_URL/$base" "$P_PATH" ||
				{ P_ERR="cannot download $BASE_URL/$base"; return "$EXIT_NOT_FOUND"; }
		fi
	fi
	[ -f "$P_PATH" ] || { P_ERR="VSIX not found: $P_PATH"; return "$EXIT_NOT_FOUND"; }
	actual=$(sha256_of "$P_PATH") || { P_ERR="neither sha256sum nor shasum is available"; return "$EXIT_VERIFY"; }
	[ "$actual" = "$expected" ] || { P_ERR="checksum mismatch for $base"; return "$EXIT_VERIFY"; }
	return 0
}

extract_vsix() {
	if command -v unzip >/dev/null 2>&1; then
		unzip -q -o "$1" 'extension/*' -d "$2"
	elif command -v bsdtar >/dev/null 2>&1; then
		bsdtar -xf "$1" -C "$2" extension
	elif command -v python3 >/dev/null 2>&1; then
		python3 -c 'import sys, zipfile
z = zipfile.ZipFile(sys.argv[1])
z.extractall(sys.argv[2], [n for n in z.namelist() if n.startswith("extension/")])' "$1" "$2"
	else
		return 127
	fi
}

# registered <extensions.json> <id> <version>
registered() {
	if command -v jq >/dev/null 2>&1; then
		jq -e --arg id "$2" --arg v "$3" \
			'any(.[]; (.identifier.id | ascii_downcase) == $id and .version == $v)' "$1" >/dev/null 2>&1
	elif command -v python3 >/dev/null 2>&1; then
		python3 -c 'import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
sys.exit(0 if any(e["identifier"]["id"].lower() == sys.argv[2] and e.get("version") == sys.argv[3] for e in d) else 1)' "$1" "$2" "$3"
	else
		return 1
	fi
}

# register <extensions.json> <id> <version> <abs path> <folder>
# shellcheck disable=SC2016 # $id, $mid etc. belong to jq and Python, not the shell
register_to() {
	if command -v jq >/dev/null 2>&1; then
		jq -c --arg id "$2" --arg v "$3" --arg p "$4" --arg rel "$5" \
			'[.[] | select((.identifier.id | ascii_downcase) != $id)]
			+ [{identifier: {id: $id}, version: $v,
			    location: {"$mid": 1, path: $p, scheme: "file"}, relativeLocation: $rel}]' \
			"$1"
	elif command -v python3 >/dev/null 2>&1; then
		python3 -c 'import json, sys
f, i, v, p, r = sys.argv[1:6]
d = [e for e in json.load(open(f, encoding="utf-8")) if e["identifier"]["id"].lower() != i]
d.append({"identifier": {"id": i}, "version": v,
          "location": {"$mid": 1, "path": p, "scheme": "file"}, "relativeLocation": r})
json.dump(d, sys.stdout, separators=(",", ":"))' "$1" "$2" "$3" "$4" "$5"
	else
		return 127
	fi
}

# register <extensions.json> <id> <version> <abs path> <folder>
register() {
	tmp=$1.$PROG.$$
	if register_to "$@" >"$tmp" && mv -f "$tmp" "$1"; then
		return 0
	fi
	rm -f "$tmp"
	return 1
}

RESULTS_TEXT=
RESULTS_JSON=
FAILED=0
FAIL_CODE=0

# record <editor> <id> <method> <status> <detail>
record() {
	RESULTS_TEXT="$RESULTS_TEXT$1	$2	$3	$4
"
	item=$(printf '{"editor":%s,"extension":%s,"source":%s,"method":%s,"status":%s,"detail":%s}' \
		"$(json_str "$1")" "$(json_str "$2")" "$(json_str "$SOURCE")" "$(json_str "$3")" \
		"$(json_str "$4")" "$(json_str "$5")")
	RESULTS_JSON="${RESULTS_JSON:+$RESULTS_JSON,}$item"
}

fail_editor() {
	record "$1" "$2" "$3" failed "$4"
	diag warn INSTALL_FAILED "$1: $4" "$5"
	FAILED=1
	[ "$FAIL_CODE" = 0 ] && FAIL_CODE=${6:-$EXIT_FAIL}
	return 0
}

install_editor() {
	ed=$1
	editor_info "$ed"
	id=$PUBLISHER.$E_EXT
	if ! resolve_method; then
		if [ "$EXPLICIT" = 1 ]; then
			fail_editor "$ed" "$id" none "editor not found" "$PROG --editor $ed --extensions-dir <dir>" "$EXIT_NOT_FOUND"
		fi
		return 0
	fi

	if [ "$SOURCE" = marketplace ]; then
		if [ "$M" = unpack ]; then
			fail_editor "$ed" "$id" unpack "unpack needs a VSIX; the marketplace source provides only an ID" \
				"$PROG --editor $ed --source release --method unpack" "$EXIT_USAGE"
			return 0
		fi
		target=$id
	else
		prepare_vsix "$E_EXT" || {
			rc=$?
			fail_editor "$ed" "$id" "$M" "$P_ERR" "$PROG --source marketplace --editor $ed" "$rc"
			return 0
		}
		target=$P_PATH
	fi

	if [ "$DRY_RUN" = 1 ]; then
		if [ "$SOURCE" = marketplace ]; then
			what=$id
		elif [ -f "$P_PATH" ]; then
			what=$P_PATH
		else
			what="$BASE_URL/${P_PATH##*/}"
		fi
		record "$ed" "$id" "$M" planned "would install $what via $M into $E_DIR"
		diag ok PLANNED "$ed: would install $id via $M"
		return 0
	fi

	if [ "$M" = cli ]; then
		if [ "$E_KIND" = flatpak ] && [ "$SOURCE" != marketplace ]; then
			# The sandbox cannot see the host's /tmp; stage inside the app's cache.
			stage=$HOME/.var/app/$E_APP/cache/$PROG
			if ! { mkdir -p "$stage" && cp -f "$target" "$stage/"; }; then
				fail_editor "$ed" "$id" cli "cannot stage the VSIX for Flatpak" "$PROG --method unpack --editor $ed"
				return 0
			fi
			target=$stage/${target##*/}
		fi
		if [ -n "$OPT_EXTDIR" ]; then
			set -- --extensions-dir "$OPT_EXTDIR" --install-extension "$target" --force
		else
			set -- --install-extension "$target" --force
		fi
		diag info RUN "$ed: $E_CMD $*"
		out=$(run_cli "$@" 2>&1)
		rc=$?
		[ "$VERBOSE" = 1 ] && [ -n "$out" ] && printf '%s\n' "$out" >&2
		if [ $rc -ne 0 ]; then
			fail_editor "$ed" "$id" cli "$(printf '%s' "$out" | grep -v -i deprecat | tail -n 1)" \
				"$PROG --editor $ed --method unpack --source local"
			return 0
		fi
		record "$ed" "$id" cli installed "installed from $target"
		diag ok INSTALLED "$ed: installed $id"
		return 0
	fi

	# unpack
	folder=$id-$P_VER
	json=$E_DIR/extensions.json
	if [ -d "$E_DIR/$folder" ] && [ -f "$json" ] && registered "$json" "$id" "$P_VER"; then
		record "$ed" "$id" unpack unchanged "$id $P_VER already installed in $E_DIR"
		diag ok UNCHANGED "$ed: $id $P_VER already installed"
		return 0
	fi
	if [ -f "$json" ] && ! command -v jq >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
		fail_editor "$ed" "$id" unpack "registering in extensions.json needs jq or python3" "$PROG --editor $ed --method cli"
		return 0
	fi
	mkdir -p "$E_DIR" || { fail_editor "$ed" "$id" unpack "cannot create $E_DIR" "$PROG --editor $ed --extensions-dir <dir>" 4; return 0; }
	stage=$E_DIR/.$folder.$PROG.$$
	rm -rf "$stage" && mkdir "$stage" && extract_vsix "$P_PATH" "$stage" && [ -d "$stage/extension" ] || {
		rm -rf "$stage"
		fail_editor "$ed" "$id" unpack "cannot extract $P_PATH (needs unzip, bsdtar or python3)" "$PROG --editor $ed --method cli"
		return 0
	}
	if ! { rm -rf "${E_DIR:?}/$folder" && mv "$stage/extension" "$E_DIR/$folder"; }; then
		rm -rf "$stage"
		fail_editor "$ed" "$id" unpack "cannot move the extension into $E_DIR" "$PROG --editor $ed --extensions-dir <dir>"
		return 0
	fi
	rm -rf "$stage"
	# Without extensions.json the editor scans folders; creating one would hide the rest.
	if [ -f "$json" ]; then
		register "$json" "$id" "$P_VER" "$E_DIR/$folder" "$folder" || {
			fail_editor "$ed" "$id" unpack "cannot update $json" "$PROG --editor $ed --method cli"
			return 0
		}
	fi
	record "$ed" "$id" unpack installed "unpacked $P_VER into $E_DIR/$folder"
	diag ok INSTALLED "$ed: unpacked $id $P_VER (restart the editor if it is running)"
	return 0
}

for e in $EDITORS; do
	install_editor "$e"
done

if [ -z "$RESULTS_JSON" ]; then
	die "$EXIT_NOT_FOUND" NO_EDITOR "no supported editor found" "$PROG --editor code --extensions-dir <dir>"
fi

if [ "$FORMAT" = json ]; then
	printf '{"metadata":{"tool":"%s","version":"%s","command":%s,"timestamp":"%s","source":%s,"dry_run":%s},"data":[%s]}\n' \
		"$PROG" "$PROG_VERSION" "$(json_str "$INVOCATION")" "$(now)" "$(json_str "$SOURCE")" \
		"$([ "$DRY_RUN" = 1 ] && echo true || echo false)" "$RESULTS_JSON"
else
	printf '%s' "$RESULTS_TEXT"
fi

[ "$FAILED" = 1 ] && exit "$FAIL_CODE"
exit 0
