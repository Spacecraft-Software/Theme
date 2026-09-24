#!/usr/bin/env nu
# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Nushell twin of install-extensions.sh: same flags, output, and exit codes.
# Needs Nushell 0.112+; unzip, bsdtar or python3 only for --method unpack.

const PROG = "install-extensions"
const PROG_VERSION = "1.0.0"
const REPO = "Spacecraft-Software/Theme"
const PUBLISHER = "spacecraft-software"
const WEBSITE = "https://Theme.SpacecraftSoftware.org/"
const SIGNER = "Mohamed.Hammad@SpacecraftSoftware.org"
const SIGNER_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICAwZ9xGo7DR5LMIyJv6VoyoRrcgZXLPF76zdSYrQT/f"
const ALL_EDITORS = [code code-flatpak codium codium-flatpak antigravity antigravity-ide]
# `antigravity` is the legacy Antigravity 1.x IDE command; Antigravity 2.0
# reuses that name for an app that takes no extensions, so it is never
# auto-detected, only installed into when named with --editor.
const AUTO_EDITORS = [code code-flatpak codium codium-flatpak antigravity-ide]

const EXIT_FAIL = 1
const EXIT_USAGE = 2
const EXIT_NOT_FOUND = 3
const EXIT_VERIFY = 6

# Current UTC time as ISO 8601 with a Z suffix
def now []: nothing -> string {
    date now | date to-timezone UTC | format date "%Y-%m-%dT%H:%M:%SZ"
}

# True when AI_AGENT or AGENT is set to anything
def agent-env []: nothing -> bool {
    ($env.AI_AGENT? | default "" | is-not-empty) or ($env.AGENT? | default "" | is-not-empty)
}

# True when CI is set and not false/0
def ci-env []: nothing -> bool {
    ($env.CI? | default "" | str downcase) not-in ["" "0" "false"]
}

# Whether a diagnostic of this severity passes the floor
def floor-allows [
    ctx: record # Run context
    severity: string # error, warn, ok or info
]: nothing -> bool {
    if $ctx.quiet {
        $severity == "error"
    } else if $ctx.verbose {
        true
    } else if (agent-env) {
        $severity in [error warn]
    } else {
        $severity != "info"
    }
}

# Emit a non-error diagnostic on stderr
def diag [
    ctx: record # Run context
    severity: string # warn, ok or info
    code: string # Stable upper-snake-case code
    message: string # Human-readable message
    hint?: string # Runnable command that helps
]: nothing -> nothing {
    if not (floor-allows $ctx $severity) { return }
    if $ctx.format == "json" {
        mut body = { severity: $severity code: $code message: $message }
        if $hint != null { $body = ($body | insert hint $hint) }
        $body = ($body | insert timestamp (now) | insert command $ctx.invocation)
        print --stderr ({ diagnostic: $body } | to json --raw)
    } else {
        let tag = (match $severity { "warn" => "WARN" "ok" => "OK" _ => "INFO" })
        print --stderr $"[($tag)] ($message)"
        if $hint != null { print --stderr $"  hint: ($hint)" }
    }
}

# Emit a structured error, clean up, and exit
def die [
    ctx: record # Run context
    exit_code: int # Process exit code
    code: string # Stable upper-snake-case code
    message: string # Human-readable message
    hint: string # Runnable command that helps
]: nothing -> nothing {
    if $ctx.format == "json" {
        let body = {
            code: $code
            exit_code: $exit_code
            message: $message
            hint: $hint
            timestamp: (now)
            command: $ctx.invocation
            docs_url: $WEBSITE
        }
        print --stderr ({ error: $body } | to json --raw)
    } else {
        print --stderr $"[ERROR] ($message)"
        print --stderr $"  hint: ($hint)"
    }
    if ($ctx.work? | default "" | is-not-empty) { rm -rf $ctx.work }
    exit $exit_code
}

