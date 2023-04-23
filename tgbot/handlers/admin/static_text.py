command_start = '/stats'
only_for_admins = 'Sorry, this function is available only for admins. Set "admin" flag in django admin panel.'

secret_admin_commands = f"⚠️ Secret Admin commands\n" \
                        f"{command_start} - bot stats"

users_amount_stat = "<b>Users</b>: {user_count}\n" \
                    "<b>24h active</b>: {active_24}"
