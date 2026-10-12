---
name: chatgpt-pro-handoff
description: Ask an ordinary ChatGPT Pro conversation to plan or review a task, with Codex supplying evidence and performing only authorized local work. Use for requests to involve actual Pro; not for general Pro availability questions.
---

# Ordinary ChatGPT Pro handoff

Run only the stages the user requested. For review-only requests, skip planning and implementation and submit the available evidence for review. For planning-only requests, return the plan without implementing it. Run planning, execution and review together only within the user's authorized scope.

This workflow requires actual replies from ordinary ChatGPT **Chat** using a user-confirmed Pro model. ChatGPT **Work** and Codex chats are different surfaces. Codex reasoning described as “Pro-level” is not a Pro reply. Do not switch Codex's model to simulate this workflow, extract cookies, use private reverse proxies or invent a completed Pro review.

## Select the conversation and route

The user selects and confirms the ordinary Pro conversation for this task. There are no default project bindings. Reuse a previously confirmed conversation when its identity, project relevance and Pro status remain applicable; recheck if they have changed or are uncertain.

Prefer direct app tools when the host exposes `list_threads`, `send_message_to_thread` and `read_thread` for ordinary ChatGPT Chat. Inspect the actual tool schemas and use `list_threads` to confirm the selected conversation's `chatgpt` identity. Send and read in that same conversation, omitting `model` and `thinking` overrides. These are host capabilities, not a general public API; a host may not expose them or may support only Codex chats. Do not invent tool names or treat the installer as providing these tools.

Otherwise, or when the user requests visible interaction, reuse a ChatGPT tab in the host's built-in browser, or open `https://chatgpt.com/` once. Confirm login, ordinary Chat and the user's selected Pro model once when establishing the conversation. If login is missing, let the user sign in. Browser profiles may be separate from other browsers. Reuse the confirmed conversation and direct tools for later turns when supported. Do not repeatedly open, reload or inspect Browser while Pro is thinking. If neither route is usable, report the missing capability and stop that dependent stage.

## Prepare and share evidence

Share only the material needed for the requested stage. Review selected source, diff, test output and applicable runtime evidence before sending; exclude credentials, personal data, private logs and unrelated content. Authorization to request Pro review does not imply permission to share unrelated private material.

For code-level work, provide actual selected source, diff, tests or an authorized connected repository. A summary does not prove Pro inspected code. Check the host's current upload capability rather than assuming historical browser limits. If upload is unavailable, use a bounded reviewed excerpt, an authorized connected source or ask the user to upload the necessary file.

[AI Context Linker](https://github.com/xhonye/AI-Context-Linker) is optional and external. If the user already uses it, refresh and review its context output before sharing. It does not call Pro or automatically attach context. Do not install it as a prerequisite or assume its output replaces source evidence.

## Requested stages

1. **Planning, if requested:** Ask Pro for bounded tasks, dependencies, reasons, testable acceptance criteria and unknowns. Read its actual reply, then compare recommendations with the current project and user scope.
2. **Execution, if authorized:** Codex performs the selected in-scope work and gathers actual changes, tests and applicable build/runtime evidence. Pro suggestions do not expand authorization.
3. **Review, if requested:** Send the actual evidence to the same Pro conversation. Ask for criterion-by-criterion `pass / revise / unknown`, with supporting evidence and missing checks. Address concrete in-scope failures and repeat only when a remaining failure warrants another review.

## Wait for the matching reply

Record the outgoing turn's message identifier, timestamp or a unique request marker, using whichever evidence the host provides. Match the new reply to that turn and the same conversation. A send acknowledgement or an older cached page is not completion. Read at sensible intervals through supported host mechanisms; do not resend the request merely because a reply is slow. Do not use Codex-only `wait_threads` for ordinary Chat unless the host explicitly documents support for it.

Stay with the requested stage until its reply completes when the host permits waiting. If the host cannot continue waiting, report the pending turn and missing step. Unattended continuation requires a supported host follow-up mechanism and the user's requested scope; this skill does not supply a scheduler or background service.

Report what Pro actually saw and concluded, what Codex independently verified, and what remains unknown. Pro acceptance is limited to the evidence supplied; it cannot establish device, production, deployment or user acceptance without those checks. Historical September 20–21, 2026 observations are not current model, quota or upload-policy verification. The full unattended planning/execution/review loop has not been demonstrated by this package. Do not guarantee a savings percentage.