# The editor table, with the extensions directory optionally overridden
def editor-info [
    name: string # Editor name
    extdir: string # Override for the extensions directory, or ""
]: nothing -> record {
    let home = $env.HOME
    let table = {
        code: { kind: "bin" cmd: "code" app: "" dir: ($home | path join ".vscode" "extensions") ext: "themes" }
        code-flatpak: {
            kind: "flatpak" cmd: "code" app: "com.visualstudio.code"
            dir: ($home | path join ".var" "app" "com.visualstudio.code" "data" "vscode" "extensions")
            ext: "themes"
        }
        codium: { kind: "bin" cmd: "codium" app: "" dir: ($home | path join ".vscode-oss" "extensions") ext: "themes" }
        codium-flatpak: {
            kind: "flatpak" cmd: "codium" app: "com.vscodium.codium"
            dir: ($home | path join ".var" "app" "com.vscodium.codium" "data" "codium" "extensions")
            ext: "themes"
        }
        antigravity: {
            kind: "bin" cmd: "antigravity" app: ""
            dir: ($home | path join ".antigravity" "extensions") ext: "themes-antigravity"
        }
        antigravity-ide: {
            kind: "bin" cmd: "antigravity-ide" app: ""
            dir: ($home | path join ".antigravity-ide" "extensions") ext: "themes-antigravity"
        }
    }
    let info = ($table | get $name)
    if ($extdir | is-empty) { $info } else { $info | update dir $extdir }
}

# Whether the editor's command-line interface is available
def cli-present [e: record]: nothing -> bool {
    if $e.kind == "flatpak" {
        (which flatpak | is-not-empty) and ((do { ^flatpak info $e.app } | complete).exit_code == 0)
    } else {
        which $e.cmd | is-not-empty
    }
}

# Run the editor's CLI and capture its output
def run-cli [e: record args: list<string>]: nothing -> record {
    if $e.kind == "flatpak" {
        do { ^flatpak run $"--command=($e.cmd)" $e.app ...$args } | complete
    } else {
        do { run-external $e.cmd ...$args } | complete
    }
}

# cli or unpack, or "" when the editor is not installed
def resolve-method [ctx: record e: record]: nothing -> string {
    let have_cli = (cli-present $e)
    # A bare extensions directory can be a leftover; it counts only when named.
    let have_dir = ($ctx.explicit and (($e.dir | path exists) or ($ctx.extdir | is-not-empty)))
    match $ctx.method {
        "cli" => (if $have_cli { "cli" } else { "" })
        "unpack" => (if $have_cli or $have_dir { "unpack" } else { "" })
        _ => {
            if $have_cli {
                let resolved = (which $e.cmd | get 0?.path? | default "" | path expand)
                if $e.ext == "themes-antigravity" and ($resolved | str starts-with "/nix/store/") {
                    "unpack"
                } else {
                    "cli"
                }
            } else if $have_dir {
                "unpack"
            } else {
                ""
            }
        }
    }
}

# Download a URL to a file; true on success
def fetch [url: string dest: string]: nothing -> bool {
    try {
        http get --raw $url | save --force --raw $dest
        true
    } catch {
        false
    }
}

# Locate, download if needed, and checksum the VSIX for an extension
def prepare-vsix [ctx: record name: string]: nothing -> record {
    let pattern = $"^($name)-[0-9][0-9.]*\\.vsix$"
    let row = (
        open --raw $ctx.manifest
        | lines
        | parse "{hash}  {path}"
        | where { |r| ($r.path | path basename) =~ $pattern }
        | get 0?
    )
    if $row == null {
        return { ok: false exit: $EXIT_NOT_FOUND err: $"SHA256SUMS lists no ($name) VSIX" }
    }
    let base = ($row.path | path basename)
    let version = ($base | str replace $"($name)-" "" | str replace ".vsix" "")
    let path = (if $ctx.source == "local" {
        $ctx.script_dir | path join $row.path
    } else {
        $ctx.work | path join $base
    })
    let url = $"($ctx.base_url)/($base)"
    if $ctx.source == "release" and not ($path | path exists) {
        if $ctx.dry_run {
            return { ok: true path: $path version: $version url: $url }
        }
        if not (fetch $url $path) {
            return { ok: false exit: $EXIT_NOT_FOUND err: $"cannot download ($url)" }
        }
    }
    if not ($path | path exists) {
        return { ok: false exit: $EXIT_NOT_FOUND err: $"VSIX not found: ($path)" }
    }
    if (open --raw $path | hash sha256) != $row.hash {
        return { ok: false exit: $EXIT_VERIFY err: $"checksum mismatch for ($base)" }
    }
    { ok: true path: $path version: $version url: $url }
}

