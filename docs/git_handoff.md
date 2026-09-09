# Git handoff

The project was prepared and committed locally for clean-clone verification.
No external remote was configured or contacted for publication. The distributed
source ZIP omits workstation Git configuration and caches; it contains the
submission project and its verified original implementation-history bundle.

The package-level `PROJECT_MANIFEST.json` identifies the local prepared commit
and every distributed project file. Extracting the ZIP does not by itself
create a GitHub repository. A future authorized upload must preserve these
file bytes, especially source, schemas, mappings, policy, prompts and the CSV.
The existing `.gitattributes` disables newline rewriting. No LFS or submodule
setup is required.

After choosing the intended destination and receiving publication authorization,
the source directory can be initialized/committed as a new Git repository, or
the prepared local repository can be used where still available. Verify the
remote content against this package after upload; its actual remote commit may
have a different history. Repository URL and account permissions remain genuine
later actions. A private assessor invitation must actually provide access;
an unaccepted invitation is not verified access.

The original implementation history is inspectable separately using
`evidence/history/README.md`. It is preserved as evidence rather than mixed into
the future destination's account configuration.
