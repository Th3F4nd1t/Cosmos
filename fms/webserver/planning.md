## Pages
- /
    - login/
    - logout/
    - auth/
        - callback/
    - profile/ (All) → view/edit your account details
    - permissions/
        - request/ (All) → request to bind to a team or role
    - notifications/ (All) → system notices (match updates, field alerts)

    - status/
        - team/<team_number>/ (Requires TM & linked team number(s))
        - field/ (Requires FH/FM/FA)
        - admin/ (Requires FA)

    - matches/
        - schedule/
            - list/ (All)
            - edit/ (Requires FA/FM)
        - results/
            - list/ (All)
            - edit/ (Requires FA/FM)
        - rankings/ (All)
        - alliances/ (Requires FA/FM)
        - practice/ (Requires FA/FM)

    - event/
        - info/ (All) → event name, location, schedule
        - announcements/
            - list/ (All)
            - add/ (Requires FA/FM)

    - teams/
        - list/ (All) → teams at event
        - inspection/
            - list/ (Requires FH/FM/FA)
            - add/ (Requires FH/FM/FA)
            - edit/ (Requires FH/FM/FA)

    - queue/
        - list/ (All) → upcoming match queue status

    - field/
        - network/
            - status/ (Requires FA/FM)
            - config/ (Requires FA)
        - plc/
            - status/ (Requires FA/FM)
            - test/ (Requires FA)
        - logs/
            - system/ (Requires FA)
            - field/ (Requires FA/FM)
            - team/<team_number>/ (Requires TM or FH/FM/FA)

    - admin/
        - users/
            - add_fa/ (Requires FA)
            - remove_fa/ (Requires FA)
            - add_fm/ (Requires FA)
            - remove_fm/ (Requires FA)
            - add_fh/ (Requires FM/FA)
            - remove_fh/ (Requires FM/FA)
            - approve_tm/ (Requires FH/FM/FA)
            - remove_tm/ (Requires FH/FM/FA)
            - list/ (Requires FA)
        - teams/
            - add/ (Requires FA/FM)
            - remove/ (Requires FA/FM)
            - list/ (Requires FA/FM)
            - bind_user/ (Requires FA/FM/FH)
            - unbind_user/ (Requires FA/FM/FH)
            - edit/ (Requires FA/FM)
        - matches/
            - add/ (Requires FA/FM)
            - remove/ (Requires FA/FM)
            - list/ (Requires FA/FM)
            - edit/ (Requires FA/FM)
            - run/ (Requires FA/FM)
        - mode/
            - change/ (Requires FA/FM)
        - settings/
            - view/<setting> (Requires FA)
            - edit/<setting> (Requires FA)