# Extract the VSIX's extension/ folder into dest
def extract-vsix [vsix: string dest: string]: nothing -> bool {
    let run = (if (which unzip | is-not-empty) {
        do { ^unzip -q -o $vsix "extension/*" -d $dest } | complete
    } else if (which bsdtar | is-not-empty) {
        do { ^bsdtar -xf $vsix -C $dest extension } | complete
    } else if (which python3 | is-not-empty) {
        let code = "import sys, zipfile
z = zipfile.ZipFile(sys.argv[1])
z.extractall(sys.argv[2], [n for n in z.namelist() if n.startswith('extension/')])"
        do { ^python3 -c $code $vsix $dest } | complete
    } else {
        { exit_code: 127 }
    })
    $run.exit_code == 0
}

# A failed result record
def failed [
    ctx: record
    editor: string
    id: string
    method: string
    detail: string
    hint: string
    exit_code: int
]: nothing -> record {
    diag $ctx warn INSTALL_FAILED $"($editor): ($detail)" $hint
    {
        editor: $editor
        extension: $id
        source: $ctx.source
        method: $method
        status: "failed"
        detail: $detail
        exit: $exit_code
    }
}

# Install into one editor; returns a result record, or null when absent
def install-editor [ctx: record name: string]: nothing -> any {
    let e = (editor-info $name $ctx.extdir)
    let id = $"($PUBLISHER).($e.ext)"
    let method = (resolve-method $ctx $e)
    let ok = { |m: string, status: string, detail: string|
        { editor: $name extension: $id source: $ctx.source method: $m status: $status detail: $detail exit: 0 }
    }
    if ($method | is-empty) {
        if $ctx.explicit {
            return (failed $ctx $name $id "none" "editor not found"
                $"($PROG) --editor ($name) --extensions-dir <dir>" $EXIT_NOT_FOUND)
        }
        return null
    }

    mut prepared_vsix: any = null
    if $ctx.source == "marketplace" {
        if $method == "unpack" {
            return (failed $ctx $name $id "unpack" "unpack needs a VSIX; the marketplace source provides only an ID"
                $"($PROG) --editor ($name) --source release --method unpack" $EXIT_USAGE)
        }
    } else {
        let prepared = (prepare-vsix $ctx $e.ext)
        if not $prepared.ok {
            return (failed $ctx $name $id $method $prepared.err
                $"($PROG) --source marketplace --editor ($name)" $prepared.exit)
        }
        $prepared_vsix = $prepared
    }
    let vsix = $prepared_vsix

    if $ctx.dry_run {
        let what = (if $vsix == null {
            $id
        } else if ($vsix.path | path exists) {
            $vsix.path
        } else {
            $vsix.url
        })
        diag $ctx ok PLANNED $"($name): would install ($id) via ($method)"
        return (do $ok $method "planned" $"would install ($what) via ($method) into ($e.dir)")
    }

    if $method == "cli" {
        mut target = (if $vsix == null { $id } else { $vsix.path })
        if $e.kind == "flatpak" and $vsix != null {
            # The sandbox cannot see the host's /tmp; stage inside the app's cache.
            let stage = ($env.HOME | path join ".var" "app" $e.app "cache" $PROG)
            mkdir $stage
            cp -f $target $stage
            $target = ($stage | path join ($target | path basename))
        }
        let base_args = [--install-extension $target --force]
        let args = (if ($ctx.extdir | is-empty) {
            $base_args
        } else {
            [--extensions-dir $ctx.extdir] | append $base_args
        })
        diag $ctx info RUN $"($name): ($e.cmd) ($args | str join ' ')"
        let run = (run-cli $e $args)
        let output = ($run.stdout + $run.stderr)
        if $ctx.verbose and ($output | is-not-empty) { print --stderr $output }
        if $run.exit_code != 0 {
            let reason = (
                $output | lines | where { |l| not ($l =~ "(?i)deprecat") } | last 1 | str join ""
            )
            return (failed $ctx $name $id "cli" $reason
                $"($PROG) --editor ($name) --method unpack --source local" $EXIT_FAIL)
        }
        diag $ctx ok INSTALLED $"($name): installed ($id)"
        return (do $ok "cli" "installed" $"installed from ($target)")
    }

    # unpack
    let folder = $"($id)-($vsix.version)"
    let dest = ($e.dir | path join $folder)
    let json = ($e.dir | path join "extensions.json")
    let registered = (($json | path exists) and (
        open $json | any { |x| ($x.identifier.id | str downcase) == $id and $x.version == $vsix.version }
    ))
    if ($dest | path exists) and $registered {
        diag $ctx ok UNCHANGED $"($name): ($id) ($vsix.version) already installed"
        return (do $ok "unpack" "unchanged" $"($id) ($vsix.version) already installed in ($e.dir)")
    }
    let stage = ($e.dir | path join $".($folder).($PROG).(random chars --length 8)")
    try { mkdir $stage } catch {
        return (failed $ctx $name $id "unpack" $"cannot create ($e.dir)"
            $"($PROG) --editor ($name) --extensions-dir <dir>" 4)
    }
    if not (extract-vsix $vsix.path $stage) or not ($stage | path join "extension" | path exists) {
        rm -rf $stage
        return (failed $ctx $name $id "unpack" $"cannot extract ($vsix.path) \(needs unzip, bsdtar or python3\)"
            $"($PROG) --editor ($name) --method cli" $EXIT_FAIL)
    }
    rm -rf $dest
    mv ($stage | path join "extension") $dest
    rm -rf $stage
    # Without extensions.json the editor scans folders; creating one would hide the rest.
    if ($json | path exists) {
        let entry = {
            identifier: { id: $id }
            version: $vsix.version
            location: { "$mid": 1 path: $dest scheme: "file" }
            relativeLocation: $folder
        }
        let tmp = $"($json).($PROG).tmp"
        try {
            open $json
            | where { |x| ($x.identifier.id | str downcase) != $id }
            | append $entry
            | to json --raw
            | save --force $tmp
            mv -f $tmp $json
        } catch {
            rm -f $tmp
            return (failed $ctx $name $id "unpack" $"cannot update ($json)"
                $"($PROG) --editor ($name) --method cli" $EXIT_FAIL)
        }
    }
    diag $ctx ok INSTALLED $"($name): unpacked ($id) ($vsix.version) \(restart the editor if it is running\)"
    do $ok "unpack" "installed" $"unpacked ($vsix.version) into ($dest)"
}

