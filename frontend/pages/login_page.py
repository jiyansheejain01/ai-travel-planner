"""
Trail map login / sign-up page for the AI Travel Planner.

Matches pages/landing_page.py's visual identity (palette, fonts, card
style) and talks to the backend's existing /auth/register, /auth/login,
and /auth/me endpoints via services/auth_service.py.
"""

from nicegui import ui

from services.auth_service import get_me, login, register

# ---------------------------------------------------------------------------
# Palette / tokens -- kept identical to landing_page.py for a consistent look
# ---------------------------------------------------------------------------
BG = '#F7F5F0'
INK = '#33342E'
MUTED = '#6B6D63'
LINE = '#DEDBD0'
BLUE = '#5B7C99'
MUSTARD = '#D4A24C'
CARD = '#FFFFFF'
ERROR = '#B24C4C'


def _load_fonts_and_icons() -> None:
    """Same one-time head injection as landing_page.py (idempotent if both run)."""
    ui.add_head_html('''
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500&display=swap" rel="stylesheet">
    ''')


def _page_style() -> None:
    ui.query('body').style(f'background:{BG};')
    ui.query('.nicegui-content').classes('items-center')


def build_login_page(on_success=None) -> None:
    """
    Renders the sign-in / create-account card.

    on_success: optional callable(dict) invoked with
        {"access_token", "refresh_token", "email"} once the user is
        authenticated (either by logging in, or by registering and then
        being logged in automatically). Typical use is to stash it in
        app.storage.user and navigate onward -- see main.py.
    """
    from nicegui import app

    _load_fonts_and_icons()
    _page_style()
    ui.colors(primary=BLUE, secondary=MUSTARD)

    mode = {'value': 'login'}  # 'login' | 'register'

    with ui.column().classes('items-center w-full').style(
        'max-width:420px; margin:0 auto; padding:64px 24px;'
    ):
        # --- Hero -----------------------------------------------------------
        with ui.column().classes('items-center w-full').style('position:relative;'):
            ui.html(f'''
<svg viewBox="0 0 320 40" width="100%" height="40"
     style="position:absolute;top:6px;left:0;opacity:0.5;">
    <path
        d="M 5 22 Q 80 4 160 20 T 315 12"
        fill="none"
        stroke="{BLUE}"
        stroke-width="2"
        stroke-dasharray="1 9"
        stroke-linecap="round"
    />
</svg>
''')

            eyebrow = ui.label('WELCOME BACK').style(
                f'position:relative; font-size:13px; letter-spacing:2px; color:{MUSTARD}; margin-bottom:6px;'
            )
            headline = ui.label('Sign in to continue').style(
                f'position:relative; font-family:Fraunces,serif; font-weight:500; '
                f'font-size:30px; line-height:1.2; color:{INK}; text-align:center; margin:0;'
            )

        ui.label(
            'Your planner agent remembers you across trips once you sign in.'
        ).style(
            f'max-width:360px; text-align:center; font-size:14px; color:{MUTED}; '
            f'line-height:1.6; margin:14px 0 28px;'
        )

        # --- Card -------------------------------------------------------------
        with ui.column().style(
            f'width:100%; background:{CARD}; border:0.5px solid {LINE}; '
            f'border-radius:14px; padding:24px 24px; gap:14px;'
        ):

            def _field_label(text: str) -> None:
                ui.label(text).style(
                    f'font-size:11.5px; font-weight:600; letter-spacing:0.3px; '
                    f'color:{MUTED}; margin-bottom:2px;'
                )

            error_label = ui.label('').style(
                f'font-size:12.5px; color:{ERROR}; min-height:16px;'
            )
            error_label.visible = False

            with ui.column().style('width:100%; gap:0;'):
                _field_label('EMAIL')
                email_input = ui.input(placeholder='you@example.com').props('borderless dense').style(
                    f'font-size:15px; color:{INK}; border-bottom:1px solid {LINE};'
                )

            with ui.column().style('width:100%; gap:0;'):
                _field_label('PASSWORD')
                password_input = ui.input(
                    placeholder='At least 8 characters',
                ).props('borderless dense type=password').style(
                    f'font-size:15px; color:{INK}; border-bottom:1px solid {LINE};'
                )

            confirm_column = ui.column().style('width:100%; gap:0;')
            with confirm_column:
                _field_label('CONFIRM PASSWORD')
                confirm_input = ui.input(
                    placeholder='Re-enter your password',
                ).props('borderless dense type=password').style(
                    f'font-size:15px; color:{INK}; border-bottom:1px solid {LINE};'
                )
            confirm_column.visible = False

            submit_button = ui.button('Sign in', color=None).props('unelevated no-caps').style(
                f'background:{BLUE}; color:white; border-radius:8px; font-weight:500; '
                f'width:100%; padding:10px 0; margin-top:4px;'
            )

        # --- Mode toggle ------------------------------------------------------
        with ui.row().classes('items-center justify-center').style('gap:6px; margin-top:18px;'):
            toggle_prompt = ui.label("Don't have an account?").style(
                f'font-size:13px; color:{MUTED};'
            )
            toggle_link = ui.link('Create one', '#').style(
                f'font-size:13px; color:{BLUE}; font-weight:600; text-decoration:none;'
            )

        def _set_error(message: str | None) -> None:
            error_label.text = message or ''
            error_label.visible = bool(message)

        def _set_mode(new_mode: str) -> None:
            mode['value'] = new_mode
            _set_error(None)

            if new_mode == 'login':
                eyebrow.text = 'WELCOME BACK'
                headline.text = 'Sign in to continue'
                submit_button.text = 'Sign in'
                confirm_column.visible = False
                toggle_prompt.text = "Don't have an account?"
                toggle_link.text = 'Create one'
            else:
                eyebrow.text = 'JOIN THE TRAIL'
                headline.text = 'Create your account'
                submit_button.text = 'Create account'
                confirm_column.visible = True
                toggle_prompt.text = 'Already have an account?'
                toggle_link.text = 'Sign in'

        def _toggle_mode() -> None:
            _set_mode('register' if mode['value'] == 'login' else 'login')

        toggle_link.on('click', lambda: _toggle_mode())

        async def _submit() -> None:
            email = (email_input.value or '').strip()
            password = password_input.value or ''

            if not email:
                _set_error('Please enter your email.')
                return

            if len(password) < 8:
                _set_error('Password must be at least 8 characters.')
                return

            if mode['value'] == 'register' and password != (confirm_input.value or ''):
                _set_error('Passwords do not match.')
                return

            _set_error(None)
            submit_button.props('loading')

            try:
                if mode['value'] == 'register':
                    await register(email, password)

                tokens = await login(email, password)
                access_token = tokens['access_token']

                user = await get_me(access_token)

                session = {
                    'access_token': access_token,
                    'refresh_token': tokens.get('refresh_token'),
                    'email': user.get('email', email),
                    'user_id': user.get('id'),
                }

                app.storage.user['auth'] = session

                ui.notify(
                    'Welcome back!' if mode['value'] == 'login' else 'Account created — welcome!',
                    type='positive',
                )

                if on_success:
                    on_success(session)
                else:
                    ui.navigate.to('/')

            except Exception as exc:
                _set_error(str(exc))
            finally:
                submit_button.props(remove='loading')

        submit_button.on('click', _submit)
        password_input.on('keydown.enter', _submit)
        confirm_input.on('keydown.enter', _submit)
