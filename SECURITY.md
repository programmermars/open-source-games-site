# Security policy

This is a static website. It has no server code, no accounts, no forms and no database, and it collects no personal data.

## Reporting a vulnerability

Report security problems privately through GitHub: open the **Security** tab of this repository and choose **Report a vulnerability**. Please don't open a public issue for a vulnerability.

In scope:

- Weaknesses in the response headers or Content-Security-Policy in `public/_headers`.
- Script injection or any way to make the generated pages run code they shouldn't.
- Anything that lets a third party use this site's resources or name.

## Hijacked or dead links

A game or homepage link that now leads to a parked, unrelated or malicious site is not secret: open a normal issue so it can be removed quickly. A scheduled workflow (`.github/workflows/check-links.yml`) also checks every link each week and fails when a link starts redirecting to a different domain.

## Out of scope

- Vulnerabilities in the games themselves. Report them to their authors; the credits page lists each project's source.
- Problems in Cloudflare or GitHub. Report them to those platforms.