# Install the Spacecraft Software colour themes into every detected
# VS Code-family editor: VS Code, VSCodium, Antigravity, Antigravity IDE,
# native or Flatpak.
#
# Sources: marketplace (the editor's own gallery, by ID), local (the VSIX
# files beside this script), release (a GitHub release), auto (local in a
# checkout, otherwise marketplace). Methods: cli (--install-extension),
# unpack (extract and register in extensions.json), auto (cli, or unpack
# when the editor has no usable CLI, as with Nix-wrapped Antigravity).
#
# Exit codes: 0 success, 1 an editor failed, 2 usage error, 3 not found,
# 6 checksum or signature verification failed.
#
# Examples:
#   nu install-extensions.nu --source local --dry-run
#   nu install-extensions.nu --source release --editor code,codium --json
#   nu install-extensions.nu --editor antigravity-ide --method unpack --source local
#
# Maintained by Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# https://Theme.SpacecraftSoftware.org/
def main [
    --source: string = "auto" # marketplace, local, release or auto
    --release: string = "latest" # Release tag for --source release
    --editor: string = "" # Comma-separated editors (default: all detected; antigravity only when named)
    --method: string = "auto" # cli, unpack or auto
    --extensions-dir: string = "" # Extensions directory (one editor only)
    --insecure-skip-signature # Check sums without verifying their signature
    --dry-run # Show what would be installed; change nothing
    --json # Machine-readable output (same as --format json)
    --format: string = "" # json (the only structured format supported)
    --quiet (-q) # Errors only on stderr
    --verbose (-v) # Everything on stderr, including editor CLI output
    --no-color # Accepted for compatibility; output is never coloured
    --version # Show version
]: nothing -> nothing {
    let flags = (
        [
            (if $source != "auto" { [--source $source] } else { [] })
            (if $release != "latest" { [--release $release] } else { [] })
            (if ($editor | is-not-empty) { [--editor $editor] } else { [] })
            (if $method != "auto" { [--method $method] } else { [] })
            (if ($extensions_dir | is-not-empty) { [--extensions-dir $extensions_dir] } else { [] })
            (if $insecure_skip_signature { [--insecure-skip-signature] } else { [] })
            (if $dry_run { [--dry-run] } else { [] })
            (if $json { [--json] } else { [] })
            (if ($format | is-not-empty) { [--format $format] } else { [] })
            (if $quiet { [--quiet] } else { [] })
            (if $verbose { [--verbose] } else { [] })
            (if $version { [--version] } else { [] })
        ]
        | flatten
    )
    let invocation = ([$PROG] | append $flags | str join " ")

    let requested = (if $json { "json" } else { $format })
    let detected = (if ($requested | is-not-empty) {
        $requested
    } else if (agent-env) or (ci-env) {
        "json"
    } else if (is-terminal --stdout) {
        "text"
    } else {
        "json"
    })
    mut ctx = {
        format: (if $detected in [json text] { $detected } else { "text" })
        invocation: $invocation
        quiet: $quiet
        verbose: $verbose
        work: ""
    }
    if $detected not-in [json text] {
        die $ctx $EXIT_USAGE USAGE $"unsupported format: ($detected) \(only json\)" $"($PROG) --json"
    }
    if $quiet and $verbose {
        die $ctx $EXIT_USAGE USAGE "--quiet and --verbose are mutually exclusive" $"($PROG) --quiet"
    }

    if $version {
        if $ctx.format == "json" {
            let metadata = {
                tool: $PROG
                version: $PROG_VERSION
                command: $invocation
                timestamp: (now)
                maintainer: "Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>"
                website: $WEBSITE
            }
            print ({ metadata: $metadata data: { version: $PROG_VERSION } } | to json --raw)
        } else {
            print $"($PROG) ($PROG_VERSION)"
            print "Maintained by Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>"
            print $WEBSITE
        }
        return
    }

    if $source not-in [auto marketplace local release] {
        die $ctx $EXIT_USAGE USAGE $"unknown source: ($source)" $"($PROG) --source local"
    }
    if $method not-in [auto cli unpack] {
        die $ctx $EXIT_USAGE USAGE $"unknown method: ($method)" $"($PROG) --method cli"
    }

    let script_dir = ($env.FILE_PWD? | default ".")
    let resolved_source = (if $source != "auto" {
        $source
    } else if ($script_dir | path join "SHA256SUMS" | path exists) and ($script_dir | path join "SHA256SUMS.sig" | path exists) {
        "local"
    } else {
        "marketplace"
    })

    let explicit = ($editor | is-not-empty)
    let editors = (if $explicit { $editor | split row "," | str trim | where { |x| $x != "" } } else { $AUTO_EDITORS })
    for e in $editors {
        if $e not-in $ALL_EDITORS {
            die $ctx $EXIT_USAGE USAGE $"unknown editor: ($e)" $"($PROG) --editor code"
        }
    }
    if ($extensions_dir | is-not-empty) and (not $explicit or ($editors | length) != 1) {
        die $ctx $EXIT_USAGE USAGE "--extensions-dir needs exactly one --editor" $"($PROG) --editor code --extensions-dir ($extensions_dir)"
    }

    $ctx = ($ctx | merge {
        source: $resolved_source
        method: $method
        explicit: $explicit
        extdir: $extensions_dir
        dry_run: $dry_run
        script_dir: $script_dir
        work: (mktemp --directory --tmpdir $"($PROG).XXXXXX")
        manifest: ""
        base_url: ""
    })

    if $resolved_source != "marketplace" {
        if $resolved_source == "local" {
            let manifest = ($script_dir | path join "SHA256SUMS")
            if not (($manifest | path exists) and ($"($manifest).sig" | path exists)) {
                die $ctx $EXIT_NOT_FOUND MANIFEST_NOT_FOUND "no signed SHA256SUMS beside this script" $"($PROG) --source release"
            }
            $ctx = ($ctx | update manifest $manifest)
        } else {
            let base_url = (if $release == "latest" {
                $"https://github.com/($REPO)/releases/latest/download"
            } else {
                $"https://github.com/($REPO)/releases/download/($release)"
            })
            let manifest = ($ctx.work | path join "SHA256SUMS")
            $ctx = ($ctx | update manifest $manifest | update base_url $base_url)
            diag $ctx info FETCH $"downloading ($base_url)/SHA256SUMS"
            if not ((fetch $"($base_url)/SHA256SUMS" $manifest) and (fetch $"($base_url)/SHA256SUMS.sig" $"($manifest).sig")) {
                die $ctx $EXIT_NOT_FOUND RELEASE_NOT_FOUND $"cannot download SHA256SUMS from release ($release)" $"($PROG) --source release --release <tag>"
            }
        }
        if $insecure_skip_signature {
            diag $ctx warn SIGNATURE_SKIPPED "signature not verified (--insecure-skip-signature); checksums still enforced"
        } else {
            if (which ssh-keygen | is-empty) {
                die $ctx $EXIT_VERIFY VERIFIER_MISSING "ssh-keygen (OpenSSH 8.1+) is needed to verify the signature" $"($PROG) --insecure-skip-signature"
            }
            let signers = ($ctx.work | path join "allowed_signers")
            $"($SIGNER) namespaces=\"file\" ($SIGNER_KEY)\n" | save --force $signers
            let manifest = $ctx.manifest
            let check = (
                do { open --raw $manifest | ^ssh-keygen -Y verify -f $signers -I $SIGNER -n file -s $"($manifest).sig" }
                | complete
            )
            if $check.exit_code != 0 {
                die $ctx $EXIT_VERIFY SIGNATURE_INVALID $"SHA256SUMS is not signed by ($SIGNER)" $"($PROG) --source marketplace"
            }
            diag $ctx info SIGNATURE_OK $"SHA256SUMS signature verified for ($SIGNER)"
        }
    }

    mut results = []
    for name in $editors {
        let result = (install-editor $ctx $name)
        if $result != null { $results = ($results | append $result) }
    }
    rm -rf $ctx.work
    $ctx = ($ctx | update work "")

    if ($results | is-empty) {
        die $ctx $EXIT_NOT_FOUND NO_EDITOR "no supported editor found" $"($PROG) --editor code --extensions-dir <dir>"
    }

    if $ctx.format == "json" {
        let metadata = {
            tool: $PROG
            version: $PROG_VERSION
            command: $invocation
            timestamp: (now)
            source: $resolved_source
            dry_run: $dry_run
        }
        print ({ metadata: $metadata data: ($results | reject exit) } | to json --raw)
    } else {
        $results | each { |r| print $"($r.editor)\t($r.extension)\t($r.method)\t($r.status)" } | ignore
    }

    let failures = ($results | where exit != 0)
    if ($failures | is-not-empty) { exit ($failures | first | get exit) }
}
