# Contributing Guide
This guide explains how to set up the project, contribute code, test changes, review pull requests,
and release updates. All contributions should follow the team's Definition of Done and project
standards.
## Code of Conduct
All team members are expected to treat one another respectfully, listen to different perspectives,
and allow everyone the opportunity to contribute. Disagreements should be handled
constructively and in good faith.
If a conflict arises, team members should first attempt to discuss the issue privately. If the issue
cannot be resolved, the team should seek guidance from the professor or instructional team.
## Getting Started
Repository access, development environment requirements, and setup instructions will be
finalized once the team establishes access to the project repository.
- Before contributing, team members should:
- Obtain access to the project repository and required development tools.
- Follow the setup instructions in the project README.
- Configure any required environment variables or local settings.
- Verify that the application runs locally before making changes.
Never commit passwords, API keys, access tokens, or other sensitive information to the
repository. Instructions for handling environment variables and secrets will be documented once
the development environment is established.
## Branching & Workflow
The team will use GitHub to manage code contributions and coordinate development. The exact
branching strategy and default branch will be established once repository access is available.
Our proposed general workflow is:
- Start by reviewing or receiving an assigned issue.
- Create a separate branch for the issue or feature being worked on.
- Implement the changes and test them locally.
- Commit the changes with descriptive commit messages.
- Open a pull request for review.
- Address reviewer feedback and ensure all required checks pass before merging.
Avoid committing directly to the default branch unless the team explicitly agrees otherwise.
Keep branches focused on a single issue or related set of changes.
## Issues & Planning
GitHub Issues will be used to track tasks, bugs, and feature requests, with additional planning
coordinated through the team's agreed-upon tools.
Issues should include:
- A clear title and description.
- The problem being addressed or the intended outcome.
- Relevant requirements and acceptance criteria.
- Any useful supporting information, screenshots, or reproduction steps.
- An assigned team member and priority when applicable.
Team members should communicate about task progress and blockers through Discord. Work
that affects project architecture, tooling, or other team members should be discussed with the
group before implementation.
## Commit Messages
Commit messages should be concise and descriptive, explaining what changed. The team will
establish a formal commit message convention once the repository is configured.
## Code Style, Linting & Formatting
All code should follow the formatting and style conventions established by the project. Team
members should check existing code and project configuration before introducing new patterns.
The team will determine the required language-specific formatters, linters, and commands once
the technology stack and repository configuration are confirmed.
Before submitting a pull request:
- Format the changed code using the project's formatter.
- Run the configured linter, if available.
- Resolve warnings and errors introduced by the changes.
- Keep changes focused and avoid unrelated modifications.
## Testing
Contributors are responsible for testing their changes before submitting a pull request. Testing
requirements and commands will be finalized after the project environment and CI pipeline are
established. Depending on the change, different tests are required:
- Unit tests
- Integration tests
- End-to-end tests
New functionality should include appropriate tests. Bug fixes should include regression tests
when practical to prevent an issue from reoccurring. Document all tests added/updated in the pull
requests, or reasoning if that is not possible.
## Definition of Done
A contribution is considered complete when:
- The implementation meets the issue's requirements and acceptance criteria.
- The contributor understands and can explain the code they submit.
- Appropriate tests have been added or updated and pass.
- Formatting and linting checks pass when configured.
- Relevant documentation has been updated.
- The pull request has received the required review and approval.
- All required CI checks pass before merging.
The team will identify the specific CI jobs and required checks once the repository pipeline is
configured. CI jobs are owned by the Quality Owner, while tests are owned by the Testing and
Quality Assurance Lead. Additionally, the Documentation Manager is responsible for confirming
the completeness of code documentation before any changes are merged.
## Contribution Norm
Every team member is expected to contribute at least one piece of accepted work per sprint.
Contributions may include code, tests, documentation, bug fixes, or other agreed-upon project
work.
Project work should be tracked through the team's issue tracker, with code and documentation
stored in the appropriate repository locations. Work involving the project partner's systems
should follow the partner's established processes.
Accepted work must meet the relevant requirements, be documented when necessary, and
receive the required review or approval. Team members should communicate early if they
encounter blockers or anticipate difficulty completing an assigned task.
## Pull Requests & Reviews
All changes should be submitted through pull requests unless the team agrees on an exception.
Pull requests should include:
- A descriptive title and summary of the changes.
- A reference to the associated issue, when applicable.
- A description of how the changes were tested.
- Screenshots or other supporting evidence when useful.
- Any relevant documentation updates or known limitations.
Reviewers should verify that the changes meet the requirements, are understandable, follow
project conventions, and include appropriate tests. Reviewers should provide constructive
feedback, and authors should address requested changes before merging.
The required number of approvals, branch protection rules, pull request templates, and status
checks will be established when repository settings are finalized.
## CI/CD
The team will use the repository's configured continuous integration and deployment pipeline to
automate applicable checks and support reliable releases.
The specific pipeline, required jobs, and deployment process will be documented once they are
established.
Contributors should verify that required CI checks pass before merging. If a check fails, review
its logs, resolve the issue, and rerun the checks. Do not bypass required checks without team
agreement.
The Quality Owner is responsible for maintaining the health of the repository, managing the CI
pipeline, and overseeing deployments and rollbacks.
## Security & Secrets
Security and confidentiality must be considered throughout development.
Contributors must:
- Never commit credentials, API keys, tokens, or other secrets.
- Use approved environment variables or secret-management mechanisms for sensitive configuration.
- Avoid including confidential project or partner information in public documentation or external tools.
- Keep dependencies up to date according to the project's agreed-upon process.
- Report suspected vulnerabilities or accidental exposure of sensitive information to the team promptly.
- Do not publish details of a suspected vulnerability publicly before coordinating with the team and project partner.
- The team will document approved security scanning tools and dependency update requirements once the development environment is established.
## Documentation Expectations
Documentation should be updated alongside code changes so that the project remains
understandable and maintainable.
Depending on the change, contributors should update:
- The README and setup instructions.
- Relevant technical documentation.
- API documentation or usage instructions.
- Tests and test instructions.
- Architecture Decision Records (ADRs) for significant technical decisions.
- Meeting notes or other project records when applicable.
- Code should be readable, with comments and docstrings used where they clarify non-obvious behavior or important implementation decisions.
Significant decisions affecting project architecture, tooling, or project-wide functionality should
be documented. Meeting summaries and project documentation should be uploaded to the team's
agreed-upon repository or shared folder. If external resources or AI-generated code are used, cite
them appropriately and ensure that the contributor understands the code before integrating it.
## Release Process
The Quality Owner is responsible for overseeing releases, managing deployments, and
coordinating rollbacks when necessary. The release process, versioning scheme, tagging
conventions, and deployment commands will be established once the project environment and
CI/CD pipeline are finalized.
Before a release:
- Confirm that the changes meet the Definition of Done.
- Verify that required tests and CI checks pass.
- Ensure relevant documentation is current.
- Obtain any required approvals.
- Follow the agreed-upon deployment procedure.
If a release introduces a significant issue, the Quality Owner will coordinate a rollback to a
previous working release when necessary. Release notes and documentation should record
relevant changes. Project-wide changes affecting scope, direction, or major functionality must be
discussed with the project partner and receive the required approval before implementation or
release.
## Support & Contact
For day-to-day questions, task coordination, and blockers, use the team's Discord server. Team
members should respond to direct Discord questions within 24 hours. General questions directed
to the team should receive a response within 72 hours. If a direct question receives no response
within 24 hours, another message may be sent. If there is still no response 48 hours after the
follow-up, contact the TA or instructional team. For repository access, development setup, or CI
issues, contact the appropriate team member or Quality Owner. For project-wide questions or
decisions, coordinate with the Project Manager and project partner as appropriate.