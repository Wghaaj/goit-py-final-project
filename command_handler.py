import contact_commands as cc


COMMAND_HANDLERS = {
    "add": cc.add_contact,
    "remove": cc.remove_contact,
    "change": cc.change_contact,
    "change-name": cc.change_name,
    "phone": cc.show_phone,
    "all": cc.show_all,

    "add-email": cc.add_email,
    "change-email": cc.change_email,
    "remove-email": cc.remove_email,

    "add-address": cc.add_address,
    "change-address": cc.change_address,
    "remove-address": cc.remove_address,

    "add-birthday": cc.add_birthday,
    "change-birthday": cc.change_birthday,
    "remove-birthday": cc.remove_birthday,
    "show-birthday": cc.show_birthday,
    "birthdays": cc.birthdays,
}